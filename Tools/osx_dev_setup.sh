#!/usr/bin/bash
# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.
# Installs brew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
# Installs git
brew install git
# OSX has some issues with python and openssl
# this is just to avoid issues in other python projects
brew install openssl
brew install python --with brewed-openssl
# installs pip and then pip installs the required modules
sudo easy_install pip
sudo pip install pycrypto pexpect requests colorama pyreadline readline pyinstaller
