import mmap
import os
import re
import shutil

from anytree import Node, PreOrderIter
from migcon.attachment import AttachmentInfo, Attachment, handle_attachment
from migcon.div_fixups import fixup_divs
from migcon.file_processor import process_files, process_dest_files
from migcon.heading_info import HeadingInfo
from migcon.link_and_table_handler import convert_remaining_html as html_convert
from pathlib import Path
from typing import Dict


def get_dest_file_from_node(node: Node) -> Path:
    if node.parent:
        filename = f"{node.filepath.name}.md"
        dest_dir = node.parent.filepath
    else:
        filename = f"{node.name}.md"
        dest_dir = node.filepath
    return Path(dest_dir, filename)


def copy_into_dir_tree(src_dir: Path, structure: Node) -> None:
    """
    Copies the source file into the new directory structure (provided by structure argument)

    :param src_dir: source directory
    :param structure: hierarchy of new directory structure
    """
    def do_it(src_file: Path, dest_file: Path) -> None:
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src_file, dest_file)
    process_files(src_dir, structure, do_it)


def rewrite_links(structure: Node, replacement_files: Dict[str, str]) -> None:
    """
    Rewrites Markdown links based on the new directory structure created by running the conversion
    :param structure: hierarchy of new directory structure
    :param replacement_files: a dictionary of file name (flat) to file name (relative to new root)
    """
    process_dest_files(structure, lambda dest_file: _rewrite_links(dest_file, replacement_files))


def _rewrite_links(file: Path, replacement_files: Dict[str, str]) -> None:
    """
    Rewrites Markdown links based on the new directory structure created by running the conversion
    :param file: source markdown file
    :param replacement_files: a dictionary of file name (flat) to file name (relative to new root)
    """
    def fixup(match) -> str:
        link_target = match.group(1)
        if link_target in replacement_files:
            return f'](/{replacement_files[link_target]})'
        return f']({link_target})'

    with open(file, mode='r+') as input_file:
        data = input_file.read()

    flags = re.IGNORECASE | re.DOTALL | re.MULTILINE
    new, count = re.subn(']\((.*?)\)', fixup, data, 0, flags)

    if count > 0:
        with open(file, mode='w') as output_file:
            output_file.write(new)


def nn_min(x: int, y: int) -> int:
    """
    the non-negative minimum of x and y
    """
    if x < 0:
        return y
    if y < 0:
        return x
    if x < y:
        return x
    return y


def remove_trailing_sections(tree: Node):
    """
    Removes the "extra" sections that are part of the export, e.g. Attachments, Comments, Change History
    :param tree: Root of the target directory tree
    """
    def do_it(dest_file: Path) -> None:
        with dest_file.open(mode='r+') as input_file:
            with mmap.mmap(input_file.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_in:
                offset = mmap_in.rfind(b'<div class="pageSectionHeader">\n\n## Attachments:')
                offset = nn_min(mmap_in.rfind(b'<div class="pageSectionHeader">\n\n## Comments:'), offset)
                offset = nn_min(mmap_in.rfind(b'## Change History'), offset)
            if offset >= 0:
                os.ftruncate(input_file.fileno(), offset)

    process_dest_files(tree, do_it)


def fixup_attachment_references(tree: Node, attachments: Dict[Path, AttachmentInfo], source_root_dir: Path,
                                target_root_dir: Path):
    """
    The export from Confluence results in attachments identified by page_id (directory) and attachment_id (filename).
    Additionally, drawio macros result in an <img> tag with the source drawio deflated and base64 encoded.
    This function replaces the <img> tags with Markdown syntax (e.g. ![](attachment:page_id/attachment_id)),
    using meaningful names for directory and file and using drawio directive when drawio images are encountered.
    :param tree: Content tree
    :param attachments: information about all the source attachments, key: page_name, value: AttachmentInfo
    :param source_root_dir: the root of the source directory tree
    :param target_root_dir: the root directory of the target directory tree
    :return: None
    """
    class Fixup:
        def __init__(self, attachment_info_map: Dict[Path, AttachmentInfo]):
            self.attachment_info_map = attachment_info_map
            self.changed = False
            self.current_file = None

        def prep_file(self, file: Path):
            self.changed = False
            self.current_file = file

        def fixup(self, match):
            self.changed = True
            if match.group(1).startswith('<img src="images/'):
                data = match.group(1).replace('src="images', 'src="/images')
                img_file = match.group(2)
                target_img_file = target_root_dir / img_file
                target_img_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(source_root_dir / img_file, target_img_file)
                return data
            elif match.group(1).find("drawio-diagram-image") != -1:
                data = match.group(2)
                if self.current_file in self.attachment_info_map:
                    attachment_info = self.attachment_info_map[self.current_file]
                else:
                    attachment = Attachment("Unknown", {
                        "(application/vnd.jgraph.mxfile)": [""]
                    })
                    attachment_info = AttachmentInfo("Unknown", self.current_file.stem, {"Unknown": attachment})
                meaningful_name, file_id = handle_attachment(data, attachment_info, source_root_dir, target_root_dir)
                if meaningful_name.endswith('.drawio.xml'):
                    return f'''```{{drawio-image}} {file_id}
```'''
                else:
                    return f'![{meaningful_name}](/{file_id})'
            else:
                # find the attachment_file name in the set of attachments for this page, use the
                # meaningful attachment name for the 'alt text' and the destination file for the
                # path to the image
                img_file = match.group(2)
                attachment_info = self.attachment_info_map[self.current_file]
                for attachment in attachment_info.attachments.values():
                    for files in attachment.files.values():
                        for file in files:
                            if file == img_file:
                                return f'![{attachment.meaningful_name}]' \
                                       f'(/{attachment.destination_file.relative_to(target_root_dir)})'
                # there are a few cases where the conversion to markdown doesn't copy files over.
                # assuming that the source export directory is a peer directory to the markdown root
                # and the markdown source root is a subdirectory of the markdown root, see if we can fish the
                # file out of the original source directory

                if (source_root_dir.parent.parent / source_root_dir.name / img_file).exists():
                    # probably one of the 'download/temp' files; copy it to target directory and
                    # return name of the file
                    img_path = Path(img_file)
                    target_img_file = f"attachments/{self.current_file.stem}/{img_path.name}"
                    shutil.copyfile(source_root_dir.parent.parent / source_root_dir.name / img_file,
                                    target_root_dir / target_img_file)
                    return f'![{img_path.stem}](/{target_img_file})'
                print(f'Warning: Could not find attachment file {img_file} for page {self.current_file}')

    fixup = Fixup(attachments)

    for node in PreOrderIter(tree):
        file = get_dest_file_from_node(node)
        fixup.prep_file(file)
        with file.open(mode='r+') as input_file:
            data = input_file.read()
        flags = re.IGNORECASE | re.DOTALL | re.MULTILINE
        new = re.sub(r'(<img\s*src="(.*?)".*?>)', fixup.fixup, data, 0, flags)
        if fixup.changed:
            with file.open(mode='w') as output_file:
                output_file.write(new)


def fixup_div_tags(tree: Node) -> None:
    """
    Fixup the div tags in the markdown files.
    :param tree: the content root node
    """
    def do_it(dest_file: Path) -> None:
        with dest_file.open(mode='r+') as input_file:
            data = input_file.read()
        new = fixup_divs(data)
        if new != data:
            with dest_file.open(mode='w') as output_file:
                output_file.write(new)

    process_dest_files(tree, do_it)


def convert_remaining_html(tree: Node) -> None:
    """
    Fixup the div tags in the markdown files.
    :param tree: the content root node
    """
    def do_it(dest_file: Path) -> None:
        with dest_file.open(mode='r+') as input_file:
            data = input_file.read()
        new = html_convert(data)
        if new != data:
            with dest_file.open(mode='w') as output_file:
                output_file.write(new)

    process_dest_files(tree, do_it)


def reconcile_heading_levels(tree: Node) -> None:
    """
    The heading levels exported from confluence sometimes are not consistent, e.g. skipping levels, etc.
    Go through a file line by line and fix up the heading levels
    :param tree: the content root node
    :return: None
    """
    def do_it(dest_file: Path) -> None:
        with dest_file.open(mode='r+') as input_file:
            data = input_file.read()
        new = HeadingInfo.reconcile_heading_levels_in_file(data, dest_file)
        if new != data:
            with dest_file.open(mode='w') as output_file:
                output_file.write(new)

    process_dest_files(tree, do_it)
