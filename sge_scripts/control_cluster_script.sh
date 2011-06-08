#!/bin/bash


# SGE Options
#$ -S /bin/bash
#$ -N avida_sex_control
#$ -l h_rt=72:00:00
#$ -t 1-20
#$ -q claus.q@compute-3-10.local,claus.q@compute-3-11.local,claus.q@compute-3-12.local,claus.q@compute-3-13.local,claus.q@compute-3-14.local,claus.q@compute-3-15.local,claus.q@compute-3-16.local,claus.q@compute-3-17.local,claus.q@compute-3-18.local,claus.q@compute-3-19.local,claus.q@compute-3-20.local,claus.q@compute-3-21.local,claus.q@compute-3-5.local,claus.q@compute-3-6.local,claus.q@compute-3-7.local,claus.q@compute-3-8.local,claus.q@compute-3-9.local

WDIR=/state/partition1/$USER/$JOB_NAME-$JOB_ID-$SGE_TASK_ID
RDIR=$HOME/avida_sex_control/results/$JOB_NAME-$JOB_ID-$SGE_TASK_ID

# Create Working Directory
mkdir -p $WDIR
if [ ! -d $WDIR ]
then
  echo $WDIR not created
  exit
fi
cd $WDIR


# Copy Data and Config Files
cp $HOME/avida_sex_control/* .

# Put your Science related commands here
./avida -s $SGE_TASK_ID >& $HOME/logs/avida_control.log

# Copy Results Back to Home Directory
mkdir -p $RDIR
cp * $RDIR/. 

# Cleanup 
rm -rf $WDIR

