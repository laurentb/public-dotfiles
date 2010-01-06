" hack to have PHP comments behave like C comments
setlocal comments=sO:*\ -,mO:*\ \ ,exO:*/,s1:/*,mb:*,ex:*/,://
setlocal cindent

" Symfony conventions
setlocal tabstop=2
setlocal shiftwidth=2
setlocal expandtab
setlocal softtabstop=2

setlocal makeprg=~/.vim/phplint.sh\ %
setlocal errorformat=%m\ in\ %f\ on\ line\ %l

