import FWCore.ParameterSet.Config as cms

# load common code
from Configuration.StandardSequences.Eras import eras
process = cms.Process('directsim', eras.Run3)

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('SimPPS.Configuration.directSimPPS_cff')
process.load('RecoPPS.Configuration.recoCTPPS_cff')

# minimum of logs
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.threshold = cms.untracked.string('')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)

# fix for problematic RP:
process.load("CondCore.CondDB.CondDB_cfi")
process.CondDB.connect = 'frontier://FrontierProd/CMS_CONDITIONS'
process.PoolDBESSource = cms.ESSource("PoolDBESSource",
    process.CondDB,
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('CTPPSPixelAnalysisMaskRcd'),
        tag = cms.string("CTPPSPixelAnalysisMask_Run3_v1_hlt")
    ))
)

# event source         
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring('file:xinput'))

# number of events
process.maxEvents = cms.untracked.PSet(
input = cms.untracked.int32(-1)
)

# update settings of beam-smearing module
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    beamDivergenceVtxGenerator = cms.PSet(initialSeed = cms.untracked.uint32(3849)),
    ppsDirectProtonSimulation = cms.PSet(initialSeed = cms.untracked.uint32(4981))
)

from SimPPS.DirectSimProducer.matching_cff import matchDirectSimOutputsAOD
matchDirectSimOutputsAOD(process)
process.beamDivergenceVtxGenerator.srcGenParticle = cms.VInputTag(
#    cms.InputTag("genPUProtons","genPUProtons"),
    cms.InputTag("genParticles")
)

# do not apply vertex smearing again
process.ctppsBeamParametersFromLHCInfoESSource.vtxStddevX = 0
process.ctppsBeamParametersFromLHCInfoESSource.vtxStddevY = 0
process.ctppsBeamParametersFromLHCInfoESSource.vtxStddevZ = 0

# undo CMS vertex shift
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetX45 = 0. 
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetY45 = 0.
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetZ45 = 0.
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetX56 = 0.
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetY56 = 0.
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetZ56 = 0.

# output configuration
from RecoPPS.Configuration.RecoCTPPS_EventContent_cff import RecoCTPPSAOD
process.out = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('xfileout'),
    outputCommands = RecoCTPPSAOD.outputCommands
)

# processing path
process.p = cms.Path(
    process.directSimPPS
    * process.recoDirectSimPPS
)

process.outpath = cms.EndPath(process.out)

process.schedule = cms.Schedule(
    process.p,
    process.outpath
)
