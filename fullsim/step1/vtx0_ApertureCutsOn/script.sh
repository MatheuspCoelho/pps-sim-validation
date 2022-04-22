#!/bin/sh
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ $6 = "vtx0_ib" ]; then
    export SCRAM_ARCH=slc7_amd64_gcc10
else
    export SCRAM_ARCH=slc7_amd64_gcc900
fi
cmssw=$4
scram project $cmssw
cd $cmssw/src/
eval `scramv1 runtime -sh`
git cms-addpkg SimTransport/PPSProtonTransport
sed -i "/Apertures/s/False/True/g" SimTransport/PPSProtonTransport/python/OpticalFunctionsConfig_cfi.py
scram b -j8
cd -
label=${3}_${6}
outfile=${label}_${1}.root
sed -i "s/xfileout/$outfile/g" $2
sed -i "s/xseed/$1/g" $2
sed -i "s/xevents/$5/g" $2
echo "***"
echo "Running with ${2}"
echo "***"
cmsRun $2
ppseos=/eos/cms/store/group/phys_pps/sim-validation/fullsim
if [ ! -d "$ppseos/${label}" ]; then
    mkdir $ppseos/${label}
fi
rsync -avPz $outfile $ppseos/${label}/$outfile
rm -rf *.*
