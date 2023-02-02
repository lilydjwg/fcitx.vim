scriptencoding utf-8
" fcitx.vim	remember fcitx's input state for each buffer
" Author:       lilydjwg
" Version:	2.0a
" URL:		https://www.vim.org/scripts/script.php?script_id=3764
" ---------------------------------------------------------------------
" Load Once:
if &cp || exists("g:loaded_fcitx") || (!exists('$DISPLAY') && !exists('$WAYLAND_DISPLAY'))
  finish
endif
let s:keepcpo = &cpo
set cpo&vim

function s:setup_cmd()
  function Fcitx2en()
    let inputstatus = trim(system(g:fcitx5_remote))
    if inputstatus == '2'
      let b:inputtoggle = 1
      call system(g:fcitx5_remote . ' -c')
    endif
  endfunction
  function Fcitx2zh()
    try
      if b:inputtoggle == 1
        call system(g:fcitx5_remote . ' -o')
        let b:inputtoggle = 0
      endif
    catch /inputtoggle/
      let b:inputtoggle = 0
    endtry
  endfunction

  let g:loaded_fcitx = 1
endfunction

" If g:fcitx5_remote is set (to the path to `fcitx5-remove`), use it to toggle IME state.
if exists("g:fcitx5_remote")
  call s:setup_cmd()

" Otherwise, if python3 is available, use python and dbus to toggle IME state.
elseif has('python3')
  try " abort on fail
    exe 'py3file' expand('<sfile>:r') . '.py'
    if py3eval('fcitx_loaded')
      function Fcitx2en()
        py3 fcitx2en()
      endfunction
      function Fcitx2zh()
        py3 fcitx2zh()
      endfunction
      function FcitxCurrentIM()
        return py3eval('fcitx_current_im()')
      endfunction

      let g:loaded_fcitx = 1
    endif
  catch
    if executable('fcitx5-remote')
      let g:fcitx5_remote = 'fcitx5-remote'
      call s:setup_cmd()
    endif
  endtry
endif

" Register autocmd if successfully loaded.
if exists("g:loaded_fcitx")
  if exists('##InsertLeavePre')
    au InsertLeavePre * call Fcitx2en()
  else
    au InsertLeave * call Fcitx2en()
  endif
  au InsertEnter * call Fcitx2zh()
  au CmdlineEnter [/\?] call Fcitx2zh()
  au CmdlineLeave [/\?] call Fcitx2en()
endif

" ---------------------------------------------------------------------
"  Restoration And Modelines:
let &cpo=s:keepcpo
unlet s:keepcpo

" vim: sw=2 :
