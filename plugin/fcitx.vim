scriptencoding utf-8
" fcitx.vim	remember fcitx's input state for each buffer
" Author:       lilydjwg
" Version:	2.0a
" URL:		https://www.vim.org/scripts/script.php?script_id=3764
" ---------------------------------------------------------------------
" Load Once:
if &cp || exists("g:loaded_fcitx") || (!exists('$DISPLAY') && !exists('$WAYLAND_DISPLAY')) || !has('python3')
  finish
endif
let s:keepcpo = &cpo
set cpo&vim
let g:loaded_fcitx = 1

try " abort on fail
  exe 'py3file' expand('<sfile>:r') . '.py'
  if py3eval('fcitx_loaded')
    if exists('##InsertLeavePre')
      au InsertLeavePre * if reg_executing() == "" | exec "py3 fcitx2en()" | endif
    else
      au InsertLeave * if reg_executing() == "" | exec "py3 fcitx2en()" | endif
    endif
    au InsertEnter * if reg_executing() == "" | exec "py3 fcitx2zh()" | endif
    au CmdlineEnter [/\?] if reg_executing() == "" | exec "py3 fcitx2zh()" | endif
    au CmdlineLeave [/\?] if reg_executing() == "" | exec "py3 fcitx2en()" | endif
  endif
endtry
" ---------------------------------------------------------------------
"  Restoration And Modelines:
let &cpo=s:keepcpo
unlet s:keepcpo
