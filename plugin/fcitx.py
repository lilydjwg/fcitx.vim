import vim
import functools

import dbus

class FcitxComm:
  def __init__(self):
    self.bus = bus = dbus.SessionBus()
    obj = bus.get_object('org.fcitx.Fcitx5', '/controller')
    self.fcitx = dbus.Interface(obj, dbus_interface='org.fcitx.Fcitx.Controller1')
    self._rime = None

  def status(self):
    return self.fcitx.State() == 2

  def activate(self):
    self.fcitx.Activate()

  def deactivate(self):
    self.fcitx.Deactivate()

  def current(self):
    im = self.fcitx.CurrentInputMethod()
    if im == 'rime':
      return self._get_rime().GetCurrentSchema()
    else:
      return im

  def _get_rime(self):
    if self._rime is None:
      obj = self.bus.get_object('org.fcitx.Fcitx5', '/rime')
      self._rime = dbus.Interface(obj, dbus_interface='org.fcitx.Fcitx.Rime1')
    return self._rime

class FcitxRimeComm:
  def __init__(self):
    bus = dbus.SessionBus()
    obj = bus.get_object('org.fcitx.Fcitx5', '/rime')
    self.fcitx = dbus.Interface(obj, dbus_interface='org.fcitx.Fcitx.Rime1')

  def status(self):
    return self.fcitx.IsAsciiMode()

  def activate(self):
    self.fcitx.SetAsciiMode(False)

  def deactivate(self):
    self.fcitx.SetAsciiMode(True)

  def current(self):
    return self.fcitx.GetCurrentSchema()

try:
  if vim.eval('get(g:, "fcitx5_rime")') == '1':
    FcitxComm = FcitxRimeComm
  Fcitx = FcitxComm()
  fcitx_loaded = True
except dbus.exceptions.DBusException as e:
  if not vim.vars.get('silent_unsupported'):
    vim.command('echohl WarningMsg | echom "fcitx.vim not loaded: %s" | echohl NONE' % e)
  fcitx_loaded = False

def may_reconnect(func):
  @functools.wraps(func)
  def wrapped():
    global Fcitx
    for _ in range(2):
      try:
        return func()
      except Exception as e:
        vim.command('echohl WarningMsg | echom "fcitx.vim: %s: %s" | echohl NONE' % (type(e).__name__, e))
        Fcitx = FcitxComm()
  return wrapped

@may_reconnect
def fcitx2en():
  if Fcitx.status():
    vim.command('let b:inputtoggle = 1')
    Fcitx.deactivate()

@may_reconnect
def fcitx2zh():
  if vim.eval('exists("b:inputtoggle")') == '1':
    if vim.eval('b:inputtoggle') == '1':
      Fcitx.activate()
      vim.command('let b:inputtoggle = 0')
  else:
    vim.command('let b:inputtoggle = 0')

@may_reconnect
def fcitx_current_im():
  return Fcitx.current()
