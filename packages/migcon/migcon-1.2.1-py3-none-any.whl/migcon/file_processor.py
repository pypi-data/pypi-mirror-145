from anytree import Node, PreOrderIter
from pathlib import Path
from typing import Callable


def get_dest_file_from_node(node: Node) -> Path:
    if node.parent:
        filename = f"{node.filepath.name}.md"
        dest_dir = node.parent.filepath
    else:
        filename = f"{node.name}.md"
        dest_dir = node.filepath
    return Path(dest_dir, filename)


def process_files(source_root: Path, structure: Node, processor: Callable[[Path, Path], None]) -> None:
    for node in PreOrderIter(structure):
        dest_file = get_dest_file_from_node(node)
        src_rile = Path(source_root, dest_file.name)
        processor(src_rile, dest_file)


def process_dest_files(structure: Node, processor: Callable[[Path], None]) -> None:
    for node in PreOrderIter(structure):
        dest_file = get_dest_file_from_node(node)
        processor(dest_file)