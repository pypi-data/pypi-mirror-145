import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.3.0.post147"
version_tuple = (0, 3, 0, 147)
try:
    from packaging.version import Version as V
    pversion = V("0.3.0.post147")
except ImportError:
    pass

# Data version info
data_version_str = "0.3.0.post21"
data_version_tuple = (0, 3, 0, 21)
try:
    from packaging.version import Version as V
    pdata_version = V("0.3.0.post21")
except ImportError:
    pass
data_git_hash = "27524327f31a6bed9fbfcad89f3050ff26144a94"
data_git_describe = "0.3.0-21-g27524327"
data_git_msg = """\
commit 27524327f31a6bed9fbfcad89f3050ff26144a94
Merge: ba4c905f 8a79c59f
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Fri Apr 8 14:05:24 2022 +0200

    Merge pull request #504 from Silabs-ArjanB/ArjanB_wfirdoc
    
    Removed rvfi_sleep and rvfi_wu

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
