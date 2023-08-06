import filecmp

from pathlib import Path
from typing import List, Dict


def find_duplicates(files: List[Path]) -> Dict[Path, List[Path]]:
    is_duplicate = set()
    duplicates = {}
    for i in range(len(files)):
        if files[i] not in is_duplicate:
            duplicates[files[i]] = []
            for j in range(i + 1, len(files)):
                if filecmp.cmp(files[i], files[j]):
                    duplicates[files[i]].append(files[j])
                    is_duplicate.add(files[j])
    return duplicates
