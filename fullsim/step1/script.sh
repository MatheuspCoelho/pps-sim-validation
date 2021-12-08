#!/bin/sh
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc900
cmssw=$4
scram project $cmssw
cd $cmssw/src/
eval `scramv1 runtime -sh`
scram b -j8
cd -
mkdir ${6}/out
mkdir ${6}/err
mkdir ${6}/log
outfile=${3}_${1}.root
sed -i "s/xfileout/$outfile/g" $2
sed -i "s/xseed/$1/g" $2
sed -i "s/xevents/$5/g" $2
cmsRun ${2}
ppseos=/eos/cms/store/group/phys_pps/sim-validation/full
rsync -avPz $outfile $ppseos/${3}/$outfile
rm -rf $outfile
