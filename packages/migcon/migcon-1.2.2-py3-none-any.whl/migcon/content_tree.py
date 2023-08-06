import os
import re

from anytree import Node, RenderTree, PreOrderIter
from markdown_it import MarkdownIt
from pathlib import Path
from typing import Dict


def format_node_name(name: str) -> str:
    # TODO: this is specific to RESERO... need to figure a better way to do this...
    name = re.sub(r'Policy_-_', '', name)
    name = re.sub(r'Playbook_-_', '', name)
    name = re.sub(r'MP\d\._', '', name)
    name = re.sub(r'ML_Platform_', '', name)
    name = re.sub(r'_-_Playbooks', '', name)
    name = re.sub(r'_-_Policies', '', name)
    return name


def _build_content_tree(content: str, source_dir: Path, target_dir: Path) -> Node:
    md = MarkdownIt()
    tokens = md.parse(content)
    structure = []

    tokens = [token for token in tokens
              if token.type == 'inline' and
              token.children and
              token.children[0].type == 'link_open']

    for token in tokens:
        file_stem = token.children[0].attrs['href'].strip().replace('\n', ' ')
        if file_stem.endswith('.md'):
            print(f"Warning: {file_stem} has .md extension")
        structure.append(((token.level // 2) - 1, f'{file_stem}'))

    idx = -1
    root = parent = Node(source_dir)
    root.filepath = target_dir
    root.afile = 'index'
    parents = {
        idx: root
    }
    keys = [idx]
    for element in structure:
        if element[0] <= idx:
            # remove keys from tmp_parent of equal or greater value than the index
            while True:
                key = keys.pop()
                del parents[key]
                if key == element[0]:
                    break
            parent = parents[keys[-1]]

        node = Node(element[1], parent)
        node.filepath = Path(node.parent.filepath, format_node_name(element[1]))
        node.afile = os.path.relpath(node.filepath, target_dir)

        parents[element[0]] = node
        idx = element[0]
        keys.append(idx)
        parent = node
    return root


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
    with open(index, mode='r') as fid:
        content = fid.read()
    return _build_content_tree(content, source_dir, target_dir)


def print_tree(root: Node):
    for pre, fill, node in RenderTree(root):
        print(f"{pre}{node.name}")


def generate_replacement_dictionary(doc_tree: Node, target_root_dir: Path) -> Dict[str, str]:
    """
    Generate a dictionary that maps flat file to structure file
    :param doc_tree: page hierarchy root node
    :return: mapping dictionary
    """
    mapping_dictionary = {}
    for node in PreOrderIter(doc_tree):
        if node.parent:
            mapping_dictionary[node.name] = Path(node.filepath).relative_to(target_root_dir)
    return mapping_dictionary
