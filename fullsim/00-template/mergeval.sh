#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc10
cmssw=$3
scram project $cmssw
cd $cmssw/src/
eval `scramv1 runtime -sh`
# replace fullsim <> directsim
sim=$1
basearea=$4
ppseos=${basearea}/${sim}
outfile=${sim}_${2}.root
if [ $sim == fullsim ]; then
    step=step3
elif [ $sim == directsim ]; then
    step=step4
else:
    echo "Wrong step"
    break
fi
if [ $2 != "" ]; then
    step=${2}/${step}
fi
list_files=`ls ${ppseos}/${step}/*|awk '{printf("file:%s,",$1)}' | sed -e's/,$//'`
echo $list_files
cp ../../merge.py .
cmsRun merge.py inputFiles=$list_files outputFile=$outfile
xrdcp -f $outfile root://eoscms.cern.ch/${ppseos}/${outfile}
# validator
echo "Starting validation procedure"
valid=${sim}_${2}_Validation.root
cp ../../libboost.tar.gz .
tar zxvf libboost.tar.gz
cp ../../validator .
./validator --i ${outfile} --o ${valid} --s ${sim} --y 2022
xrdcp -f ${valid} root://eoscms.cern.ch/${ppseos}/${valid}
cd ../..
rm -rf CMSSW*
