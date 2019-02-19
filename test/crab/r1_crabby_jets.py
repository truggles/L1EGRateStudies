import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process("L1Jets",eras.Phase2_trigger)

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(1)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(),
   # fileNames = cms.untracked.vstring(
   #     'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/TT_TuneCUETP8M2T4_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v2/30000/564C271B-9654-E811-9338-90B11C2AA16C.root',
   # ),
   dropDescendantsOfDroppedBranches=cms.untracked.bool(False),
   inputCommands = cms.untracked.vstring(
                    "keep *",
                    "drop l1tEMTFHitExtras_simEmtfDigis_CSC_HLT",
                    "drop l1tEMTFHitExtras_simEmtfDigis_RPC_HLT",
                    "drop l1tEMTFTrackExtras_simEmtfDigis__HLT",
                    "drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT",
                    "drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT",
                    "drop l1tEMTFHit2016s_simEmtfDigis__HLT",
                    "drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT",
                    "drop l1tEMTFTrack2016s_simEmtfDigis__HLT",
                    "drop l1tHGCalTowerMapBXVector_hgcalTriggerPrimitiveDigiProducer_towerMap_HLT",
                    "drop PCaloHits_g4SimHits_EcalHitsEB_SIM",
                    "drop EBDigiCollection_simEcalUnsuppressedDigis__HLT",
                    "drop PCaloHits_g4SimHits_HGCHitsEE_SIM",
                    "drop HGCalDetIdHGCSampleHGCDataFramesSorted_mix_HGCDigisEE_HLT",

   )
)

# All this stuff just runs the various EG algorithms that we are studying
                         
# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '100X_upgrade2023_realistic_v1', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '93X_upgrade2023_realistic_v5', '')

# Choose a 2030 geometry!
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')

# Add HCAL Transcoder
process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
process.load('CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi')




# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1EGCrystal clusters using Emulator

process.load('L1Trigger.L1CaloTrigger.L1EGammaCrystalsEmulatorProducer_cfi')



# --------------------------------------------------------------------------------------------
#
# ----    Produce the calibrated tower collection combining Barrel, HGCal, HF

process.load('L1Trigger/L1CaloTrigger/L1TowerCalibrationProducer_cfi')
process.L1TowerCalibrationProducer.barrelSF = cms.double(4.0)
process.L1TowerCalibrationProducer.hgcalSF = cms.double(1.45)
process.L1TowerCalibrationProducer.hfSF = cms.double(1.2)
#process.L1TowerCalibrationProducer.skipCalibrations = cms.bool(True)



# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1CaloJets with the L1EG clusters as ECAL seeds

process.load('L1Trigger/L1CaloTrigger/L1CaloJetProducer_cfi')
process.L1CaloJetProducer.EtMinForCollection = cms.double(20)


process.pL1Objs = cms.Path( 
    process.L1EGammaClusterEmuProducer *
    process.L1TowerCalibrationProducer *
    process.L1CaloJetProducer
)



process.Out = cms.OutputModule( "PoolOutputModule",
     fileName = cms.untracked.string( "output_round1.root" ),
     fastCloning = cms.untracked.bool( False ),
     outputCommands = cms.untracked.vstring(
                          "drop *",
                          "keep *_genParticles_*_*",
                          "keep *_L1EGammaClusterEmuProducer_*_*",
                          "keep *_L1TowerCalibrationProducer_*_*",
                          "keep *_L1CaloJetProducer_*_*",
                          "keep *_simCaloStage2Digis_MP_HLT",
                          "keep *_addPileupInfo_*_*",
                          "keep *_ak4GenJetsNoNu__HLT",
                          )
)

process.end = cms.EndPath( process.Out )



#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())

