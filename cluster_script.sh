#!/bin/bash

WDIR=/state/partition1/$USER/$JOB_NAME-$JOB_ID-$SGE_TASK_ID

# SGE Options
#$ -S /bin/bash
#$ -N sexose
#$ -l h_rt=12:00:00
#$ -t 1-500
#$ -q claus.q@compute-3-10.local,claus.q@compute-3-11.local,claus.q@compute-3-12.local,claus.q@compute-3-13.local,claus.q@compute-3-14.local,claus.q@compute-3-15.local,claus.q@compute-3-16.local,claus.q@compute-3-17.local,claus.q@compute-3-18.local,claus.q@compute-3-19.local,claus.q@compute-3-20.local,claus.q@compute-3-21.local,claus.q@compute-3-5.local,claus.q@compute-3-6.local,claus.q@compute-3-7.local,claus.q@compute-3-8.local,claus.q@compute-3-9.local
#$ -pe serial 2

# Create Working Directory
mkdir -p $WDIR
if [ ! -d $WDIR ]
then
  echo $WDIR not created
  exit
fi
cd $WDIR

SEED=16


# Copy Data and Config Files
cp $HOME/sexose_sim/* .
# Put your Science related commands here

./avida -s $SEED

# Copy Results Back to Home Directory
RDIR=$HOME/finished_sim/$1/sexose-$1-$2-$JOB_ID-$SGE_TASK_ID
mkdir -p $RDIR
cp * $RDIR/. 

# Cleanup 
rm -rf $WDIR

