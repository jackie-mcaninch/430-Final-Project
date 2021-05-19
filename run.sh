#!/bin/bash

if [ "$1" == "local1" ]
then
	python local_optimizationv1.py instance${2}.txt
	python visualize.py $2 local1
fi
if [ "$1" == "local2" ]
then
	python local_optimizationv2.py instance${2}.txt
	python visualize.py $2 local2
fi
if [ "$1" == "greedy" ]
then
	python greedy.py instance${2}.txt
	python visualize.py $2 greedy
fi
