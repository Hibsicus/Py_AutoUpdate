# -*- coding: utf-8 -*-
import py_regedit
import py_socket
import os

reg = py_regedit.RegEdit(py_regedit.REG_ROOT, py_regedit.REG_PATH, py_regedit.REG_FLAGS)

if reg.checkValueByname('HTCPLAYER'):
    pass
else:
    reg.createValue('HTCPLAYER', "\"" + py_socket.DIRPATH + r"\py_main.exe" + "\"" + " -silent")

print(py_socket.DIRPATH)
print(os.path.realpath(__file__))
soc = py_socket.SocketEdit("127.0.0.1", 2010)
soc.client()
