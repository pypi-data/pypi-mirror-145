import copy
from functools import cached_property

from google.protobuf.json_format import ParseDict

from mgo_serializer.fields import BaseField, Empty, set_value
from mgo_serializer.exceptions import ValidationError
from mgo_serializer.helpers import BindingDict, ReturnList, ReturnDict, NestedBoundField, BoundField
from mgo_serializer.meta import SerializerMetaclass


def mongo_to_protobuf(data, schema):
    """
    Convert data to protobuf.
    :return: protobuf
    :rtype: object
    """
    protobuf = schema() if callable(schema) else schema
    return ParseDict(data, protobuf)


class BaseSerializer(BaseField):
    """
    Base class for all serializers.
    """

    def __init__(self, instance=None, data=Empty, **kwargs):
        self.instance = instance
        if data is not Empty:
            self.initial_data = data
        self.partial = kwargs.pop("partial", False)
        kwargs.pop("many", None)
        super().__init__(**kwargs)

    def __new__(cls, *args, **kwargs):
        if kwargs.pop("many", False):
            return cls.many_init(*args, **kwargs)
        return super().__new__(cls, *args, **kwargs)

    def __class_getitem__(cls, *args, **kwargs):
        """
        Allow type checkers to make serializers generic.
        """
        return cls

    @classmethod
    def many_init(cls, *args, **kwargs):
        child_serializer = cls(*args, **kwargs)
        list_kwargs = {
            'child': child_serializer
        }
        list_kwargs.update({
            key: value for key, value in kwargs.items()
        })
        meta = getattr(cls, 'Meta', None)
        list_serializer_class = getattr(meta, 'list_serializer_class', ListSerializer)
        return list_serializer_class(*args, **list_kwargs)

    def to_internal_value(self, data):
        raise NotImplementedError('.to_internal_value() must be implemented.')

    def to_representation(self, value):
        raise NotImplementedError('.to_representation() must be implemented.')

    def to_protobuf(self, data):
        raise NotImplementedError('.to_protobuf() must be implemented.')

    def is_valid(self):
        """
        Validates the data.
        """
        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.to_internal_value(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        return not bool(self._errors)

    @property
    def data(self):
        """
        Returns the serialized data on the serializer.

        :see: https://www.django-rest-framework.org/api-guide/serializers/#data
        """
        if hasattr(self, 'initial_data') and not hasattr(self, '_validated_data'):
            msg = (
                'When a serializer is passed a `data` keyword argument you '
                'must call `.is_valid()` before attempting to access the '
                'serialized `.data` representation.\n'
                'You should either call `.is_valid()` first, '
                'or access `.initial_data` instead.'
            )
            raise AssertionError(msg)

        if not hasattr(self, '_data'):
            if self.instance is not None and not getattr(self, '_errors', None):
                self._data = self.to_representation(self.instance)
            elif hasattr(self, '_validated_data') and not getattr(self, '_errors', None):
                self._data = self.to_representation(self.validated_data)
            else:
                self._data = self.get_initial()

        return self._data

    @property
    def protobuf(self):
        """
        Returns the serialized data on the serializer.

        :see: https://www.django-rest-framework.org/api-guide/serializers/#data
        """
        self._protobuf = self.to_representation(self.validated_data)
        protobuf_list = []
        for data in self._protobuf:
            protobuf_list.append(self.to_protobuf(data))

        return protobuf_list

    @property
    def errors(self):
        if not hasattr(self, '_errors'):
            msg = 'You must call `.is_valid()` before accessing `.errors`.'
            raise AssertionError(msg)
        return self._errors

    @property
    def validated_data(self):
        if not hasattr(self, '_validated_data'):
            msg = 'You must call `.is_valid()` before accessing `.validated_data`.'
            raise AssertionError(msg)
        return self._validated_data


class ListSerializer(BaseSerializer):
    """
    Serializer for list of objects.
    """

    child = None
    many = True

    def __init__(self, *args, **kwargs):
        self.child = kwargs.pop('child', copy.deepcopy(self.child))
        super().__init__(*args, **kwargs)
        # Bind child to self.
        self.child.bind(field_name='', parent=self)

    def get_initial(self):
        if hasattr(self, 'initial_data'):
            return self.to_representation(self.initial_data)
        return []

    def to_internal_value(self, data):
        ret = []
        errors = []
        for item in data:
            try:
                validated = self.child.run_validation(item)
            except ValidationError as exc:
                errors.append(exc.detail)
            else:
                ret.append(validated)
                errors.append({})

        if any(errors):
            raise ValidationError(errors)

        return ret

    def to_representation(self, data):
        return [self.child.to_representation(item) for item in data]

    def to_protobuf(self, data):
        return self.child.to_protobuf(data)

    def validate(self, attrs):
        return attrs

    def run_validation(self, data=Empty):
        """
        We override the default `run_validation`, making it transparent to the user.
        """
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        value = self.to_internal_value(data)
        try:
            value = self.validate(value)
            assert value is not None, '.validate() should return the validated data'
        except ValidationError:
            raise ValidationError('Validation error')

        return value

    def is_valid(self):
        """
        This implementation is the same as the default, but we use lists as default data instead of dicts.
        """
        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = []
                self._errors = exc.detail
            else:
                self._errors = []

        return not bool(self._errors)

    @property
    def data(self):
        ret = super().data
        return ReturnList(ret, serializer=self)

    @property
    def errors(self):
        ret = super().errors
        if isinstance(ret, dict):
            return ReturnDict(ret, serializer=self)
        return ReturnList(ret, serializer=self)

    @property
    def protobuf(self):
        ret = super().protobuf
        return ReturnList(ret, serializer=self)


class Serializer(BaseSerializer, metaclass=SerializerMetaclass):

    @cached_property
    def fields(self):
        fields = BindingDict(self)
        for key, value in self.get_fields().items():
            fields[key] = value
        return fields

    @property
    def _readable_fields(self):
        for field in self.fields.values():
            yield field

    def get_fields(self):
        """
        Returns a dictionary of {field_name: field_instance}.
        """
        return copy.deepcopy(self._declared_fields)


    def get_initial(self):
        if hasattr(self, 'initial_data'):
            return dict([
                (field_name, field.get_value(self.initial_data))
                for field_name, field in self.fields.items()
                if (field.get_value(self.initial_data) is not Empty)
            ])

        return dict([
            (field.field_name, field.get_initial())
            for field in self.fields.values()
        ])

    def to_internal_value(self, data):
        ret = dict()
        errors = dict()
        fields = self._readable_fields

        for field in fields:
            clean_method = getattr(self, 'clean_' + field.field_name, None)
            primitive_value = field.get_value(data, self)
            try:
                validated_value = field.run_validation(primitive_value)
                if clean_method:
                    validated_value = clean_method(primitive_value)
            except ValidationError as e:
                errors[field.field_name] = 'ERROR: ' + str(e)
            else:
                set_value(ret, field.attributes, validated_value)

        return ret

    def to_representation(self, instance):
        ret = {}
        fields = self._readable_fields
        for field in fields:
            attribute = field.get_attribute(instance)
            key = field.proto_field if field.proto_field else field.field_name
            if attribute is None:
                ret[key] = None
            else:
                ret[key] = field.to_representation(attribute)
        return ret

    def to_protobuf(self, data):
        if self.pb:
            return mongo_to_protobuf(data, self.pb)
        return self.pb

    def __iter__(self):
        for field in self.fields.values():
            yield field

    def __getitem__(self, key):
        field = self.fields[key]
        value = self.data.get(key)
        error = self.errors.get(key) if hasattr(self, '_errors') else None
        if isinstance(field, Serializer):
            return NestedBoundField(field, value, error)
        return BoundField(field, value, error)

    # Include a backlink to the serializer class on return objects.
    # Allows renderers such as HTMLFormRenderer to get the full field info.

    @property
    def data(self):
        ret = super().data
        return ReturnDict(ret, serializer=self)

    @property
    def errors(self):
        ret = super().errors
        return ReturnDict(ret, serializer=self)
