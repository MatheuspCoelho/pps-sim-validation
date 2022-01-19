#!/bin/sh
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc900
cmssw=$4
scram project $cmssw
cd $cmssw/src/
eval `scramv1 runtime -sh`
scram b -j8
cd -
label=${3}_${6}
outfile=${label}_${1}.root
sed -i "s/xfileout/$outfile/g" $2
sed -i "s/xseed/$1/g" $2
sed -i "s/xevents/$5/g" $2
if [ -z "$6" ]; then
    config=$2
else
    config=$2_$6
fi
echo "***"
echo "Running with ${config}"
echo "***"
cmsRun ${config}
ppseos=/eos/cms/store/group/phys_pps/sim-validation/fullsim
if [ ! -d "$ppseos/${label}" ]; then
    mkdir $ppseos/${label}
fi
rsync -avPz $outfile $ppseos/${label}/$outfile
rm -rf *.*
