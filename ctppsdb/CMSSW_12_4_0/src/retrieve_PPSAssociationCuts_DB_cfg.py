##### configuration #####
run_number = 1  # used to select the IOV
db_tag="PPSAssociationCuts_Run3_v1_mc"
#########################

import FWCore.ParameterSet.Config as cms

process = cms.Process("retrievePPSAssociationConfig")

# Message Logger
process.MessageLogger = cms.Service("MessageLogger",
                                    destinations = cms.untracked.vstring('cout'),
                                    cout = cms.untracked.PSet(
                                        threshold = cms.untracked.string('INFO')
                                    )
                                    )


# Load CondDB service
process.load("CondCore.CondDB.CondDB_cfi")
process.CondDB.connect = cms.string( 'frontier://FrontierProd/CMS_CONDITIONS' )

# A data source must always be defined. We don't need it, so here's a dummy one.
process.source = cms.Source("EmptyIOVSource",
                            timetype = cms.string('runnumber'),
                            firstValue = cms.uint64(run_number),
                            lastValue = cms.uint64(run_number),
                            interval = cms.uint64(1)
                            )

# input service
process.PoolDBESSource = cms.ESSource("PoolDBESSource",
                                      process.CondDB,
                                      DumbStat = cms.untracked.bool(True),
                                      toGet = cms.VPSet(cms.PSet(
                                          record = cms.string('PPSAssociationCutsRcd'),
                                          tag = cms.string(db_tag)
                                      )
                                      )
                                      )

# DB object retrieve module
process.retrieve_config = cms.EDAnalyzer("RetrievePPSAssociationCuts",
                                         toGet = cms.VPSet(cms.PSet(
                                             record = cms.string('PPSAssociationCutsRcd'),
                                             data = cms.vstring('PPSAssociationCuts')
                                         )
                                         ),
                                         verbose = cms.untracked.bool(True)
                                         )

process.path = cms.Path(process.retrieve_config)
