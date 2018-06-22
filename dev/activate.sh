#!/bin/bash
dd="$(dirname ${BASH_SOURCE[0]})"
rdd="$(realpath ${dd})"
rd="$(dirname ${rdd})"
export PATH="${PATH}:${rd}"
source "${rdd}/completion.sh"
