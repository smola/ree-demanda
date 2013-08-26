#!/bin/bash

gnuplot graphs.gnuplot
pushd graphs
for f in *.ps ; do
	convert $f -rotate 90 -background white -flatten  ${f/.ps/.png}
done
popd
