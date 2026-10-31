scriptencoding utf-8
" vim-lightline theme generated from 墨观 Inkstone // do not edit by hand
" Follows the active inkstone variant; :Inkstone refreshes it automatically.

function! lightline#colorscheme#inkstone#refresh() abort
  let p = inkstone#Palette()

  let s:accents = {
        \ 'normal': p.cursor,
        \ 'insert': p.str,
        \ 'replace': p.keyword,
        \ 'visual': p.type,
        \ 'command': p.warn,
        \ 'terminal': p.info,
        \ }

  let s:p = {
        \ 'inactive': {},
        \ 'tabline': {},
        \ }

  " Paint the mode segment with the mode colour itself, matching the
  " airline theme; the rest of the bar stays on the status-bar surfaces.
  for [mode, accent] in items(s:accents)
    let s:p[mode] = {
          \ 'left': [
          \   [p.bg, accent, 'bold'],
          \   [accent, p.bg_alt],
          \ ],
          \ 'middle': [
          \   [p.lineno_act, p.widget],
          \ ],
          \ 'right': [
          \   [p.bg, accent, 'bold'],
          \   [p.lineno_act, p.widget],
          \ ],
          \ }
  endfor

  let s:p.normal.error = [[p.bg, p.err, 'bold']]
  let s:p.normal.warning = [[p.bg, p.warn, 'bold']]

  let s:p.inactive = {
        \ 'left': [
        \   [p.comment, p.bg_hard],
        \   [p.lineno, p.bg_hard],
        \ ],
        \ 'middle': [
        \   [p.lineno, p.bg_hard],
        \ ],
        \ 'right': [
        \   [p.comment, p.bg_hard],
        \   [p.lineno, p.bg_hard],
        \ ],
        \ }

  let s:p.tabline = {
        \ 'left': [[p.lineno_act, p.bg_alt]],
        \ 'middle': [[p.comment, p.bg_hard]],
        \ 'right': [[p.lineno_act, p.bg_alt]],
        \ 'tabsel': [[p.bg, p.cursor, 'bold']],
        \ }

  let g:lightline#colorscheme#inkstone#palette = lightline#colorscheme#fill(s:p)
endfunction

call lightline#colorscheme#inkstone#refresh()
