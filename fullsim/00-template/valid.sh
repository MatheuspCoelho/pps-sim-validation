#!/bin/bash

# setup cmssw
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc10
cmssw=$3
ecms=$4
scram project $cmssw
cd $cmssw/src/
eval `scramv1 runtime -sh`
# compile validator
cp ../../validator.cc .
libboost=/cvmfs/cms.cern.ch/slc7_amd64_gcc10/external/boost/1.78.0-850e5328ab465746724c19b2301f9b35/lib/
g++ -O3 -o validator validator.cc `root-config --cflags --libs --ldflags` -L$libboost/external/slc7_amd64_gcc10/lib/ -lboost_program_options
# run validator
basearea=$4
ppseos=${basearea}/${1}
./validator --i ${ppseos}/${1}_${2}.root --s ${1} --e $ecms
