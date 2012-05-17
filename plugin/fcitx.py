#!/usr/bin/env python3
# vim:fileencoding=utf-8

import os
import vim
import socket
import struct
FCITX_STATUS = struct.pack('i', 0)
FCITX_OPEN   = struct.pack('i', 1 | (1 << 16))
FCITX_CLOSE  = struct.pack('i', 1)
INT_SIZE     = struct.calcsize('i')
fcitxsocketfile = vim.eval('s:fcitxsocketfile')

def fcitxtalk(command=None):
  sock = socket.socket(socket.AF_UNIX)
  try:
    sock.connect(fcitxsocketfile)
  except socket.error:
    vim.command('echohl WarningMsg | echo "fcitx.vim: socket connection error" | echohl NONE')
    return
  try:
    if not command:
      sock.send(FCITX_STATUS)
      return struct.unpack('i', sock.recv(INT_SIZE))[0]
    elif command == 'c':
      sock.send(FCITX_CLOSE)
    elif command == 'o':
      sock.send(FCITX_OPEN)
    else:
      raise ValueError('unknown fcitx command')
  finally:
    sock.close()

def fcitx2en():
  if fcitxtalk() == 2:
    vim.command('let b:inputtoggle = 1')
    fcitxtalk('c')

def fcitx2zh():
  if vim.eval('exists("b:inputtoggle")') == '1':
    if vim.eval('b:inputtoggle') == '1':
      fcitxtalk('o')
      vim.command('let b:inputtoggle = 0')
  else:
    vim.command('let b:inputtoggle = 0')
