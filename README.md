Keep and restore fcitx state for each buffer separately when leaving/re-entering insert mode or search mode. Like always typing English in normal mode, but Chinese in insert mode.

The branch uses a server-client architecture to support cross-user usage (e.g. `sudo vim`) or even cross-host usages (not implemented yet).

Requires:

* fcitx 5
* Vim with Python 3 compiled in
* The python-dbus package
* Run the `fcitx-status` script as a service

Links:

* [git repo](https://github.com/lilydjwg/fcitx.vim)
* [www.vim.org](https://www.vim.org/scripts/script.php?script_id=3764)

Warning:

1. If you use Vim in terminal, to avoid the Esc delay, please set `'ttimeoutlen'` to 100 or some other value. And check screen's `maptimeout` or tmux's `escape-time` option if you use it too.

在离开或重新进入插入模式或搜索模式时自动记录和恢复每个缓冲区各自的输入法状态，以便在普通模式下始终是英文输入模式，切换回插入模式时恢复离开前的输入法输入模式。

这个分支使用服务端/客户端架构，以便支持跨用户的用法（如 `sudo vim`），甚至是跨主机的用法（尚未实现）。

要求:

* fcitx 5
* 带有 Python 3 支持的 Vim
* python-dbus 包
* 作为服务运行 `fcitx-status` 脚本

链接：

* [git 仓库](https://github.com/lilydjwg/fcitx.vim)
* [www.vim.org](https://www.vim.org/scripts/script.php?script_id=3764)

注意事项:

1. 终端下请设置 Vim `'ttimeoutlen'` 选项为较小值（如100），否则退出插入模式时会有较严重的延迟。同样会造成延迟的还有 screen 的 `maptimeout` 选项以及 tmux 的 `escape-time` 选项。
