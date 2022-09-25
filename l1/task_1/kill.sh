#!/usr/bin/env bash
args=""
for arg in "$@"
do
	args+=" $arg"
done
pids=$(pidof $args)
kill $pids
jobs