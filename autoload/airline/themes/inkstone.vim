scriptencoding utf-8
" vim-airline theme generated from 墨观 Inkstone // do not edit by hand
if exists('g:airline#themes#inkstone#palette')
  finish
endif

function! s:c(hex) abort
  return inkstone#Cterm(a:hex)
endfunction

function! s:mk(fg, bg, attr) abort
  return [a:fg, a:bg, s:c(a:fg), s:c(a:bg), a:attr]
endfunction

function! airline#themes#inkstone#refresh()
  let p = inkstone#Palette()
  let accent = {
        \ 'red': s:mk(p.keyword, p.bg_alt, ''),
        \ 'green': s:mk(p.str, p.bg_alt, ''),
        \ 'yellow': s:mk(p.type, p.bg_alt, ''),
        \ 'orange': s:mk(p.warn, p.bg_alt, ''),
        \ 'blue': s:mk(p.cursor, p.bg_alt, ''),
        \ 'purple': s:mk(p.type, p.bg_alt, ''),
        \ }

  let g:airline#themes#inkstone#palette = {}
  let g:airline#themes#inkstone#palette.accents = accent
  let g:airline#themes#inkstone#palette.accents.bold = ['', '', '', '', 'bold']
  let g:airline#themes#inkstone#palette.accents.italic = ['', '', '', '', 'italic']
  let g:airline#themes#inkstone#palette.accents.none = ['', '', '', '', '']

  let s:B = s:mk(p.lineno_act, p.widget, '')
  let s:Warn = s:mk(p.bg, p.warn, 'bold')
  let s:Err = s:mk(p.bg, p.err, 'bold')

  " the mode section is painted with the mode colour itself, so switching
  " modes changes the bar instead of only recolouring one glyph
  function! s:map_for(a, accent, p) abort
    let s:A = s:mk(a:p.bg, a:accent, 'bold')
    let s:C = s:mk(a:accent, a:p.bg_hard, '')
    let g:airline#themes#inkstone#palette[a:a] = airline#themes#generate_color_map(s:A, s:B, s:C)
    let g:airline#themes#inkstone#palette[a:a].airline_warning = s:Warn
    let g:airline#themes#inkstone#palette[a:a].airline_error = s:Err
  endfunction

  call s:map_for('normal', p.cursor, p)
  call s:map_for('insert', p.str, p)
  call s:map_for('replace', p.keyword, p)
  call s:map_for('visual', p.type, p)

  let s:IA1 = s:mk(p.comment, p.bg_hard, '')
  let s:IA2 = s:mk(p.lineno, p.bg_hard, '')
  let s:IA3 = s:mk(p.lineno, p.bg_hard, '')
  let g:airline#themes#inkstone#palette.inactive = airline#themes#generate_color_map(s:IA1, s:IA2, s:IA3)
  let g:airline#themes#inkstone#palette.inactive.airline_warning = s:mk(p.comment, p.bg_hard, '')
  let g:airline#themes#inkstone#palette.inactive.airline_error = s:mk(p.comment, p.bg_hard, '')

  let g:airline#themes#inkstone#palette.tabline = {
        \ 'airline_tab': s:mk(p.lineno_act, p.bg_alt, ''),
        \ 'airline_tabsel': s:mk(p.bg, p.cursor, 'bold'),
        \ 'airline_tabtype': s:mk(p.fg, p.bg_alt, ''),
        \ 'airline_tabfill': s:mk(p.comment, p.bg_hard, ''),
        \ 'airline_tabmod': s:mk(p.bg, p.type, 'bold'),
        \ 'airline_tabhid': s:mk(p.lineno, p.bg_hard, ''),
        \ }
endfunction

call airline#themes#inkstone#refresh()
