#!/usr/bin/env bash
# source this file to get bash tab-completion
_otwstests()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    NUM_ARGS=${#COMP_WORDS[@]}
    if test "${NUM_ARGS}" -lt 2 ; then
        opts=$(test-ot-ws --show-completions)
    else
        opts=$(test-ot-ws --show-completions ${COMP_WORDS[*]})
    fi
    if [[ ${cur} == * ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}

complete -F _otwstests test-ot-ws


