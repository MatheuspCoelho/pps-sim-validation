#!/bin/bash

# setup cmssw
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc10
cmssw=$3
scram project $cmssw
cd $cmssw/src/
eval `scramv1 runtime -sh`
scram b -j8
# compile validator
cp ../../validator.cc .
g++ -O3 -o validator validator.cc `root-config --cflags --libs --ldflags` -L$CMSSW_RELEASE_BASE/external/slc7_amd64_gcc10/lib/ -lboost_program_options
# run validator
ppseos=/eos/cms/store/group/phys_pps/sim-validation/${1}
./validator --i ${ppseos}/${1}_${2}.root --s ${1} --e 13600
