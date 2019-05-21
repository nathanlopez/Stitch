# Stitch

## :Warning: &nbsp; DISCLAIMER &nbsp; :Warning:

**Stitch is for education/research purposes only.**
<br><br>
The author takes ***NO RESPONSIBILITY*** and/or liability for how you choose to use any of the tools/source code/any files provided.
<br><br>
The author and anyone affiliated with **will not be liable for any losses and/or damages in connection with use of** ***ANY*** **files provided with Stitch**.
<br><br>
By using Stitch or any files included, you understand that you are **AGREEING TO USE AT YOUR OWN RISK**. 
<br>
***Once again Stitch and ALL files included are for EDUCATION and/or RESEARCH purposes ONLY.***
<br><br>
Stitch is *ONLY* intended to be used on your own pentesting labs, or with explicit consent from the owner of the property being tested.

## :information_source: &nbsp; About Stitch &nbsp; :information_source:
A Cross Platform Python Remote Administration Tool:

This is a cross platform python framework which allows you to build custom payloads for Windows, Mac OSX and Linux as well. You are able to select whether the payload binds to a specific IP and port, listens for a connection on a port, option to send an email of system info when the system boots, and option to start keylogger on boot. Payloads created can only run on the OS that they were created on.

### Features
#### :anchor: &nbsp; Cross Platform Support &nbsp; :anchor:
- Command and file auto-completion
- Antivirus detection 
- Able to turn off/on display monitors
- Hide/unhide files and directories
- View/edit the hosts file
- View all the systems environment variables
- Keylogger with options to view status, start, stop and dump the logs onto your host system
- View the location and other information of the target machine 
- Execute custom python scripts which return whatever you print to screen
- Screenshots
- Virtual machine detection
- Download/Upload files to and from the target system
- Attempt to dump the systems password hashes
- Payloads' properties are "disguised" as other known programs

#### :diamond_shape_with_a_dot_inside: &nbsp; Windows Specific &nbsp; :diamond_shape_with_a_dot_inside:
- Display a user/password dialog box to obtain user password
- Dump passwords saved via Chrome
- Clear the System, Security, and Application logs
- Enable/Disable services such as RDP,UAC, and Windows Defender
- Edit the accessed, created, and modified properties of files
- Create a custom popup box
- View connected webcam and take snapshots
- View past connected wifi connections along with their passwords
- View information about drives connected 
- View summary of registry values such as DEP

#### :apple: &nbsp; Mac OSX Specific &nbsp; :apple:
- Display a user/password dialog box to obtain user password
- Change the login text at the user's login screen
- Webcam snapshots

#### :penguin: &nbsp; Mac OSX/Linux Specific &nbsp; :penguin:
- SSH from the target machine into another host
- Run sudo commands
- Attempt to bruteforce the user's password using the passwords list found in Tools/
- Webcam snapshots? (untested on Linux)

### Implemented Transports
All communication between the host and target is AES encrypted. Every Stitch program generates an AES key which is then put into all payloads. To access a payload the AES keys must match. To connect from a different system running Stitch you must add the key by using the showkey command from the original system and the addkey command on the new system. 

### Implemented Payload Installers
The "stitchgen" command gives the user the option to create [NSIS](http://nsis.sourceforge.net/Main_Page) installers on Windows and [Makeself](http://stephanepeter.com/makeself/) installers on posix machines. For Windows, the installer packages the payload and an elevation exe ,which prevents the firewall prompt and adds persistence, and places the payload on the system. For Mac OSX and Linux, the installer places the payload and attempts to add persistence. To create NSIS installers you must [download](http://nsis.sourceforge.net/Download) and install NSIS. 

### Wiki
* [Crash Course of Stitch](https://github.com/nathanlopez/Stitch/wiki/Crash-Course)

### Requirements
- [Python 2.7](https://www.python.org/downloads/)

For easy installation run the following command that corresponds to your OS:
```
# for Windows
pip install -r win_requirements.txt

# for Mac OSX
pip install -r osx_requirements.txt

# for Linux
pip install -r lnx_requirements.txt
```

- [Pycrypto](https://pypi.python.org/pypi/pycrypto)
- [Requests](http://docs.python-requests.org/en/master/)
- [Colorama](https://pypi.python.org/pypi/colorama)
- [PIL](https://pypi.python.org/pypi/PIL)

#### :diamond_shape_with_a_dot_inside: &nbsp; Windows Specific &nbsp; :diamond_shape_with_a_dot_inside:
- [Py2exe](http://www.py2exe.org/)
- [pywin32](https://sourceforge.net/projects/pywin32/)

#### :apple: &nbsp; Mac OSX Specific &nbsp; :diamond_shape_with_a_dot_inside:
- [PyObjC](https://pythonhosted.org/pyobjc/)

#### :penguin: &nbsp; Mac OSX/Linux Specific &nbsp; :diamond_shape_with_a_dot_inside:
- [PyInstaller](http://www.pyinstaller.org/)
- [pexpect](https://pexpect.readthedocs.io/en/stable/)

### :fire: &nbsp; To Run &nbsp; :fire:
```
python main.py
or
./main.py
```

### Motivation
My motivation behind this was to advance my knowledge of python, hacking, and just to see what I could accomplish. Was somewhat discouraged and almost abandoned this project when I found the amazing work done by [n1nj4sec](https://github.com/n1nj4sec/pupy), but still decided to put this up since I had already come so far. 

### Other open-source Python RATs for Reference
* [vesche/basicRAT](https://github.com/vesche/basicRAT)
* [n1nj4sec/pupy](https://github.com/n1nj4sec/pupy)

### Screenshots

![linux options](https://cloud.githubusercontent.com/assets/13227314/21706500/76fdb962-d37c-11e6-9284-093ad065aeca.PNG)
![win_options](https://cloud.githubusercontent.com/assets/13227314/21706517/80d977b4-d37c-11e6-9588-5cd1bb3ecf37.PNG)
![win_upload](https://cloud.githubusercontent.com/assets/13227314/21706518/83c8509e-d37c-11e6-9f6e-f86b3a696c1a.PNG)
![osx_download](https://cloud.githubusercontent.com/assets/13227314/21706506/79f54e96-d37c-11e6-928b-68a8c57df919.PNG)

### License

See [LICENSE](/LICENSE)
