#!/usr/bin/env bash

for i in "${@:3}"
do
	scp $1$i $2
done

