" inkstone: :Inkstone [variant] command
if exists('g:loaded_inkstone')
  finish
endif
let g:loaded_inkstone = 1

command! -nargs=? -bar -complete=customlist,inkstone#Complete
      \ Inkstone call inkstone#Command(<q-args>)
