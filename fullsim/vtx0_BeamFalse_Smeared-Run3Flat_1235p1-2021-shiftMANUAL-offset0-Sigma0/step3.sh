#!/bin/sh

# setup cmssw
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc10
cmssw=$4
scram project $cmssw
cd $cmssw/src/
eval `scramv1 runtime -sh`
scram b -j8
# prep config
it=$1
config=$2
cp ../../$config .
step=$3
tag=$6
ppseos=/eos/cms/store/group/phys_pps/sim-validation/fullsim
prestep=$(echo "$step" | sed -r 's/3/2/g')
input=${prestep}_${tag}_${it}.root
infile=${ppseos}/${tag}/${prestep}/$input
label=${step}_${tag}
outfile=${label}_${it}.root
xrdcp $infile ./$input
sed -i "s?xinput?$input?" $config
sed -i "s/xfileout/$outfile/g" $config
sed -i "s/xseed/$it/g" $config
# run step3
cmsRun $config
# prep storage
if [ ! -d "$ppseos/${tag}/${step}" ]; then
    mkdir -p $ppseos/${tag}/${step}
fi
# transfer output files to eos
xrdcp $outfile $ppseos/${tag}/${step}/$outfile
# clean working node
cd ../..
rm -rf CMSSW*
