from abc import ABC, abstractmethod
from anytree import Node
from anytree.exporter import DictExporter
from pathlib import Path
from yaml import dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class TOCGenerator(ABC):
    @abstractmethod
    def generate(self, doc_structure: Node):
        pass

class JupyterBookTOCGenerator(TOCGenerator):
    def generate(self, doc_structure: Node):
        # this is a bit of a hack, we are using "afile" rather than "file" so it sorts before "children"
        # I tried using an ordered dictionary, but it prints a bunch of extraneous stuff
        dct = DictExporter(attriter=lambda attrs: [(k, v) for k, v in attrs if k == "afile"]).export(doc_structure)
        toc = dump(dct).replace('children:', 'sections:').replace('afile:', 'file:').replace('file:', 'root:', 1)
        # noinspection PyUnresolvedReferences
        with open(Path(doc_structure.filepath, "_toc.yml"), "w") as toc_file:
            toc_file.write("format: jb-article\n")
            toc_file.write(toc)
