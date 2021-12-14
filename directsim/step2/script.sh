#!/bin/sh
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc900
cmssw=$4
scram project $cmssw
cd $cmssw/src/
eval `scramv1 runtime -sh`
scram b -j8
cd -
#if [ ! -d "${6}/out" ]; then
#    mkdir ${6}/out
#fi
#if [ ! -d "${6}/err" ]; then
#    mkdir ${6}/err
#fi
#if [ ! -d "${6}/log" ]; then
#    mkdir ${6}/log
#fi 
ppseos=/eos/cms/store/group/phys_pps/sim-validation/directsim
infile=${ppseos}/step1/step1_${1}.root
outfile=${3}_${1}.root
sed -i "s?xinput?$infile?" $2
sed -i "s/xfileout/$outfile/g" $2
cmsRun ${2}
if [ ! -d "$ppseos/${3}" ]; then
    mkdir $ppseos/${3}
fi
rsync -avPz $outfile $ppseos/${3}/$outfile
rm -rf *.*
