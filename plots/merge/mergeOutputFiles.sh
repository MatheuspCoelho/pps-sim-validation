#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc10
cmssw=CMSSW_12_3_0_pre2
scram project $cmssw
cd $cmssw/src/
eval `scramv1 runtime -sh`
scram b -j8
cd -
# replace fullsim <> directsim
sim=$1
#sim=directsim
ppseos=/eos/cms/store/group/phys_pps/sim-validation/${sim}
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
    step=${step}_${2}
fi
list_files=`ls ${ppseos}/${step}/*|awk '{printf("file:%s,",$1)}' | sed -e's/,$//'`
echo $list_files
cmsRun copyPickMerge_cfg.py inputFiles=$list_files outputFile=$outfile
rsync -avPz $outfile $ppseos/$outfile
rm -rf *.*
