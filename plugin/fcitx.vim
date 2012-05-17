scriptencoding utf-8
" fcitx.vim	remember fcitx's input state for each buffer
" Author:       lilydjwg
" Version:	1.1
" URL:		http://www.vim.org/scripts/script.php?script_id=3764
" ---------------------------------------------------------------------
" Load Once:
if &cp || exists("g:loaded_fcitx") || !exists('$DISPLAY') || exists('$SSH_TTY')
  finish
endif
if has("python3")
  let python3 = 1
elseif has("python")
  let python3 = 0
else
  runtime so/fcitx.vim
  finish
endif
let s:keepcpo = &cpo
set cpo&vim
" this is quicker than expand()
let s:fcitxsocketfile = '/tmp/fcitx-socket-' . $DISPLAY
if !filewritable(s:fcitxsocketfile) "try again
  if strridx(s:fcitxsocketfile, '.') > 0
    let s:fcitxsocketfile = strpart(s:fcitxsocketfile, 0,
	  \ strridx(s:fcitxsocketfile, '.'))
  else
    let s:fcitxsocketfile = s:fcitxsocketfile . '.0'
    if !filewritable(s:fcitxsocketfile)
      echohl WarningMsg
      echomsg "socket file of fcitx not found, fcitx.vim not loaded."
      echohl None
      finish
    endif
  endif
endif
let g:loaded_fcitx = 1
let pyfile = expand('<sfile>:r') . '.py'
if python3
  exe 'py3file' pyfile
  au InsertLeave * py3 fcitx2en()
  au InsertEnter * py3 fcitx2zh()
else
  exe 'pyfile' pyfile
  au InsertLeave * py fcitx2en()
  au InsertEnter * py fcitx2zh()
endif
" ---------------------------------------------------------------------
"  Restoration And Modelines:
unlet python3
unlet pyfile
let &cpo=s:keepcpo
unlet s:keepcpo
" vim:fdm=expr:fde=getline(v\:lnum-1)=~'\\v"\\s*-{20,}'?'>1'\:1
