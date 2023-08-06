import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.3.0.post138"
version_tuple = (0, 3, 0, 138)
try:
    from packaging.version import Version as V
    pversion = V("0.3.0.post138")
except ImportError:
    pass

# Data version info
data_version_str = "0.3.0.post12"
data_version_tuple = (0, 3, 0, 12)
try:
    from packaging.version import Version as V
    pdata_version = V("0.3.0.post12")
except ImportError:
    pass
data_git_hash = "28fc1a3f369a18f0faaa840a0fcb7451db52aabc"
data_git_describe = "0.3.0-12-g28fc1a3"
data_git_msg = """\
commit 28fc1a3f369a18f0faaa840a0fcb7451db52aabc
Merge: db37466 a84e73e
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Thu Apr 7 11:43:56 2022 +0200

    Merge pull request #492 from silabs-oysteink/silabs-oysteink_clic-3
    
    Basic CLIC vectoring support

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
