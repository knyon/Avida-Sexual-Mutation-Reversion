#!/bin/bash


# SGE Options
#$ -S /bin/bash
#$ -N avida_sex_control
#$ -t 1-20
#$ -q all.q

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
cp $HOME/avida_exec/* .

# Put your Science related commands here
./avida -s $SGE_TASK_ID >& control_run.log

# Copy Results Back to Home Directory
mkdir -p $RDIR
cp -r $WDIR/data $RDIR/. 

# Cleanup 
rm -rf $WDIR

