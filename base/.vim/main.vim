scriptencoding utf-8

filetype off
call pathogen#infect()

" usually these are already defaults in the global vimrc
set nocompatible
set hidden
set ttyfast
set termencoding=utf-8
filetype on
filetype plugin indent on

set background=dark

if (&term !~ 'linux')
    " 256 colors
    set t_Co=256
    colorscheme zenburn
endif

" indentation basics
set tabstop=4
set shiftwidth=4
set expandtab
set autoindent
set smartindent
set softtabstop=4
set smarttab
set backspace=indent,eol,start

" ignore case in searches, unless the pattern is not fully lowercase
" can be ignored with \c or \C in the pattern
set ignorecase smartcase

" clear search hilight
nnoremap <silent> <F10> :nohlsearch<CR>

" autoinsert comment leader
set formatoptions+=ro

" autowrap comments
set formatoptions+=c

" allow virtual editing in Visual block mode
" the cursor can be positioned where there is no actual character
set virtualedit=block

" autocompletion menu
set wildmenu
set wildmode=list:full

" show cursor position
set ruler

set showmatch

" show file format only if not unix
function ShowFileFormatFlag(var)
    if ( a:var != 'unix' )
        return '['.a:var.'] '
    else
        return ''
    endif
endfunction

" always show the statusline
set laststatus=2
set statusline=%<%f%h%m%r\ \ [%n]%=%{ShowFileFormatFlag(&fileformat)}0x%B\ \ %c%V,%l/%L\ %P

" change the statusline color depending on the mode
function! InsertStatuslineColor(mode)
    if a:mode == 'i'
        hi StatusLine ctermbg=108
    elseif a:mode == 'r'
        hi StatusLine ctermbg=174
    else
        hi StatusLine ctermbg=187
    endif
endfunction

if (&t_Co > 255)
    au InsertEnter * call InsertStatuslineColor(v:insertmode)
    au InsertChange * call InsertStatuslineColor(v:insertmode)
    au InsertLeave * hi StatusLine ctermbg=186
endif


" Tell vim to remember certain things when we exit
"  '40 : marks will be remembered for up to 40 previously edited files
"  "2000 : will save up to 2000 lines for each register
"  :200 : up to 200 lines of command-line history will be remembered
"  % : saves and restores the buffer list
"  n... : where to save the viminfo files
set viminfo='40,\"2000,:200,%,n~/.viminfo
set history=200

" when editing a file, always jump to the last cursor position
" (unless the filetype is a commit)
let g:leave_my_cursor_position_alone = 1 " prevent gentoo's similar command
au BufReadPost *
    \ if line("'\"") > 1 && line("'\"") <= line("$") && &ft !~ "commit" |
    \ exe "normal! g`\"" |
    \ endif

" no auto wrap for pentadactyl edits
au BufRead,BufNewFile pentadactyl*.txt set textwidth=0 wrapmargin=0

set list listchars=nbsp:⍽,tab:»·,trail:·,extends:»,precedes:«
set showbreak=»

set writebackup nobackup
set undolevels=2000
set timeoutlen=750
set autowrite " write before make and some other commands

if !filewritable($HOME."/.vim/swp")
    call mkdir($HOME."/.vim/swp", "p")
endif
set directory=~/.vim/swp

let g:localvimrc_ask = 0

" keyboard shortcuts
set pastetoggle=<F11>

function ToggleNumber()
    if (&number)
        set nonumber norelativenumber
        hi LineNr          ctermfg=248   ctermbg=235
    elseif (&relativenumber)
        set norelativenumber number
        hi LineNr          ctermfg=248   ctermbg=235
    else
        set nonumber relativenumber
        hi LineNr          ctermfg=240   ctermbg=235
    endif
endfunction
nmap <silent> <F1> <Esc>:call ToggleNumber()<CR>

function ToggleSpell()
    if (&spell && &spelllang=="en")
        set spelllang=fr
        echo "spell: fr"
    elseif (&spell)
        set nospell
        echo "spell off"
    else
        set spell spelllang=en
        echo "spell: en"
    endif
endfunction
nmap <silent> <F2> <Esc>:call ToggleSpell()<CR>

nnoremap <silent> <F12> :YRShow<CR>

" bépo keyboard layout
source ~/.vim/bepo.vim

" remove trailing spaces, retab…
function! Cleanup()
    %s/\s\+$//e
    retab
    setlocal ff=unix
endfunction
comm! Cleanup call Cleanup()

" create parent directory before writing
augroup BWCCreateDir
    au!
    autocmd BufWritePre * if expand("<afile>")!~#'^\w\+:/' && !isdirectory(expand("%:h")) | execute "silent! !mkdir -p ".shellescape(expand('%:h'), 1) | redraw! | endif
augroup END

let $PAGER=''
let $MANPAGER=''

if filereadable($HOME."/.vim/local.vim")
    source ~/.vim/local.vim
endif

let python_highlight_all = 1
let python_slow_sync = 1

if (&t_Co > 255)
    let g:indent_guides_auto_colors = 0
    let g:indent_guides_guide_size = 1
    let g:indent_guides_start_level = 2
    let g:indent_guides_enable_on_vim_startup = 1
    autocmd VimEnter,Colorscheme * :hi IndentGuidesOdd  guibg=red   ctermbg=236
    autocmd VimEnter,Colorscheme * :hi IndentGuidesEven guibg=green ctermbg=238
endif

" copy/paste from the X clipboard
:com -range Cb :silent :<line1>,<line2>w !xsel -i -b
:com -range Cp :silent :<line1>,<line2>w !xsel -i -p
:com -range Cs :silent :<line1>,<line2>w !xsel -i -s

:com -range Pb :silent :r !xsel -o -b
:com -range Pp :silent :r !xsel -o -p
:com -range Ps :silent :r !xsel -o -s

source ~/.vim/completion.vim
