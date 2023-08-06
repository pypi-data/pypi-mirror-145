from mgo_serializer import Serializer


def mongo_to_protobuf(data, fields, schema):
    """
    Convert data to protobuf.
    :return: protobuf
    :rtype: object
    """
    protobuf = schema()
    # Convert QuerySet to protobuf object
    for field, cls in fields.items():
        if data and data[field] is not None:
            if not isinstance(cls, Serializer):
                if cls.proto_field:
                    protobuf.__setattr__(cls.proto_field, data[field])
                else:
                    protobuf.__setattr__(field, data[field])
            else:
                if cls.proto_field:
                    protobuf.MergeFrom(schema(**{cls.proto_field: data[field]}))
                else:
                    protobuf.MergeFrom(schema(**{field: data[field]}))

    return protobuf


