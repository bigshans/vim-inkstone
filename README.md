# 墨观 Inkstone for Vim / Neovim

A traditional Chinese color theme for Vim and Neovim, ported from
[**墨观 Inkstone**](https://github.com/Konata9/inkstone) — the VS Code theme built
from the 526 colors of [zhongguose.com](https://zhongguose.com/).

Six variants share one hue skeleton, so switching feels like the same painting
under a different light. Every color here is taken straight from the upstream
theme files, so Vim matches the VS Code / Ghostty / Konsole versions byte for byte.

| Variant | Mode | Canvas | Keywords | Strings | Types |
| --- | --- | --- | --- | --- | --- |
| **玄墨 Xuanmo** | dark | `#14131a` | `#da5761` | `#2bae85` | `#d6a01d` |
| **玄墨 Dimmed** | dark | `#19181e` | `#c27c88` | `#69a794` | `#d6a01d` |
| **沧海 Canghai** | dark | `#0d1822` | `#dc5e41` | `#1ba784` | `#c08eaf` |
| **宣纸 Xuanzhi** | light | `#f7f4ed` | `#c34435` | `#1a6840` | `#813c85` |
| **宣纸 Dimmed** | light | `#e9e2d4` | `#894e54` | `#1a6840` | `#525288` |
| **青瓷 Qingci** | light | `#e8f0ec` | `#bc3a46` | `#1a6840` | `#813c85` |

## Features

- Six variants, `dark`/`light` derived from the theme canvas automatically.
- Truecolor when available; every color is otherwise mapped to the nearest
  xterm-256 entry, so it degrades gracefully over ssh/tmux.
- Covers the editor UI and syntax groups (`Normal`, `CursorLine`, `Pmenu`,
  `StatusLine`, `Diff*`, `Diagnostic*`, `Coc*`, `ALE*`, `GitGutter*`, spell
  checking, quickfix, popups…) plus the filetypes people actually stare at
  (markdown, html/css, yaml/json, shell, python, rust, go, java, c/c++, SQL, vim).
- Embedded `:terminal` gets the theme's 16-color ANSI palette.
- Bundled [vim-airline](https://github.com/vim-airline/vim-airline) theme that
  follows the active variant, including the light ones.
- `:Inkstone` command with completion for switching variants at runtime.

## Install

```vim
" vim-plug
Plug 'bigshans/vim-inkstone'
" lazy.nvim
{ 'bigshans/vim-inkstone', priority = 1000, config = function() vim.cmd.colorscheme('inkstone') end }
" packer.nvim
use 'bigshans/vim-inkstone'
" dein.vim
call dein#add('bigshans/vim-inkstone')
```

Or manually: put this directory anywhere in `'runtimepath'` and run
`:colorscheme inkstone`.

```vim
colorscheme inkstone            " default variant (玄墨)
colorscheme inkstone-xuanzhi    " or name a variant explicitly
:Inkstone                       " list variants
:Inkstone canghai               " switch at runtime
```

## Configuration

```vim
let g:inkstone_variant = 'xuanzhi'      " used by :colorscheme inkstone (default 'xuanmo')
let g:inkstone_transparent = 1          " leave the background unset
let g:inkstone_termguicolors = 0        " don't force 'termguicolors'
let g:airline_theme = 'inkstone'        " use the bundled airline theme
```

`:help inkstone` has the full reference.

## How it is generated

`autoload/inkstone.vim` keeps the highlight rules in hand-written Vim script; only
its palette block is generated. `tools/themes/` vendors the upstream
`*-color-theme.json` files, so a rebuild needs nothing but Python 3:

```sh
python3 tools/build.py            # rewrites the palette block from tools/themes/
```

To track a newer upstream release, drop the new JSON files into `tools/themes/`
and rerun the command.

## Credits

- Original theme and palette design: [Konata9/inkstone](https://github.com/Konata9/inkstone) (MIT).
- Colors: [zhongguose.com](https://zhongguose.com/) — 526 traditional Chinese colors.
- This Vim port: derived colors, highlight mapping, airline theme and the
  `:Inkstone` command.

## License

MIT — see [LICENSE](LICENSE).
