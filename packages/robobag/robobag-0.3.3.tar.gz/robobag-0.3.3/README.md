# bag

```bash
# install
pip install robobag

# install protobuf
brew install protobuf

# generate profile_pb2.py
cd robobag
protoc -I=./ --python_out=./ ./profile.proto

# build package
python3 setup.py sdist

# install from local
pip3 install dist/robobag-0.3.2.tar.gz

# publish to pypi
pip install twine
twine upload dist/*

# use as cli
robobag --help
robobag profile -i /path/to/data.bag
robobag extract -i /path/to/data.bag -p /path/to/data.pb.bin  -t /hdmap -f parquet
robobag extract -i /path/to/data.bag -p /path/to/data.pb.bin  -t /camera_front -f mp4
```

## release

- v0.3.3 fix open-cv vulnerability
- v0.3.2 fix unsign int bug in build_pa_field
- v0.3.1
- v0.3.0 add cli
- v0.2.4 init

## type conversion

- [ros bag primitive type](http://wiki.ros.org/action/show/msg?action=show&redirect=ROS%2FMessage_Description_Language)
- [pyarrow data type](https://arrow.apache.org/docs/python/api/datatypes.html)
- [hive type](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=82706456#LanguageManualTypes-bigint)

| primitive type | parquet                                                  | hive sql type                           | comment                               |
| -------------- | -------------------------------------------------------- | --------------------------------------- | ------------------------------------- |
| byte           | pa.int8()                                                | TINYINT                                 | deprecated                            |
| bool           | pa.bool\_()                                              | BOOLEAN                                 |                                       |
| int8           | pa.int8()                                                | TINYINT                                 |                                       |
| uint8          | pa.uint8()                                               | SMALLINT                                | unsign not support                    |
| int16          | pa.int16()                                               | SMALLINT                                |                                       |
| uint16         | pa.uint16()                                              | INT                                     | unsign not support                    |
| int32          | pa.int32()                                               | INT                                     |                                       |
| uint32         | pa.uint32()                                              | BIGINT                                  | unsign not support                    |
| int64          | pa.int64()                                               | BIGINT                                  |                                       |
| uint64         | pa.uint64()                                              | BIGINT                                  | unsign not support, might try decimal |
| float32        | pa.float32()                                             | FLOAT                                   |                                       |
| float64        | pa.float64()                                             | DOUBLE                                  |                                       |
| string         | pa.string()                                              | STRING                                  |                                       |
| time           | pa.struct([("secs", pa.int64()), ('nsecs', pa.int64())]) | STRUCT<`secs`: BIGINT, `nsecs`: BIGINT> |                                       |
| duration       | pa.struct([("secs", pa.int64()), ('nsecs', pa.int64())]) | STRUCT<`secs`: BIGINT, `nsecs`: BIGINT> |                                       |
