import platform
import subprocess
import os


def check_os(data):
    """ Check if you have Windows env or not
    >>> check_os(platform.system)
    True """
    return True if data.upper() == "WINDOWS" else False


def check_if_32_or_64(arc_tup):
    """ Check what architecture your OS is running
    (32 or 64 bit)
    >>> check_if_32_or_64(platform.architecture())
    64 """
    if arc_tup[0] == "64bit":
        return 64
    elif arc_tup[0] == "32bit":
        return 32
    else:
        return None


def install_pyhook(whl_path):
    """ Install pyhook from the whl files in whls """
    whl_start_name = "pyHook-1.5.1-cp27-cp27m-"
    if check_if_32_or_64(platform.architecture()) == 64:
        whl_end_name = "win_amd64.whl"
    elif check_if_32_or_64(platform.architecture()) == 32:
        whl_end_name = "win32.whl"
    else:
        raise EnvironmentError("Unable to verify the architecture of the system"
                               "exiting..")
    full_whl_path = whl_path + "\\" + whl_start_name + whl_end_name
    pip_command = ["pip", "install", full_whl_path]
    return subprocess.call(pip_command)


def install_pil():
    """ Install PIL from a thirdparty package site """
    pack_name = "PIL"
    dist_url = "https://dist.plone.org/thirdparty/"
    pip_command = ["pip", "install", "--no-index", "-f", dist_url, "-U", pack_name]
    return subprocess.call(pip_command)


def install_py2exe():
    """ Install py2exe from sourceforge """
    source_url = "http://sourceforge.net/projects/py2exe/files/latest/download?source=files"
    pip_command = ["pip", "install", source_url]
    return subprocess.call(pip_command)


def install_other(path):
    """ Install all the """
    filename = "build\\reqs\\win_requirements.txt"
    pip_command = ["pip", "install", "-r", path + filename]
    return subprocess.call(pip_command)


def main():
    """ Main function for the installations """
    if check_os(platform.system()) is True:  # If your OS is Windows
        with open("{}\\build\\text_files\\run.txt".format(os.getcwd()), "a+") as run:
            if run.read().strip() == "false":  # Has it been run before?
                print("Installing required packages for Windows..")
                operating_system = check_os(platform.system())
                if operating_system is True:
                    install_py2exe()
                    install_pil()
                    install_pyhook(os.getcwd() + "build" + "\\" + "whls")
                    install_other(os.getcwd())
                    run.seek(0)
                    run.truncate(0)
                    run.write("true")  # Write 'true' to the file so this won't be run again
                else:
                    pass  # OS is not Windows
            else:
                pass  # Has been run before
    else:  # If your OS is not Windows
        pass


if __name__ == '__main__':
    main()
