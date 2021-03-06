#!/bin/bash

PROJDIR=~/Documents/SummerFellowship/sexose

SEED=7131990

AVIDADIR=$PROJDIR/avida_core
CFGDIR=$PROJDIR/custom_cfgs
WDIR=$PROJDIR/working
RDIR=$PROJDIR/results

cp $AVIDADIR/avida $AVIDADIR/environment.cfg $AVIDADIR/instset-heads-sex.cfg $WDIR
cp $CFGDIR/avida.cfg $CFGDIR/default-heads-sex.org $WDIR
cp $CFGDIR/local_run_events.cfg $WDIR/events.cfg

cd $WDIR

./avida -s $SEED > $PROJDIR/logs/avida_so.log 2> $PROJDIR/logs/avida_err.log

SAVEDIR=$RDIR/$(date "+%m-%d_%H-%M")_control_run
mkdir -p $SAVEDIR
cp $WDIR/data/* $SAVEDIR/

rm -Rf $WDIR/*
growlnotify -m "Control run has finished."
