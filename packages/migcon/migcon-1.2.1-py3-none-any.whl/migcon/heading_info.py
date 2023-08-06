import re

from pathlib import Path
from typing import Dict

class HeadingInfo:
    level_map: Dict[int, int]
    next_level: int

    def __init__(self, data: str, file: Path):
        self.level_map = {
            1: 1
        }
        self.next_level = 2
        # how many times does "# " appear in the file?
        count = len(re.findall(r'^#\s', data, re.MULTILINE))
        # we have 3 cases:
        # 1. the file has no heading 1s
        # 2. the file has a single heading 1
        # 3. the file has multiple heading 1s
        self.case = 1 if count == 0 else 2 if count == 1 else 3
        if self.case == 1:
            print(f'Warning: {file} has no heading 1s. Not Implemented')
        self.level_1_count = 0

    def get_corrected_level(self, level: int) -> int:
        """
        Get the corrected level for the level found in the data stream
        :param level: the heading level observed
        :return: the corrected level
        """
        if level == 1:
            self.level_1_count += 1
            if self.level_1_count == 2:
                # we've hit the second level 1... any levels that have been corrected up to this point
                # should be ok. From here on out, we need to adjust up one level, so iterate through
                # the level map and add 1 to each level. Also bump the next level up by 1
                for k in self.level_map.keys():
                    self.level_map[k] += 1
                self.next_level += 1
        elif level not in self.level_map:
            self.level_map[level] = self.next_level
            self.next_level += 1
        return self.level_map[level]

    @staticmethod
    def reconcile_heading_levels_in_file(data: str, file: Path) -> str:
        """
        The heading levels exported from confluence sometimes are not consistent, e.g. skipping levels, etc.
        Go through a file line by line and fix up the heading levels
        :param data: the file content
        :param file: the file path of the content
        :return: the fixed up file content
        """
        heading_info = HeadingInfo(data, file)

        lines = data.splitlines()
        new_lines = []

        for line in lines:
            if line.startswith('#'):
                level = line.count('#')
                new_level = heading_info.get_corrected_level(level)
                new_lines.append(f'{"#" * new_level}{line[level:]}')
            else:
                new_lines.append(line)
        return '\n'.join(new_lines) + '\n'
