import argparse

from pathlib import Path
from migcon.content_manager import copy_into_dir_tree, rewrite_links, remove_trailing_sections, \
    fixup_attachment_references, fixup_div_tags, convert_remaining_html, reconcile_heading_levels
from migcon.attachment import process_attachments
from migcon.content_tree import build_content_tree, generate_replacement_dictionary
from migcon.toc_generator import JupyterBookTOCGenerator

def main():
    # create an argument parser that accepts to arguments an input directory and an output directory
    parser = argparse.ArgumentParser(description="Convert a Confluence export to Jupyter Book")
    parser.add_argument("input", help="Source Directory (created by Confluence to Markdown)")
    parser.add_argument("output", help="Target directory (will hold migrated Jupyter Book source)")
    args = parser.parse_args()

    source = Path(args.input).expanduser()
    target = Path(args.output).expanduser()
    target.mkdir(parents=True, exist_ok=True)

    # The following needs to take place:
    # 1. Build a content tree from the index.md in the source directory
    # 2. Build a link replacement dictionary from the content tree
    # 3. Generate a _toc.yml file in the target directory from the content tree
    # 4. Copy the markdown files from the source directory into the new directory structure in the target directory
    # 5. Copy the attachments from the source directory into meaningful names in the target directory, including
    #    processing the drawio xml files, e.g. inflate compressed portion into individual files
    # 6. Rewrite the links in the markdown files in the target directory
    # 7. Remove trailing sections of files (## Attachments, ## History, ## Comments)
    # 8. Fixup references to attachments (meaningful names, markdown imagee syntax, drawio directives, etc.)
    # 9. Fixup superfluous <div> tags in the markdown files
    # 10. Convert tables and images to markdown
    # 11. Reconcile heading levels

    tree = build_content_tree(source, target)                           # 1.
    replacements = generate_replacement_dictionary(tree)                # 2.
    JupyterBookTOCGenerator().generate(tree)                            # 3.
    copy_into_dir_tree(source, tree)                                    # 4.
    attachment_info = process_attachments(source, tree)                 # 5.
    rewrite_links(tree, replacements)                                   # 6.
    remove_trailing_sections(tree)                                      # 7.
    fixup_attachment_references(tree, attachment_info, source, target)  # 8.
    fixup_div_tags(tree)                                                # 9.
    convert_remaining_html(tree)                                        # 10.
    reconcile_heading_levels(tree)                                      # 11.


if __name__ == "__main__":
    main()
