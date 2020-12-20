import vim

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

Fcitx = FcitxComm()

def fcitx2en():
  if Fcitx.status():
    vim.command('let b:inputtoggle = 1')
    Fcitx.deactivate()

def fcitx2zh():
  if vim.eval('exists("b:inputtoggle")') == '1':
    if vim.eval('b:inputtoggle') == '1':
      Fcitx.activate()
      vim.command('let b:inputtoggle = 0')
  else:
    vim.command('let b:inputtoggle = 0')
