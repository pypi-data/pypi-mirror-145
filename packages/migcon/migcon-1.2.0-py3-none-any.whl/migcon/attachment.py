import base64
import filecmp
import re
import shutil

from anytree import Node
from dataclasses import dataclass
from migcon.drawio_handler import copy_drawio_file
from migcon.file_dups import find_duplicates
from migcon.file_processor import process_dest_files
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class Attachment:
    """
    A class to hold information about an attachment. With Page attachments in confluence, multiple files
    can share the same name, also with potentially different types, e.g. application/json and application/octet-stream.
    This is modeled by having a dictionary that maps attachment type to a list of file names.
    """
    meaningful_name: str
    files: Dict[str, List[str]]  # key: attachment type, value: list of file names
    destination_file: Path = None
    multiple_copies_warning: bool = False


@dataclass
class AttachmentInfo:
    """
    This class is used to store the information about the attachments, specifically we derive the page id from the
    attachment url string (Path(url).parent.name). As multiple versions of the same file can be attached to a
    confluence page, we keep a dictionary of the "meaningful name" that maps to an attachment
    which holds a list of all file names that are associated to that "attachment".
    """
    page_id: str
    page_name: str
    attachments: Dict[str, Attachment]  # key: meaningful attachment name, value: attachment


def process_attachment(data: str, page_name: str) -> AttachmentInfo:
    pattern = r'## Attachments.*?<div class="greybox" align="left">(.*?)</div>'
    # retrieve the matching string from the pattern
    match = re.search(pattern, data, flags=re.DOTALL | re.MULTILINE | re.IGNORECASE)
    if match:
        attachments_section = match.group(1)
        return _process_attachment(attachments_section, page_name)


def _process_attachment(attachments_section: str, page_name: str) -> AttachmentInfo:
    pattern = '\[(.*?)\]\((.*?)\)\s*?\((.*?)\)'
    # iterate over matches of the pattern
    page_id = "unset"
    attachments = {}
    for match in re.finditer(pattern, attachments_section, flags=re.DOTALL | re.MULTILINE | re.IGNORECASE):
        # extract the meaningful attachment name, file name and attachment type
        att_name = match.group(1).replace(' ', '_').replace('\n', '_')
        att_url = match.group(2)
        att_type = match.group(3)
        page_id = Path(att_url).parent.name
        if att_name in attachments:
            if att_type in attachments[att_name].files:
                attachments[att_name].files[att_type].append(att_url)
            else:
                attachments[att_name].files[att_type] = [att_url]
        else:
            attachments[att_name] = Attachment(att_name, {att_type: [att_url]})
    return AttachmentInfo(page_id, page_name, attachments)


def copy_attachment(source: Path, page_dir: Path, attachment: Attachment, meaningful_name: str, parent_page: Path)\
        -> Tuple[int, int]:
    """
    Copy the attachment to the attachment directory.
    :param source: the source directory
    :param page_dir: the directory to copy the attachment to
    :param attachment: the attachment_obj that holds the attachments to copy
    :param meaningful_name: the name of the attachment
    :param parent_page: the page that the attachment is attached to
    :return: Tuple of (# of files copied, # of files skipped)
    """
    files = []
    for attachment_type, file_paths in attachment.files.items():
        # we will ignore attachment type. The cases we've seen with same name for different types are:
        # application/octet-stream and application/json...
        for file_name in file_paths:
            files.append(source / file_name)
    deduped_files = find_duplicates(files)
    is_drawio = '(application/vnd.jgraph.mxfile)' in attachment.files
    idx = 0
    files_copied = 0
    files_skipped = 0
    for source_file, skipped_files in deduped_files.items():
        files_skipped += len(skipped_files)
        if is_drawio:
            # drawio files are placed in the same directory as the parent page
            dest_file = parent_page.parent / f'{meaningful_name}'
        else:
            dest_file = page_dir / f'{meaningful_name}'
        if idx > 0:
            dest_file = dest_file.parent / f'{dest_file.stem}_{idx}{dest_file.suffix}'
        if dest_file.exists():
            dest_file.unlink()
        if not source_file.exists():
            print(f'Warning: {source_file} does not exist. (Meaningful name: {dest_file})')
            files_skipped += 1
        else:
            files_copied += 1
            if is_drawio:
                dest_file = copy_drawio_file(source_file, dest_file)
            else:
                shutil.copy(source_file, dest_file)
            if attachment.destination_file:
                attachment.multiple_copies_warning = True
            attachment.destination_file = dest_file
            idx += 1
    return files_copied, files_skipped


def process_attachments(source: Path, tree: Node) -> Dict[Path, AttachmentInfo]:
    """
    Gathers information on the attachments for each source page. It is common for Confluence to attach multiple
    copies of the same file (different versions perhaps, but often they are identical). This function will
    aggregate all the attachments for each file, and then return a dictionary of the form:
    {
        <file_path>: <AttachmentInfo>
    }
    as well as copying the attachments from the source directory into the target directory tree with meaningful
    names rather than page id and attachment ids.
    :param source: Root directory of the source files
    :param tree: content tree
    :return: dictionary mapping target files to attachment information
    """
    attachment_dir = tree.filepath / 'attachments'
    attachment_dir.mkdir(exist_ok=True)
    attachments = get_attached_files(tree)
    for parent_page, attachment_info in attachments.items():
        files_copied = 0
        files_skipped = 0
        page_dir = attachment_dir / attachment_info.page_name
        page_dir.mkdir(exist_ok=True)
        for meaningful_name, attachment in attachment_info.attachments.items():
            copied, skipped = copy_attachment(source, page_dir, attachment, meaningful_name, parent_page)
            files_copied += copied
            files_skipped += skipped
        # after copying all attachments, ensure that the same number of files appear in the source and target
        # directories
        source_dir = source / next(iter(next(iter(attachment_info.attachments.values())).files.values()))[0]
        source_dir = source_dir.parent
        source_count = len(list(source_dir.glob('*')))
        dest_count = files_copied + files_skipped
        if source_count != dest_count:
            # If you see this warning, there is another case to add to test_content_manager
            print(f'Warning: {files_copied} files were copied to {page_dir}, and {files_skipped} were skipped '
                  f'due to duplication detection or missing file, but there are {source_count} files in the '
                  f'{source_dir}.')
    return attachments


def get_attached_files(structure: Node) -> Dict[Path, AttachmentInfo]:
    """
    Returns a dictionary of target file paths to attachment information
    :param structure: root of the content tree
    :return: mapping of target file to attachment information for that file
    """
    attached_files = {}

    def do_it(dest_file: Path) -> None:
        if dest_file.is_file():
            page_name = dest_file.stem
            with dest_file.open(mode='r+') as input_file:
                data = input_file.read()
            attachment_info = process_attachment(data, page_name)
            if attachment_info:
                attached_files[dest_file] = attachment_info
    process_dest_files(structure, do_it)

    return attached_files


def handle_attachment(data: str, attachment_info: AttachmentInfo, source_root: Path,
                      target_root: Path) -> Tuple[str, str]:
    # data is likely coming in as base64 encoded string prefixed with 'data:image/png;base64,'
    # verify that's the case... If it isn't, then I'm uncertain what to do, so print a warning and
    # continue...
    if not data.startswith('data:image/png;base64,'):
        print(f"WARNING: data is not base64 encoded: {data[:100]}")
        return "skip", "skip"
    data = base64.b64decode(data[len('data:image/png;base64,'):])

    # create a temporary file and write inflated data str into it
    temp_file = target_root / "attachments/temporary.png"
    with open(temp_file, 'wb') as output_file:
        output_file.write(data)

    # compare the temp file to the contents of the files in attachments that are 'png'
    for attachment in attachment_info.attachments.values():
        if "(image/png)" in attachment.files:
            for file in attachment.files["(image/png)"]:
                if filecmp.cmp(temp_file, source_root / file):
                    # if the file is the same, we don't need to copy it again
                    temp_file.unlink()
                    # TODO: if we find a match with a png file in the attachments, then try to correlate it back to a
                    #  drawio file
                    #  Unfortunately, exact match on contents is not sufficient. For now, leave this as a manual step
                    return attachment.meaningful_name, file
    # if we get here, the file is not the same as any of the files in the attachments, so we need to copy it
    target_dir = target_root / "attachments" / attachment_info.page_name
    target_dir.mkdir(parents=True, exist_ok=True)
    idx = 0
    while True:
        meaningful_name = f"auto_generated_{idx}.png"
        target_file = target_dir / meaningful_name
        if not target_file.exists():
            shutil.copy(temp_file, target_file)
            temp_file.unlink()
            return meaningful_name, str(target_file.relative_to(target_root))
        idx += 1