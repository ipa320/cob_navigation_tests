#!/bin/bash
mkdir -p ./.tmp
cd ./.tmp
echo "set terminal postscript enhanced mono dashed lw 1 'Helvetica' 14" > gnucmd
echo "set output 'tmp.ps'" >> gnucmd
echo "set autoscale xfixmin" >> gnucmd
echo "set autoscale xfixmax" >> gnucmd
for f in $( ls ../gnuplot ); do
    echo "plot \"../gnuplot/$f\" using 1:2 with linespoints title \"$f\", \"../gnuplot/$f\" using 1:3 with line title \"arithemtic mean for $f\"" >> gnucmd
    echo "plot \"../gnuplot/$f\" using 1:4 with linespoints title \"standard deviation for $f\"" >> gnucmd
done

gnuplot gnucmd
gvfs-open tmp.ps 2>/dev/null
