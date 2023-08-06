import os

from anytree import Node, RenderTree, PreOrderIter
from markdown_it import MarkdownIt
from pathlib import Path
from typing import Dict


def build_content_tree(source_dir: Path, target_dir: Path) -> Node:
    """
    Parse the index.md file and build the content tree.

    Tree nodes will have two attributes:
    - afile: the name of the file
    - filepath: that file path (relative to root), including file name

    :param source_dir: directory that contains the html to md converted export from Confluence
    :param target_dir: directory that sphinx/jupyter book files will be writen to
    :return: root node of the content tree
    """
    # from the confluence generated embedded list representing page hierarchy
    # parse the markdown and use it to generate a page hierarchy tree
    index = Path(source_dir, 'index.md')
    md = MarkdownIt("commonmark")
    with open(index, mode='r') as fid:
        tokens = md.parse(fid.read())
    structure = []
    process = False
    level = 0
    for token in tokens:
        if token.content == 'Available Pages:':
            process = True
        if process:
            if token.type == 'bullet_list_open':
                level = token.level
            if token.type == "inline" and 'href' in token.children[0].attrs:
                structure.append((level, token.children[0].attrs['href']))
    idx = -1
    parents = {}
    root = parent = None
    keys = []
    for element in structure:
        if element[0] > idx:
            node = Node(element[1], parent)
        else:
            # remove keys from tmp_parent of equal or greater value than the index
            while True:
                key = keys.pop()
                del parents[key]
                if key == element[0]:
                    break
            node = Node(element[1], parents[keys[-1]])
        parents[element[0]] = node
        idx = element[0]
        keys.append(idx)
        parent = node
        if node.parent:
            node.filepath = Path(node.parent.filepath, element[1])
            node.afile = os.path.relpath(node.filepath, target_dir)
        else:
            root = node
            node.filepath = target_dir
            node.afile = node.name
    return root


def print_tree(root: Node):
    for pre, fill, node in RenderTree(root):
        print(f"{pre}{node.name}")


def generate_replacement_dictionary(doc_tree: Node) -> Dict[str, str]:
    """
    Generate a dictionary that maps flat file to structure file
    :param doc_tree: page hierarchy root node
    :return: mapping dictionary
    """
    mapping_dictionary = {}
    for node in PreOrderIter(doc_tree):
        if node.parent:
            mapping_dictionary[node.name] = node.afile
    return mapping_dictionary
