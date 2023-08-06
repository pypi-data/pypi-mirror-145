import setuptools

setuptools.setup(
    name="mgo_serializer",
    version="0.0.2",
    author='MosyDev',
    author_email='mostafa.uwsgi@gmail.com',
    description='A MongoEngine Serializer to serialize objects from JSON/BSON to JSON and gRPC',
    url='https://github.com/its0x4d/mgo_serializer',
    packages=setuptools.find_packages(),
    license='GPLv3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ]
)
