import FWCore.ParameterSet.Config as cms

# load common code
from Configuration.StandardSequences.Eras import eras
process = cms.Process('directsim', eras.Run3)

# load config
import Validation.CTPPS.simu_config.year_2021_cff as config
process.load("Validation.CTPPS.simu_config.year_2021_cff")
process.ctppsCompositeESSource.periods=[config.profile_2021_default]

process.load('Configuration.EventContent.EventContent_cff')

# minimal logger settings                                                                                                           
process.load("FWCore.MessageService.MessageLogger_cfi")
process.options   = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
)
process.MessageLogger.cerr.FwkReport.reportEvery = 5

# event source         
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring('file:xinput'))

# number of events
process.maxEvents = cms.untracked.PSet(
input = cms.untracked.int32(-1)
)

# override beam-parameter source
process.load("CalibPPS.ESProducers.ctppsBeamParametersFromLHCInfoESSource_cfi")

process.ctppsBeamParametersFromLHCInfoESSource.beamDivX45 = process.ctppsBeamParametersESSource.beamDivX45
process.ctppsBeamParametersFromLHCInfoESSource.beamDivX56 = process.ctppsBeamParametersESSource.beamDivX56
process.ctppsBeamParametersFromLHCInfoESSource.beamDivY45 = process.ctppsBeamParametersESSource.beamDivY45
process.ctppsBeamParametersFromLHCInfoESSource.beamDivY56 = process.ctppsBeamParametersESSource.beamDivY56

process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetX45 = process.ctppsBeamParametersESSource.vtxOffsetX45
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetX56 = process.ctppsBeamParametersESSource.vtxOffsetX56
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetY45 = process.ctppsBeamParametersESSource.vtxOffsetY45
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetY56 = process.ctppsBeamParametersESSource.vtxOffsetY56
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetZ45 = process.ctppsBeamParametersESSource.vtxOffsetZ45
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetZ56 = process.ctppsBeamParametersESSource.vtxOffsetZ56

process.ctppsBeamParametersFromLHCInfoESSource.vtxStddevX = process.ctppsBeamParametersESSource.vtxStddevX
process.ctppsBeamParametersFromLHCInfoESSource.vtxStddevY = process.ctppsBeamParametersESSource.vtxStddevY
process.ctppsBeamParametersFromLHCInfoESSource.vtxStddevZ = process.ctppsBeamParametersESSource.vtxStddevZ

# update settings of beam-smearing module
process.beamDivergenceVtxGenerator.src = cms.InputTag("")
process.beamDivergenceVtxGenerator.srcGenParticle = cms.VInputTag(
#    cms.InputTag("genPUProtons","genPUProtons"),
    cms.InputTag("genParticles")
)

# do not apply vertex smearing again
process.ctppsBeamParametersFromLHCInfoESSource.vtxStddevX = 0
process.ctppsBeamParametersFromLHCInfoESSource.vtxStddevY = 0
process.ctppsBeamParametersFromLHCInfoESSource.vtxStddevZ = 0

# undo CMS vertex shift
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetX45 = +0.2475 * 1E-1
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetY45 = -0.6924 * 1E-1
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetZ45 = -8.1100 * 1E-1

process.out = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('xfileout'),
    outputCommands = process.AODSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

process.out.outputCommands.append('keep *_*_*_*')

# processing path
process.p = cms.Path(
  process.beamDivergenceVtxGenerator
  * process.ctppsDirectProtonSimulation
  * process.reco_local
  * process.ctppsProtons
)

process.outpath = cms.EndPath(process.out)

process.schedule = cms.Schedule(
    process.p,
    process.outpath
)
