import sys
import os

class Shortcut():
    def fix_paths(script, folder=None, icon_path=None, icon=None):
    """get absolute paths to

    1.  script
    2.  desktop folder or subfolder (creating if needed)
    3.  icon

    """
    scriptname = os.path.abspath(script)

    dest = os.path.join(get_homedir(), 'Desktop')
    if folder is not None:
        dest = os.path.join(dest, folder)
        if not os.path.exists(dest):
            os.mkdir(dest)

    if icon_path is None:
        _path, _fname = os.path.split(__file__)
        icon_path = os.path.join(_path, 'icons')
    if icon is None:
        icon = 'py'
    ext = '.ico'
    if platform.startswith('darwin'):
        ext = '.icns'
    iconfile = os.path.abspath(os.path.join(icon_path, icon + ext))

    return scriptname, dest, iconfile
