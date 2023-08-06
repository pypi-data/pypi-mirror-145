import re


def fixup_toc_macro(content, flags = re.DOTALL | re.MULTILINE | re.IGNORECASE):
    # since jupyter-book has a toc for each page when rendering html, we can just remove the toc-macro
    toc_macro = r'<div class="toc-macro.*?>.*?</div>'
    content = re.sub(toc_macro, '', content, 0, flags)
    return content


def fixup_expander(content, flags = re.DOTALL | re.MULTILINE | re.IGNORECASE):
    # replace the expander macro with the dropdown directive from sphinx.panels
    expander = r'<div id="expander-content-.*?class="expand-content">\s*(.*?)\s*</div>'
    content = re.sub(expander, r'\1\n```', content, 0, flags)
    expander = r'<div id="expander-control-.*?class="expand-control">\s*<img.*?/>(.*?)\s*</div>'
    content = re.sub(expander, r'```{dropdown} \1', content, 0, flags)
    expander = r'<div id="expander-.*?class="expand-container">(.*?)\s*</div>'
    content = re.sub(expander, r'\1', content, 0, flags)
    return content


def fixup_multi_column(content, flags = re.DOTALL | re.MULTILINE | re.IGNORECASE):
    patterns = [
        r'<div class="innerCell">\s*(.*?)\s*</div>',
        r'<div class="cell normal" data-type="normal">\s*(.*?)\s*</div>',
        r'<div class="columnLayout single" layout="single">\s*(.*?)\s*</div>',
    ]
    for pattern in patterns:
        content = re.sub(pattern, r'\1', content, 0, flags)
    return content


def fixup_divs(content: str) -> str:
    patterns = [
        r'<div class="content-wrapper">\s*(.*?)\s*</div>',
        r'<div class="content-wrapper">\s*(.*?)\s*</div>',
        r'<div class="table-wrap">\s*(.*?)\s*</div>',
        r'<div class="code panel.*?<div class="CodeContent.*?>\s*(.*?)\s*</div>\s*</div>',
        r'<div>\s*(.*?)\s*</div>',
        r'<div>\s*(.*?)\s*</div>',
        r'<div class="details">\s*(.*?)\s*</div>',
    ]
    flags = re.IGNORECASE | re.DOTALL | re.MULTILINE
    content = fixup_expander(content, flags)
    for pattern in patterns:
        content = re.sub(pattern, r'\1\n', content, 0, flags)
    content = content.replace(u'\xa0', ' ')
    content = fixup_toc_macro(content, flags)
    content = fixup_multi_column(content, flags)
    return content