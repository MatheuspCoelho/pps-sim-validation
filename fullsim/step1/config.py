import FWCore.ParameterSet.Config as cms
import math

from Configuration.StandardSequences.Eras import eras
process = cms.Process('SIM',eras.Run3)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC14TeV_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.GeometrySimDB_cff')

process.load('IOMC.EventVertexGenerators.beamDivergenceVtxGenerator_cfi')
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
  generator = cms.PSet(initialSeed = cms.untracked.uint32(10000+0)),
  VtxSmeared= cms.PSet(initialSeed = cms.untracked.uint32(20000+0)),
  LHCTransport=cms.PSet(initialSeed = cms.untracked.uint32(30000+0),
                        engineName = cms.untracked.string('TRandom3')),
  g4SimHits=cms.PSet(initialSeed = cms.untracked.uint32(40000+0)),
  beamDivergenceVtxGenerator=cms.PSet(initialSeed = cms.untracked.uint32(50000+0))
)

process.load('SimG4Core.Application.g4SimHits_cfi')
process.g4SimHits.LHCTransport = cms.bool(True)

process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(500)
        )

process.source = cms.Source("EmptySource",
        firstLuminosityBlock = cms.untracked.uint32(0+1)
)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2021_realistic', '')

# Generator
phi_min = -math.pi
phi_max = math.pi
t_min   = 0.
t_max   = 1.
xi_min  = 0.02
xi_max  = 0.15
ecms = 14000. # ATTENTION: if using HECTOR propagator, currently the energy is hardcoded as 6500 but the optics file is prepared for 7 TeV

process.generator = cms.EDProducer("RandomtXiGunProducer",
        PGunParameters = cms.PSet(
            PartID = cms.vint32(2212),
            MinPhi = cms.double(phi_min),
            MaxPhi = cms.double(phi_max),
            ECMS   = cms.double(ecms),
            Mint   = cms.double(t_min),
            Maxt   = cms.double(t_max),
            MinXi  = cms.double(xi_min),
            MaxXi  = cms.double(xi_max)
            ),
        Verbosity = cms.untracked.int32(0),
        psethack = cms.string('single protons'),
        FireBackward = cms.bool(True),
        FireForward  = cms.bool(True),
        firstRun = cms.untracked.uint32(1),
        )

process.ProductionFilterSequence = cms.Sequence(process.generator)

#################################
process.o1 = cms.OutputModule("PoolOutputModule",
        outputCommands = cms.untracked.vstring('keep *'),
        fileName = cms.untracked.string('step1_0.root')
        )

process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)

process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.outpath = cms.EndPath(process.o1)
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.outpath)

# filter all path with the production filter sequence
for path in process.paths:
    getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq

process.load('SimPPS.Configuration.GenPPS_cff')
from SimTransport.PPSProtonTransport.PPSTransport_cff import LHCTransport
from IOMC.EventVertexGenerators.beamDivergenceVtxGenerator_cfi import *
eras.ctpps.toReplaceWith(process.PPSTransportTask,cms.Task(beamDivergenceVtxGenerator,LHCTransport))

process.LHCTransport.HepMCProductLabel = cms.InputTag('generator','unsmeared')
#process.LHCTransport.HepMCProductLabel = cms.InputTag('beamDivergenceVtxGenerator')

LHCTransport.useBeamPositionFromLHCInfo=cms.bool(True)
# If beamspot to be different from database, then:
#LHCTransport.useBeamPositionFromLHCInfo=cms.bool(False)
#process.load("CalibPPS.ESProducers.ctppsBeamParametersFromLHCInfoESSource_cfi")
#process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetX45 = 0.#1.915e-5
#process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetY45 = 0.#-4.701e-6
#process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetZ45 = 0.#-9.104e-2
