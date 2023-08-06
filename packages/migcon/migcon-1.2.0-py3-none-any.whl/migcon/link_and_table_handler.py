import re

from markdownify import markdownify as md


# 1. a line starts with and ends with a pipe (we have a complete row)
# 2. a line starts with a pipe but doesn't end with a pipe (we have the start of a row)
# 3. a line doesn't start with a pipe but ends with a pipe (we have the end of a row)
# 4. a line doesn't start with a pipe and doesn't end with a pipe (we have a cell continuation)
# 5. a line consists of just a pipe (assume it is the closing pipe of a row)
def get_table_row_case(line: str) -> int:
    if line == '|':
        return 5
    elif line.startswith('|') and line.endswith('|'):
        return 1
    elif line.startswith('|') and not line.endswith('|'):
        return 2
    elif not line.startswith('|') and line.endswith('|'):
        return 3
    else:
        return 4


def fixup_table_md(content: str) -> str:
    lines = content.strip().split('\n')
    output = []
    for line in lines:
        line = line.strip()
        if line:
            line_case = get_table_row_case(line)
            if line_case == 1 or line_case == 2:
                # we have a complete row, or start of a rowadd it to the output
                output.append(line)
            elif line_case == 3 or line_case == 4:
                # we have a row continuation, append it to the last element of output
                # check to see if the first character is some sort of markdown list delimiter, if so, we need to prepend
                # a <br /> to the line
                if line.startswith('*') or line.startswith('-') or line.startswith('+'):
                    output[-1] += '<br />'
                # check to see if the first characters are a number followed by a period, if so, we need to prepend
                # a <br /> to the line
                elif re.match(r'^\d+\.', line):
                    output[-1] += '<br />'
                else:
                    output[-1] += ' '
                output[-1] += line
            elif line_case == 5:
                # we have a closing pipe, append it to the last element of output
                output[-1] += ' ' + line

    # if the second line contains anything other than '|', ' ' or '-', then we need to add a header row
    if len(output) > 1:
        if len(set(output[1]) - set('| -')) > 0:
            columns = output[0].count('|')
            header0 = '|'
            header1 = '|'
            for i in range(columns - 1):
                header0 += ' |'
                header1 += ' --- |'
            output.insert(0, header1)
            output.insert(0, header0)

    return "\n".join(output)

def convert_remaining_html(content: str) -> str:

    def _convert_to_md(match):
        html_source = match.group(1)
        converted = md(html_source)
        if html_source.startswith("<table"):
            # we are handling tables, ensure that there aren't any new lines that split rows, etc.
            converted = fixup_table_md(converted)
        else:
            # we are handling a link, go ahead and strip newlines
            converted = converted.replace('\n', ' ')
        return converted

    flags = re.IGNORECASE | re.DOTALL | re.MULTILINE

    html_link = r'(<a\s*?href.*?</a>)'
    content = re.sub(html_link, _convert_to_md, content, 0, flags)

    html_table = r'(<table.*?</table>)'
    content = re.sub(html_table, _convert_to_md, content, 0, flags)

    return content
