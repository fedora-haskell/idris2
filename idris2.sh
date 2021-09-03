#!/bin/sh

export IDRIS2_PREFIX=@IDRIS2_PREFIX@

${IDRIS2_PREFIX}/bin/idris2 "$@"
