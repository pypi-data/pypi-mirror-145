import click
from .bag import Bag
from .message import Message
from pathlib import Path
import json


@click.group()
def cli():
    pass


@click.command()
@click.option('bag_file_path', '-i', '--input', required=True, prompt="Input bag file path", type=click.Path(exists=True))
def profile(bag_file_path):
    fp = Path(bag_file_path)
    with open(fp, "rb") as f:
        bag = Bag(file_obj=f, show_progress=True)
        profile = bag.profile
        profile_json = bag.profile_json
    output_file_path = bag_file_path.replace('.bag', 'pb.bin')

    with open(fp.with_suffix('.pb.bin'), 'wb') as o:
        o.write(profile.SerializeToString())

    with open(fp.with_suffix('.yaml'), 'wb') as o:
        for index, conn in enumerate(profile_json["connection"]):
            if index != 0:
                o.write("\n\n\n\n".encode("utf-8"))

            o.write(("# 定义 %d\n# type = %s\n# topic = %s\n" %
                    (index, conn["type"], conn["topic"])).encode("utf-8"))
            o.write(conn["message_definition"].encode('utf8'))

    with open(fp.with_suffix('.json'), 'w') as o:
        slim_ = dict.copy(profile_json)
        del slim_["chunk"]
        del slim_["chunk_info"]
        for conn in slim_["connection"]:
            del conn['message_definition']
        json.dump(slim_, o, indent=4)


@click.command()
@click.option('bag_file_path', '-i', '--input', required=True, prompt="Input bag file path", type=click.Path(exists=True))
@click.option('bag_profile_path', '-p', '--profile', required=True, prompt="Bag profile path", type=click.Path(exists=True))
@click.option('message_topic', '-t', '--topic', required=True, prompt="Message topic", type=click.STRING)
@click.option('message_format', '-f', '--format', required=True, prompt="Message format", type=click.Choice(['parquet', 'mp4']))
def extract(bag_file_path, bag_profile_path, message_topic, message_format):
    fp = Path(bag_file_path)
    fpp = Path(bag_profile_path)
    mt = "."+message_topic.replace("/", "_")
    with open(fp, "rb") as f:
        with open(fpp, "rb") as p:
            extractor = Message(f, p, show_progress=True)
            topic_data, topic_schema, hql = extractor.read_message(
                message_topic)
            if message_format == "parquet":
                with open(fp.with_suffix(mt+".parquet"), "wb") as o:
                    extractor.save_parquet(topic_data, topic_schema, o)
                with open(fp.with_suffix(mt+".hql"), "w") as o:
                    o.write(hql)
            elif message_format == "mp4":
                extractor.save_mp4(topic_data, topic_schema,
                                   str(fp.with_suffix(mt+".mp4")))


cli.add_command(profile)
cli.add_command(extract)

if __name__ == '__main__':
    cli()
