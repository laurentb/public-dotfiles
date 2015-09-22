# This file is sourced by all *interactive* bash shells on startup.
# This file *should generate no output* or it will break
# the scp and rcp commands.

if [[ $- != *i* ]] ; then
    # Shell is non-interactive.  Be done now!
    return
fi

# stuff common to zsh and bash
[ -f ~/.sh_common ] && . ~/.sh_common

shopt -s cdspell
[ $BASH_VERSINFO -ge 4 ] && shopt -s autocd
[ $BASH_VERSINFO -ge 4 ] && shopt -s globstar

shopt -s checkwinsize


# hande multiline commands as a single command
shopt -s cmdhist

# ignore dangerous commands and duplicates/whitespace
HISTIGNORE='&:[bf]g:exit:*>|*:history*:svn revert*:*rm*-rf*:*rm*-f*'

# history sharing
HISTCONTROL=ignoreboth
shopt -u histappend
PROMPT_COMMAND="history -a; history -c; history -r"

HISTSIZE=9000
HISTFILESIZE=9000

export HISTTIMEFORMAT='%F %T '

if [[ ${EUID} == 0 ]]; then
    PS1='\[\033[01;31m\]\h\[\033[01;34m\] \w \$\[\033[00m\] '
elif [[ -z ${SSH_TTY} && -n ${DISPLAY} ]]; then
    if [[ -n "${USER}" && "${USER}" == "$(logname 2>/dev/null)" ]]; then
        PS1='\[\033[01;30m\]\h\[\033[01;34m\] \w \$\[\033[00m\] '
    else
        PS1='\[\033[01;30m\]\u@\h\[\033[01;34m\] \w \$\[\033[00m\] '
    fi
else
    PS1='\[\033[01;32m\]\u@\h\[\033[01;34m\] \w \$\[\033[00m\] '
fi

export PROMPT_DIRTRIM=3

# disallow redirections (>) to an existing file − use >| to bypass
set -C

[[ ${IN_KRUSADER} ]] && HISTIGNORE="${HISTIGNORE}:cd '*'"

trap 'echo [0m[31mexited with $? ' ERR

