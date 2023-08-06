# Copyright 2021 Benjamin Winger
# Distributed under the terms of the GNU General Public License v3

import os
import re
from collections import defaultdict
from typing import Dict, Generator, List, Optional, TextIO, Tuple, Union


class INI:
    """
    Class for parsing INI files.

    Current Restrictions:
    - key/value pairs must be separated by =
    - keys may not begin or end with whitespace
    - values will have beginning or ending whitespace stripped when returned.
    - Comments will only be ignored if they are on one line, but not
        if they are on the same line as a key/value pair, where they will be treated as part of the value

    Implementation notes:
    - Validation of key/value pairs occurs when data is used, not when the file is read.
    - When replacing keys with duplicates, all old keys will be removed from all sections (in the
      case of duplicate sections),  and the new elements will be inserted in a single block at the
      location of the first old key.
    - Lists returned by the `[]` operator should not be modified, as the underlying data will not change.
    """

    class _Section:
        def __init__(self, ini: "INI", values: List[str]):
            self.values = values
            self.ini = ini

        def __contains__(self, key: str) -> bool:
            try:
                next(self._find_values(key.strip()))
                return True
            except StopIteration:
                return False

        def _find_values(self, key: str) -> Generator[Tuple[int, str], None, None]:
            for index, elem in enumerate(self.values):
                # Ignore empty lines and comments
                if not elem.strip() or elem.strip()[0] in ("#", "["):
                    continue

                if "=" not in elem:
                    raise RuntimeError(f"Unrecognized line {elem}")
                elem_key, value = elem.split("=", 1)
                if elem_key.strip() == key:
                    yield index, value.strip()

        def __getitem__(self, key: str) -> List[str]:
            key = key.strip()
            return [value for index, value in self._find_values(key)]

        def __delitem__(self, key: str):
            values = self._find_values(key)
            for index, _ in reversed(list(values)):
                del self.values[index]

        def __setitem__(self, key: str, values: Union[str, List[str]]):
            oldvalues = list(self._find_values(key))

            if isinstance(values, str):
                values = [values]

            if oldvalues:
                start_index = oldvalues[0][0]
                for index, _ in reversed(oldvalues):
                    del self.values[index]
                for new_value in reversed(values):
                    self.values.insert(start_index, self.format(key, new_value))
            else:
                self.values.extend([self.format(key, value) for value in values])

        def format(self, key: str, value: str) -> str:
            """
            Formats key and value into an entry.

            E.g.
            'key = value\n'
            """
            key = key.strip()
            value = value.strip()
            return f"{key} = {value}" + self.ini.linesep

    def __init__(self, file: Optional[TextIO] = None, *, linesep: str = os.linesep):
        self.section_map: Dict[Optional[str], List[INI._Section]] = defaultdict(list)
        self.sections: List[INI._Section] = []
        self.linesep = linesep
        if file is not None:
            try:
                while True:
                    self._add_section(file)
            except EOFError:
                pass

    def _add_section(self, file: TextIO):
        section_name = None
        values: List[str] = []

        def add():
            section = INI._Section(self, values)
            self.section_map[section_name].append(section)
            self.sections.append(section)

        while True:
            previous_position = file.tell()
            line = file.readline()

            if not line:
                add()
                raise EOFError

            if line.strip().startswith("[") and not values:
                match = re.match(r"\s*\[(.*)\]", line)
                if not match:
                    raise RuntimeError(
                        f"Line {line} should contain a section but it does not"
                    )
                section_name = match.groups()[0]
            if line.strip().startswith("[") and values:
                # Rewind to previous position so that the header
                # can be read by the next section
                file.seek(previous_position)
                break

            values.append(line)

        add()

    def __setitem__(
        self, section_key: Tuple[Optional[str], str], value: Union[str, List[str]]
    ):
        section, key = section_key
        found = False
        if section in self.section_map:
            # Add key to an existing section
            for tmp_section in self.section_map[section]:
                if key in tmp_section:
                    # If the key previously existed, the new value will be in the first location of that key
                    # Once the key has been found, remove matching entries from all other sections
                    if found:
                        del tmp_section[key]
                    else:
                        tmp_section[key] = value
                        found = True
            if not found:
                # If the key did not previously exist, it will be appended to the end of the last section
                self.section_map[section][-1][key] = value
        else:
            # Add new section and insert key
            new_section = INI._Section(self, [f"[{section}]" + self.linesep])
            new_section[key] = value
            self.section_map[section].append(new_section)
            self.sections.append(new_section)

    def __getitem__(
        self, section_key: Tuple[Optional[str], str]
    ) -> Union[None, str, List[str]]:
        section, key = section_key
        results: List[str] = []
        for tmp_section in self.section_map[section]:
            if key in tmp_section:
                results.extend(tmp_section[key])

        if len(results) == 1:
            return results[0]
        if results:
            return results

        return None

    def dump(self) -> str:
        values = []
        for section in self.sections:
            values.extend(section.values)
        return "".join(values)
