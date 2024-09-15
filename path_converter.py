from pathlib import Path, PureWindowsPath

def convert_windows_path_to_wsl(windows_path):
    windows_path = PureWindowsPath(windows_path)
    posix_path = Path(windows_path.drive[0].lower() + windows_path.as_posix()[2:])
    wsl_path = Path('/mnt').joinpath(posix_path)
    return str(wsl_path)