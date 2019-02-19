import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process("L1AlgoTest",eras.Phase2_trigger)

#from CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi import *

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   #reportEvery = cms.untracked.int32(100)
   reportEvery = cms.untracked.int32(1)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(50) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(500) )

process.source = cms.Source("PoolSource",
    # Set to do test run on official Phase-2 L1T Ntuples
    #/GluGluHToTauTau_M125_14TeV_powheg_pythia8/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW
    #/store/mc/PhaseIIFall17D/GluGluHToTauTau_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/00000/00C160E6-6A39-E811-B904-008CFA152144.root
    #
    #/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW
    #/store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/00000/02AE7A07-2339-E811-B98B-E0071B7AC750.root
    #
    #/WJetsToLNu_TuneCUETP8M1_14TeV-madgraphMLM-pythia8/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v3/GEN-SIM-DIGI-RAW
    #/store/mc/PhaseIIFall17D/WJetsToLNu_TuneCUETP8M1_14TeV-madgraphMLM-pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v3/30000/162DC63A-C458-E811-92E1-B083FED42FAF.root

    #fileNames = cms.untracked.vstring('file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/SingleE_FlatPt-2to100/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/80000/C0F55AFC-1638-E811-9A14-EC0D9A8221EE.root'),
    #fileNames = cms.untracked.vstring('file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/00000/02AE7A07-2339-E811-B98B-E0071B7AC750.root'),
    #fileNames = cms.untracked.vstring('file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/GluGluHToTauTau_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/00000/00C160E6-6A39-E811-B904-008CFA152144.root'),
    #fileNames = cms.untracked.vstring('file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/00000/EEC3EC7E-C537-E811-9954-E0071B73C650.root'),
    #fileNames = cms.untracked.vstring('file:/hdfs/store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/00000/9C33F8F2-5D39-E811-8987-0025904C7FC2.root'),
    #fileNames = cms.untracked.vstring('file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/SingleNeutrino/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/80000/C2AEC8C0-695C-E811-ABAD-0CC47AF9B496.root'),

    #fileNames = cms.untracked.vstring('file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/00000/C072C4FC-DF37-E811-8A20-E0071B6C9DD0.root'),
    fileNames = cms.untracked.vstring(
        'file:/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ttbarPU200/ttbarPU200_10_5_0_rep.root',
        'file:/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ttbarPU200/1.root',
        'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/TT_TuneCUETP8M2T4_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v2/30000/564C271B-9654-E811-9338-90B11C2AA16C.root',
        'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/00000/2829A010-B243-E811-B2A3-A0369FE2C0DE.root',
        'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/00000/90F6FE0D-B243-E811-8A7E-A0369FD0B192.root',
        'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/00000/54D11785-C443-E811-8A2F-0CC47A4D99F0.root',
        'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/00000/2461D62D-D043-E811-9A11-0CC47A4DEF54.root',
        'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/00000/683F62C4-B843-E811-928C-A0369FD0B234.root',
        'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/00000/C2C91225-C343-E811-BAC6-A0369FE2C18E.root',
    ),
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
                    "drop l1tL1PF*_l1pf*Producer_*_L1",

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
# ----   Produce Gen Taus

process.tauGenJets = cms.EDProducer(
    "TauGenJetProducer",
    GenParticles =  cms.InputTag('genParticles'),
    includeNeutrinos = cms.bool( False ),
    verbose = cms.untracked.bool( False )
)



process.tauGenJetsSelectorAllHadrons = cms.EDFilter("TauGenJetDecayModeSelector",
     src = cms.InputTag("tauGenJets"),
     select = cms.vstring('oneProng0Pi0', 
                          'oneProng1Pi0', 
                          'oneProng2Pi0', 
                          'oneProngOther',
                          'threeProng0Pi0', 
                          'threeProng1Pi0', 
                          'threeProngOther', 
                          'rare'),
     filter = cms.bool(False)
)



process.tauGenJetsSelectorElectrons = cms.EDFilter("TauGenJetDecayModeSelector",
     src = cms.InputTag("tauGenJets"),
     select = cms.vstring('electron'), 
     filter = cms.bool(False)
)



process.tauGenJetsSelectorMuons = cms.EDFilter("TauGenJetDecayModeSelector",
     src = cms.InputTag("tauGenJets"),
     select = cms.vstring('muon'), 
     filter = cms.bool(False)
)








# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1EGCrystal clusters using Emulator

process.load('L1Trigger.L1CaloTrigger.L1EGammaCrystalsEmulatorProducer_cfi')
process.L1EGammaClusterEmuProducer.ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","REPR")



# --------------------------------------------------------------------------------------------
#
# ----    Produce the calibrated tower collection combining Barrel, HGCal, HF

process.load('L1Trigger/L1CaloTrigger/L1TowerCalibrationProducer_cfi')
process.L1TowerCalibrationProducer.L1HgcalTowersInputTag = cms.InputTag("hgcalTowerProducer","HGCalTowerProcessor","REPR")



# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1CaloJets with the L1EG clusters as ECAL seeds

process.load('L1Trigger/L1CaloTrigger/L1CaloJetProducer_cfi')


process.pL1Objs = cms.Path( 
    process.tauGenJets *
    process.tauGenJetsSelectorAllHadrons *
    process.tauGenJetsSelectorElectrons *
    process.tauGenJetsSelectorMuons *
    process.L1EGammaClusterEmuProducer *
    process.L1TowerCalibrationProducer *
    process.L1CaloJetProducer
)



# ----------------------------------------------------------------------------------------------
# 
# Analyzer starts here

process.analyzer = cms.EDAnalyzer('L1CaloJetStudies',
    L1CaloJetsInputTag = cms.InputTag("L1CaloJetProducer","L1CaloJetsNoCuts"),
    genJets = cms.InputTag("ak4GenJetsNoNu", "", "HLT"),
    genHadronicTauSrc = cms.InputTag("tauGenJetsSelectorAllHadrons"),
    genMatchDeltaRcut = cms.untracked.double(0.25),
    genMatchRelPtcut = cms.untracked.double(0.5),
    debug = cms.untracked.bool(False),
    #doRate = cms.untracked.bool(False),
    doRate = cms.untracked.bool(True),
    Stage2JetTag = cms.InputTag("simCaloStage2Digis", "MP", "HLT"),
    Stage2TauTag = cms.InputTag("simCaloStage2Digis", "MP", "HLT"),
    puSrc = cms.InputTag("addPileupInfo")
)

process.panalyzer = cms.Path(process.analyzer)



process.TFileService = cms.Service("TFileService", 
   fileName = cms.string("_jetOutputFileName0GeV3.root"), 
   #closeFileFast = cms.untracked.bool(True)
   closeFileFast = cms.untracked.bool(False)
)



#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())

