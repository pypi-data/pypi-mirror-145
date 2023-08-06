import base64
import xml.etree.ElementTree as ETree
import zlib

from pathlib import Path
from urllib.parse import unquote
from xml.dom import minidom


def inflate(data: str) -> str:
    """
    reverses the compression used by draw.io

    see: https://drawio-app.com/extracting-the-xml-from-mxfiles/
    see: https://stackoverflow.com/questions/1089662/python-inflate-and-deflate-implementations

    :param data: base64 encoded string
    :return: "plain text" version of the deflated data
    """
    data = base64.b64decode(data)
    decompress = zlib.decompressobj(-zlib.MAX_WBITS)
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return unquote(inflated.decode('utf-8'))


def copy_drawio_file(source: Path, target: Path) -> Path:
    tree = ETree.parse(source)
    root = tree.getroot()
    data = root.find('diagram').text
    target_file = Path(f"{str(target)}.drawio.xml")
    write_file_from_data(data, target_file)
    return target_file


def write_file_from_data(data: str, target_file: Path) -> None:
    with target_file.open(mode='w+') as output_file:
        output_file.write(minidom.parseString(inflate(data)).toprettyxml(indent="   "))
