"Updating a DNS SOA serial number
nnoremap <F8> /\<\d\{10}\><CR>ce<C-r>=strftime("%Y%m%d00")<CR><Esc>:echo @"<CR>
