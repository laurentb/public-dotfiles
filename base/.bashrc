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

# Make Bash append rather than overwrite the history on disk:
shopt -s histappend

# Whenever displaying the prompt, read new items and write the previous line to disk:
PROMPT_COMMAND='history -n;history -a'
# hande multiline commands as a single command
shopt -s cmdhist

# ignore dangerous commands and duplicates/whitespace
export HISTIGNORE='&:[bf]g:exit:*>|*:history*:svn revert*:*rm*-rf*:*rm*-f*'
HISTCONTROL=ignoreboth

HISTSIZE=3000
HISTFILESIZE=3000

export HISTTIMEFORMAT='%F %T '

# disallow redirections (>) to an existing file − use >| to bypass
set -C

# TODO when not in screen, disable history *writing*
