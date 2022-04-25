#!/bin/sh
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc900
cmssw=$4
scram project $cmssw
cd $cmssw/src/
eval `scramv1 runtime -sh`
git cms-addpkg Validation/CTPPS
scram b -j8
cd -
ppseos=/eos/cms/store/group/phys_pps/sim-validation/directsim
infile=${ppseos}/step3_standard_xi1/step3_standard_xi1_${1}.root
label=${3}_${6}
outfile=${label}_${1}.root
sed -i "s?xinput?$infile?" $2
sed -i "s/xfileout/$outfile/g" $2
sed -i "s/xseed/$1/g" $2
cmsRun ${2}
if [ ! -d "$ppseos/${label}" ]; then
    mkdir $ppseos/${label}
fi
rsync -avPz $outfile $ppseos/${label}/$outfile
rm -rf *.*
