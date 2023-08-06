import os.path

path = "/etc/udev/rules.d/99-myrule.rules"
if os.path.isfile(path):
    f = open(path, "w")
    f.write(
        "SUBSYSTEM=='block', ACTION=='add', ENV{DEVTYPE}=='partition',RUN+='/bin/sh -c '/bin/main.pex''"
    )
    f.close

# TOD0 solve PermissionError: [Errno 13] Permission denied:
# resolve path to python folder
