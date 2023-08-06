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
        if node.parent:
            dest_file = get_dest_file_from_node(node)
            src_file = Path(source_root, f"{node.name}.md")
            processor(src_file, dest_file)


def process_dest_files(structure: Node, processor: Callable[[Path], None]) -> None:
    for node in PreOrderIter(structure):
        if node.parent:
            dest_file = get_dest_file_from_node(node)
            processor(dest_file)