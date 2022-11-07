#!/bin/sh

# setup cmssw
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc10
cmssw=$2
scram project $cmssw
cd $cmssw/src/
eval `scramv1 runtime -sh`
scram b -j8
# prep config
it=$1
step=step1
cp ../../step1.py .
tag=$4
label=${step}_${tag}
outfile=${label}_${it}.root
xtmin=$5
xtmax=$6
xximin=$7
xximax=$8
xecms=$9
# prep step1
sed -i "s/xfileout/$outfile/g" step1.py
sed -i "s/xseed/$1/g" step1.py
sed -i "s/xevents/$3/g" step1.py
sed -i "s/xtmin/$xtmin/g" step1.py
sed -i "s/xtmax/$xtmax/g" step1.py
sed -i "s/xximin/$xximin/g" step1.py
sed -i "s/xximax/$xximax/g" step1.py
sed -i "s/xecms/$xecms/g" step1.py
# run step1
cmsRun step1.py
basearea=$5
ppseos=${basearea}/fullsim
if [ ! -d "$ppseos/${tag}/${step}" ]; then
    mkdir -p $ppseos/${tag}/${step}
fi
# transfer output files to eos
xrdcp -f $outfile root://eoscms.cern.ch/$ppseos/${tag}/${step}/$outfile

input=${label}_${it}.root
# prep step2
step=step2
cp ../../step2.py .
label=${step}_${tag}
outfile=${label}_${it}.root
sed -i "s?xinput?$input?" step2.py
sed -i "s/xfileout/$outfile/g" step2.py
sed -i "s/xseed/$1/g" step2.py
# run step2
cmsRun step2.py
if [ ! -d "$ppseos/${tag}/${step}" ]; then
    mkdir -p $ppseos/${tag}/${step}
fi
# transfer output files to eos
xrdcp -f $outfile root://eoscms.cern.ch/$ppseos/${tag}/${step}/$outfile

input=${label}_${it}.root
# prep step3
step=step3
cp ../../step3.py .
label=${step}_${tag}
outfile=${label}_${it}.root
sed -i "s?xinput?$input?" step3.py
sed -i "s/xfileout/$outfile/g" step3.py
# run step3
cmsRun step3.py
# prep storage
if [ ! -d "$ppseos/${tag}/${step}" ]; then
    mkdir -p $ppseos/${tag}/${step}
fi
# transfer output files to eos
xrdcp -f $outfile root://eoscms.cern.ch/$ppseos/${tag}/${step}/$outfile
# clean working node
cd ../..
rm -rf CMSSW*
