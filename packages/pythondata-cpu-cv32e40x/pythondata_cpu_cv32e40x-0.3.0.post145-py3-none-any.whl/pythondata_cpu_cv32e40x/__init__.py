import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.3.0.post145"
version_tuple = (0, 3, 0, 145)
try:
    from packaging.version import Version as V
    pversion = V("0.3.0.post145")
except ImportError:
    pass

# Data version info
data_version_str = "0.3.0.post19"
data_version_tuple = (0, 3, 0, 19)
try:
    from packaging.version import Version as V
    pdata_version = V("0.3.0.post19")
except ImportError:
    pass
data_git_hash = "ba4c905fbfc31975f93f40bf39611d83b153324e"
data_git_describe = "0.3.0-19-gba4c905f"
data_git_msg = """\
commit ba4c905fbfc31975f93f40bf39611d83b153324e
Merge: d5cfe18b ae3b654d
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Thu Apr 7 14:48:39 2022 +0200

    Merge pull request #505 from Silabs-ArjanB/ArjanB_wfim
    
    minstret rvfi reporting fix for WFI

"""

# Tool version info
tool_version_str = "0.0.post126"
tool_version_tuple = (0, 0, 126)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post126")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
