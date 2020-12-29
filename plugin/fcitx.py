import vim
import functools

import dbus

class FcitxComm():
  def __init__(self):
    bus = dbus.SessionBus()
    obj = bus.get_object('org.fcitx.Fcitx5', '/controller')
    self.fcitx = dbus.Interface(obj, dbus_interface='org.fcitx.Fcitx.Controller1')

  def status(self):
    return self.fcitx.State() == 2

  def activate(self):
    self.fcitx.Activate()

  def deactivate(self):
    self.fcitx.Deactivate()

try:
  Fcitx = FcitxComm()
  fcitx_loaded = True
except dbus.exceptions.DBusException as e:
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
