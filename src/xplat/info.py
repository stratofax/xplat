"""
Get information about the current platform, like system, OS, python.
"""

import platform
from typing import Dict, List, Tuple, Union

NOT_FOUND = "(not found)"
STD_COLUMN = 14
WIDE_COLUMN = 28


def get_platform_info() -> str:
    """Get the platform summary string"""
    return platform.platform()


def get_system_info() -> Dict[str, str]:
    """Get system information as a dictionary"""
    sys_info = platform.uname()
    return {label.title(): value for label, value in zip(sys_info._fields, sys_info)}


def get_python_info() -> Dict[str, str]:
    """Get Python information as a dictionary"""
    return {
        "Python Branch": platform.python_branch() or NOT_FOUND,
        "Python Compiler": platform.python_compiler() or NOT_FOUND,
        "Python Implementation": platform.python_implementation() or NOT_FOUND,
        "Python Revision": platform.python_revision() or NOT_FOUND,
        "Python Version": platform.python_version() or NOT_FOUND,
    }


def get_os_specific_info() -> Dict[str, str]:
    """Get OS-specific information as a dictionary"""
    sys_name = platform.system()
    info = {}
    
    if sys_name == "Linux":    # pragma: no cover
        libc_info = platform.libc_ver()
        info["libc Library"] = libc_info[0]
        info["libc Version"] = libc_info[1]
    elif sys_name == "Darwin":    # pragma: no cover
        mac_ver = platform.mac_ver()
        info["macOS Version"] = mac_ver[0]
    elif sys_name == "Windows":   # pragma: no cover
        win_ver = platform.win32_ver()
        iot = "Yes" if platform.win32_is_iot() else "No"
        info.update({
            "Windows Edition": platform.win32_edition(),
            "Windows Release": win_ver[0],
            "Windows Version": win_ver[1],
            "Windows Service Pack": win_ver[2],
            "Windows OS Type": win_ver[3],
            "Windows IoT Edition": iot,
        })
    return info


def get_all_info() -> Dict[str, Union[str, Dict[str, str]]]:
    """Get all platform information as a dictionary"""
    return {
        "platform": get_platform_info(),
        "system": get_system_info(),
        "python": get_python_info(),
        "os_specific": get_os_specific_info()
    }


def add_header(label: str, tab_stop: int = WIDE_COLUMN,
               indent: int = 2, char: str = "-") -> str:
    """Add a header with suffix text and line decorations"""
    padding = char * (tab_stop - len(label))
    return f"\n{char * indent} {label} Information {padding}\n"


def add_row(label: str, value: str, tab_stop: int = STD_COLUMN) -> str:
    """add a two-column row at specified tab stop"""
    padding = " " * (tab_stop - len(label))
    return f"{label}: {padding} {value}\n"


def add_list(two_column_list: list, tab_stop: int = WIDE_COLUMN) -> str:
    """add a list of two-column rows at specified tab stop"""
    new_rows = ""
    for label, property in two_column_list:
        # check for empty strings
        value = property or NOT_FOUND
        new_rows += add_row(label, value, tab_stop)
    return new_rows


def create_platform_report() -> str:
    """
    Create a report of platform information as a string for console output.
    """
    info = get_all_info()
    platform_rpt = ""

    # Platform summary
    platform_rpt += add_header("Platform")
    platform_rpt += f"{info['platform']}\n"

    # System information
    platform_rpt += add_header("System")
    for label, value in info['system'].items():
        platform_rpt += add_row(label, value)

    # Python information
    platform_rpt += add_header("Python")
    python_info = [[k, v] for k, v in info['python'].items()]
    platform_rpt += add_list(python_info)

    # OS-specific information
    if info['os_specific']:
        os_name = platform.system()
        platform_rpt += add_header(os_name)
        for label, value in info['os_specific'].items():
            platform_rpt += add_row(label, value, tab_stop=WIDE_COLUMN)

    return platform_rpt


if __name__ == "__main__":   # pragma: no cover
    """Run the module as a script."""
    print(create_platform_report())
