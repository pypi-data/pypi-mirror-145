# Copyright 2021 Benjamin Winger
# Distributed under the terms of the GNU General Public License v3

from io import StringIO

from roundtripini import INI


def test_simple_ini():
    """Tests that simple files can be read and written while preserving formatting"""
    file = """
[section]
key = value
other key=other value
"""

    ini = INI(StringIO(file))
    assert ini["section", "key"] == "value"
    assert ini["section", "other key"] == "other value"
    assert ini.dump() == file


def test_ini_modification():
    """Tests that the file can be modified while still preserving formatting"""
    file = """
# Comment

[section]
# Comment
key = value
other key=other value
"""

    changed_file = """
# Comment

[section]
# Comment
key = new value
other key = other value
"""

    ini = INI(StringIO(file))
    ini["section", "key"] = "new value"
    ini["section", "other key"] = "other value"
    assert ini["section", "key"] == "new value"
    assert ini["section", "other key"] == "other value"
    assert ini.dump() == changed_file


def test_simple_duplicate_keys():
    """Tests that duplicate keys are supported"""
    file = """
[section]
key = value
key = value 2
"""

    changed_file = """
[section]
key = value
key = value 2
key = value 3
"""

    ini = INI(StringIO(file))
    assert ini["section", "key"] == ["value", "value 2"]
    ini["section", "key"] = ini["section", "key"] + ["value 3"]
    assert ini["section", "key"] == ["value", "value 2", "value 3"]
    assert ini.dump() == changed_file


def test_simple_duplicate_sections():
    """Tests that duplicate sections are supported"""
    file = """
[section]
key = value

[section]
key = value 2
"""

    changed_file = """
[section]
key = value
key = value 2
key = value 3

[section]
"""

    ini = INI(StringIO(file))
    assert ini["section", "key"] == ["value", "value 2"]
    ini["section", "key"] = ini["section", "key"] + ["value 3"]
    assert ini["section", "key"] == ["value", "value 2", "value 3"]
    assert ini.dump() == changed_file


def test_add_section():
    """Tests that inserting new sections works"""

    file = """
[section]
key = value
"""

    changed_file = """
[section]
key = value
[section 2]
key = value
"""

    ini = INI(StringIO(file))
    ini["section 2", "key"] = "value"
    assert ini["section", "key"] == "value"
    assert ini["section 2", "key"] == "value"
    assert ini.dump() == changed_file
