" 墨观 Inkstone — entry point.
" Pick a variant with g:inkstone_variant, e.g. let g:inkstone_variant = 'xuanzhi',
" or switch at runtime with :Inkstone xuanzhi
" NB: a nested :colorscheme does nothing, so source via :runtime
if exists('g:inkstone_variant') && get(g:, 'inkstone_variant', '') !=# ''
  execute 'runtime colors/inkstone-' . g:inkstone_variant . '.vim'
else
  runtime colors/inkstone-xuanmo.vim
endif
