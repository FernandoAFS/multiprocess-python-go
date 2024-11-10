#!/bin/bash

for i in {1..12};
do
    echo "Python results: ${i}"
    perf stat python mp_calc_pi.py $i 2>&1
done

for i in {1..12};
do
    echo "Go results results: ${i}"
    perf stat go run calc_pi.go $i 2>&1
done
