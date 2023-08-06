import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.3.0.post143"
version_tuple = (0, 3, 0, 143)
try:
    from packaging.version import Version as V
    pversion = V("0.3.0.post143")
except ImportError:
    pass

# Data version info
data_version_str = "0.3.0.post17"
data_version_tuple = (0, 3, 0, 17)
try:
    from packaging.version import Version as V
    pdata_version = V("0.3.0.post17")
except ImportError:
    pass
data_git_hash = "d5cfe18b6a1fd9cc328afac0ad1394ff5812537f"
data_git_describe = "0.3.0-17-gd5cfe18b"
data_git_msg = """\
commit d5cfe18b6a1fd9cc328afac0ad1394ff5812537f
Merge: 27f67bc4 fe057c87
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Thu Apr 7 14:03:43 2022 +0200

    Merge pull request #503 from Silabs-ArjanB/ArjanB_wfir
    
    Now signaling wfi on RVFI only when its wakeup condition has been met…

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
