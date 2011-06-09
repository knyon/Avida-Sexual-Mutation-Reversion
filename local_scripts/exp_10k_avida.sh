#!/bin/bash

PROJDIR=~/Documents/SummerFellowship/sexose

SEED=7131990

AVIDADIR=$PROJDIR/avida_core
CFGDIR=$PROJDIR/custom_cfgs
WDIR=$PROJDIR/working
RDIR=$PROJDIR/results

cp $AVIDADIR/avida $AVIDADIR/default-heads-sex.org $AVIDADIR/environment.cfg $AVIDADIR/instset-heads-sex.cfg $WDIR
cp $CFGDIR/avida.cfg $WDIR
cp $CFGDIR/local_run_events.cfg $WDIR/events.cfg

cd $WDIR

./avida -set REVERT_DETRIMENTAL 1.0 -s $SEED > $PROJDIR/logs/avida_so.log 2> $PROJDIR/logs/avida_err.log

SAVEDIR=$RDIR/$(date "+%m-%d_%H-%M")_exp_run
mkdir -p $SAVEDIR
cp $WDIR/data/* $SAVEDIR/

rm -Rf $WDIR/*
