Keep and restore fcitx state for each buffer separately when leaving/re-entering insert mode or search mode. Like always typing English in normal mode, but Chinese in insert mode.

D-Bus only works with the same user so this won't work with `sudo vim`. See the `fcitx5-server` branch for an experimental implementation that supports `sudo vim`.

By default, it use python3 and D-Bus to toggle IME state.
If you set `g:fcitx5_remote` to the executable path of `fcitx5-remote` **BEFORE** loading the plugin, it will use `fcitx5-remote` instead of python and D-Bus. In this case, python3 support is optional.

Usually `fcitx5-remote` mode is way faster to start up since Python script need quite some time for the initial load if you don't use any other plugins that load Python. The Python version will be faster while switching.

Base requirements:

* fcitx 5

Requirements for Python mode (`g:fcitx5_remote` is not set):

* Vim with Python 3 compiled in
* The python-dbus package

Requirements for `fcitx5-remote` mode (`g:fcitx5_remote` is set):

* fcitx5-remote

Links:

* [git repo](https://github.com/lilydjwg/fcitx.vim)
* [www.vim.org](https://www.vim.org/scripts/script.php?script_id=3764)

Warning:

1. If you use Vim in terminal, to avoid the Esc delay, please set `'ttimeoutlen'` to 100 or some other value. And check screen's `maptimeout` or tmux's `escape-time` option if you use it too.

在离开或重新进入插入模式或搜索模式时自动记录和恢复每个缓冲区各自的输入法状态，以便在普通模式下始终是英文输入模式，切换回插入模式时恢复离开前的输入法输入模式。

D-Bus 只在同一用户时有效，所以使用 `sudo vim` 时本代码就失效了。在 `fcitx5-server` 分支有一个实验性的版本支持 `sudo vim` 的用法。

本插件默认会使用 Python 3 并通过 D-Bus 来切换输入法状态。
但如果你在加载插件**之前**设置了 `g:fcitx5_remote` 为你已安装的 `fcitx5-remote` 可执行文件的路径，那么本插件会使用它来切换输入法状态；此模式下本插件并不需要 Python 。

如果你没有其他使用 Python 的 Vim 插件，本插件的 Python 模式初始化可能会显著拖慢启动时间；而 `fcitx5-remote` 模式则没有这个问题。Python 模式会在切换时更快。

基本要求：

* fcitx 5

使用 Python 模式的要求（未设置 `g:fcitx5_remote`）：

* 带有 Python 3 支持的 Vim
* python-dbus 包

使用 `fcitx5-remote` 模式的要求（需设置 `g:fcitx5_remote`）：

* fcitx5-remote

链接：

* [git 仓库](https://github.com/lilydjwg/fcitx.vim)
* [www.vim.org](https://www.vim.org/scripts/script.php?script_id=3764)

注意事项:

1. 终端下请设置 Vim `'ttimeoutlen'` 选项为较小值（如100），否则退出插入模式时会有较严重的延迟。同样会造成延迟的还有 screen 的 `maptimeout` 选项以及 tmux 的 `escape-time` 选项。
2. 请在fcitx5-configtool中确认英语是第一个输入法，中文是第二个输入法，rime用户请注意在fcitx5中一定要有两个输入法。
