# stay on the xpath

some nice simple wrappers around the excellent libxml2 library

# on majave
to get this working on macos, you may need to install the deve libraries for Majave

cd[Mojave gcc includes for build](https://silvae86.github.io/sysadmin/mac/osx/mojave/beta/libxml2/2018/07/05/fixing-missing-headers-for-homebrew-in-mac-osx-mojave/)

## on catalina -> python3.9
```
brew install libxml2
brew install python3

cd /usr/local/lib/python3.9/site-packages

sudo ln -s /usr/local/Cellar/libxml2/2.9.12/lib/python3.9/site-packages/* .
```

## linux dependencies
```bash
sudo apt-get install libxml2 libxml2-dev
```

## xget.py

gets xpath values from the command line

## xset.py

sets xpath values from the command line

## validate.py

uses libxml2 to validate schemas



