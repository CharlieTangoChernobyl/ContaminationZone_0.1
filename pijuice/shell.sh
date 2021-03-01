#!/bin/sh
python ./counter.py & 
print "Counter running" &
python ./src/main.py &
print "PiJuice runnning"