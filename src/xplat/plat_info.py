"""
Get information about the current platform, like system, OS, python.
"""

import platform

NOT_FOUND = "(not found)"
STD_COLUMN = 14
WIDE_COLUMN = 28


def add_header(label: str, tab_stop: int = WIDE_COLUMN,
               indent: int = 2, char: str = "-") -> str:
    """Add a header with suffix text and line decorations"""
    padding = char * (tab_stop - len(label))
    return f"\n{char * indent} {label} Information {padding}\n"


def add_row(label: str, value: str, tab_stop: int = STD_COLUMN) -> str:
    """add a two-column row at specified tab stop"""
    padding = " " * (tab_stop - len(label))
    return f"{label}: {padding} {value}\n"


def add_list(two_column_list: list, tab_stop=WIDE_COLUMN) -> str:
    new_rows = ""
    for label, property in two_column_list:
        # check for empty strings
        value = property or NOT_FOUND
        new_rows += add_row(label, value, tab_stop)
    return new_rows


# create platform report
def create_platform_report() -> str:

    platform_rpt = add_header("Platform")

    # use platform summary
    platform_summary = platform.platform()
    platform_rpt += f"{platform_summary}\n"

    # get uname data (system, node, release, version, machine)
    platform_rpt += add_header("System")
    # returns named tuple uname
    sys_info = platform.uname()
    # tuple of the named tuple labels
    sys_labels = sys_info._fields
    # zip the two tuples together, title-case the name
    for (label, value) in zip(sys_labels, sys_info):
        platform_rpt += add_row(label.title(), value)

    # get python executable info
    platform_rpt += add_header("Python")

    python_info = [
        ["Python Branch", platform.python_branch()],
        ["Python Compiler", platform.python_compiler()],
        ["Python Implementation", platform.python_implementation()],
        ["Python Revision", platform.python_revision()],
        ["Python Version", platform.python_version()],
    ]

    platform_rpt += add_list(python_info)

    # execute platform-specific code
    sys_name = platform.system()
    if sys_name == "Linux":
        platform_rpt += add_header("Linux")
        # libc_ver is a 2-element tuple
        libc_info = platform.libc_ver()
        platform_rpt += add_row("libc Library",
                                libc_info[0],
                                tab_stop=WIDE_COLUMN)
        platform_rpt += add_row("libc Version",
                                libc_info[1],
                                tab_stop=WIDE_COLUMN)
    elif sys_name == "Darwin":
        platform_rpt += add_header("macOS")
        mac_ver = platform.mac_ver()
        platform_rpt += add_row("macOS Version",
                                mac_ver[0],
                                tab_stop=WIDE_COLUMN)
    elif sys_name == "Windows":
        platform_rpt += add_header("Windows")
        win_ver = platform.win32_ver()
        iot = "Yes" if platform.win32_is_iot() else "No"
        windows_info = [
            ["Windows Edition", platform.win32_edition()],
            ["Windows Release", win_ver[0]],
            ["Windows Version", win_ver[1]],
            ["Windows Service Pack", win_ver[2]],
            ["Windows OS Type", win_ver[3]],
            ["Windows IoT Edition", iot],
        ]
        platform_rpt += add_list(windows_info)
    else:
        if sys_name == "":
            sys_name = NOT_FOUND
        platform_rpt += f"\nUnidentified system name: {sys_name}\n"
    return platform_rpt


if __name__ == "__main__":
    platform_report = create_platform_report()
    print(f"{platform_report}")
