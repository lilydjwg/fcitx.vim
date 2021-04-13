import vim
import socket
import struct

fcitxsocketfile = '\0fcitx-status'
fcitx_loaded = False

class FcitxComm(object):
  STATUS     = b'\0'
  ACTIVATE   = b'\1'
  DEACTIVATE = b'\2'

  def __init__(self, socketfile):
    self.socketfile = socketfile
    self.sock = None

  def status(self):
    return self._with_socket(self._status)

  def activate(self):
    self._with_socket(self._command, self.ACTIVATE)

  def deactivate(self):
    self._with_socket(self._command, self.DEACTIVATE)

  def _error(self, e):
    estr = str(e).replace('"', r'\"')
    file = self.socketfile.replace('"', r'\"').replace('\0', '@')
    vim.command('echohl WarningMsg | echo "fcitx.vim: socket %s error: %s" | echohl NONE' % (file, estr))

  def _connect(self):
    self.sock = sock = socket.socket(socket.AF_UNIX)
    sock.settimeout(0.5)
    try:
      sock.connect(self.socketfile)
      return True
    except (socket.error, socket.timeout) as e:
      self.sock = None
      self._error(e)
      return False

  def _with_socket(self, func, *args, **kwargs):
    if not self.sock:
      if not self._connect():
        return

    try:
      return func(*args, **kwargs)
    except (socket.error, socket.timeout, struct.error) as e:
      self.sock = None
      self._error(e)

  def _status(self):
    self.sock.send(self.STATUS)
    return self.sock.recv(1)[0]

  def _command(self, cmd):
    self.sock.send(cmd)

Fcitx = FcitxComm(fcitxsocketfile)

def fcitx2en():
  st = Fcitx.status()
  if st is None:
    return

  if st:
    vim.command('let b:inputtoggle = 1')
    Fcitx.deactivate()

def fcitx2zh():
  if vim.eval('exists("b:inputtoggle")') == '1':
    if vim.eval('b:inputtoggle') == '1':
      Fcitx.activate()
      vim.command('let b:inputtoggle = 0')
  else:
    vim.command('let b:inputtoggle = 0')

fcitx_loaded = True
