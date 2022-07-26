#!/bin/sh

# setup cmssw
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc10
cmssw=$4
tar zxfv cmssw-compiled.tar.gz
cd $cmssw/src/
eval `scramv1 runtime -sh`
scramv1 b ProjectRename
vtxfile=IOMC/EventVertexGenerators/python/VtxSmearedParameters_cfi.py
#sed -i "50s/0.0107682/0.00/g" $vtxfile
#sed -i "51s/0.041722/0.00/g"  $vtxfile
#sed -i "52s/0.035748/0.00/g"  $vtxfile
sed -n 50,52p $vtxfile
# prep config
it=$1
config=$2
cp ../../$config .
step=$3
tag=$6
label=${step}_${tag}
outfile=${label}_${it}.root
sed -i "s/xfileout/$outfile/g" $config
sed -i "s/xseed/$1/g" $config
sed -i "s/xevents/$5/g" $config
# run step1
cmsRun $config
# prep storage
ppseos=/eos/cms/store/group/phys_pps/sim-validation/fullsim
if [ ! -d "$ppseos/${tag}/${step}" ]; then
    mkdir -p $ppseos/${tag}/${step}
fi
# transfer output files to eos
xrdcp -f $outfile $ppseos/${tag}/${step}/$outfile
# clean working node
cd ../..
rm -rf CMSSW*
