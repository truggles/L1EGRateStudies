// -*- C++ -*-
//
// Package:    L1EGCrystalsHeatMap
// Class:      L1EGCrystalsHeatMap
// 
/**\class L1EGCrystalsHeatMap L1EGCrystalsHeatMap.cc SLHCUpgradeSimulations/L1EGCrystalsHeatMap/src/L1EGCrystalsHeatMap.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Nick Smith
//         Created:  Mon Apr  7 19:20:22 CDT 2014
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "SimDataFormats/Track/interface/SimTrackContainer.h"
#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "SimDataFormats/CaloHit/interface/PCaloHitContainer.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "Geometry/CaloEventSetup/interface/CaloTopologyRecord.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"

#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/EcalAlgo/interface/EcalBarrelGeometry.h"
#include "Geometry/EcalAlgo/interface/EcalEndcapGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloCellGeometry.h"
#include <iostream>

#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "FastSimulation/CaloGeometryTools/interface/CaloGeometryHelper.h"
#include "SimDataFormats/SLHC/interface/L1EGCrystalCluster.h"
#include "Geometry/CaloTopology/interface/CaloTopology.h"

#include "Geometry/CommonDetUnit/interface/GeomDet.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "SimDataFormats/CaloTest/interface/HcalTestNumbering.h"
#include "DataFormats/HcalDetId/interface/HcalSubdetector.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"

#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"
#include "DataFormats/HcalRecHit/interface/HcalSourcePositionData.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include "TH2.h"
#include "TVector3.h"

namespace l1slhc {
   class L1EGCrystalClusterTest {
      public:
         float et ;
         float eta ;
         float phi ;
         float e ;
         float x ;
         float y ;
         float z ;
         float hovere ;

         float ECALiso ;
         float ECALetPUcorr;
         bool marked=false;
         bool isoMarked=false;
   };
}

//
// class declaration
//

class L1EGCrystalsHeatMap : public edm::EDAnalyzer {
   public:
      explicit L1EGCrystalsHeatMap(const edm::ParameterSet&);
      ~L1EGCrystalsHeatMap();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      //virtual void endRun(edm::Run const&, edm::EventSetup const&);
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

      // ----------member data ---------------------------
      CaloGeometryHelper myGeometry;
      std::vector<l1slhc::L1EGCrystalClusterTest> ecalhits;
      std::vector<l1slhc::L1EGCrystalClusterTest> hcalhits;
      bool DEBUG;
      bool First = true;
      TH2F * heatmap;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
L1EGCrystalsHeatMap::L1EGCrystalsHeatMap(const edm::ParameterSet& iConfig)
{
   DEBUG = iConfig.getParameter<bool>("DEBUG");
   
   edm::Service<TFileService> fs;
   heatmap = fs->make<TH2F>("heatmap", "Heatmap;d#eta;d#phi", 21, -0.175-0.0175/2, 0.175+0.0175/2, 21, -0.175-0.0175/2, 0.175+0.0175/2);
}


L1EGCrystalsHeatMap::~L1EGCrystalsHeatMap()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
L1EGCrystalsHeatMap::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   
   if (First) {
      edm::ESHandle<CaloTopology> theCaloTopology;
      iSetup.get<CaloTopologyRecord>().get(theCaloTopology);       
      edm::ESHandle<CaloGeometry> pG;
      iSetup.get<CaloGeometryRecord>().get(pG);     
      // Setup the tools
      double bField000 = 4.;
      myGeometry.setupGeometry(*pG);
      myGeometry.setupTopology(*theCaloTopology);
      myGeometry.initialize(bField000);
      First = false ;
   }

   // Retrieve the SimHits.
   // Sasha's FAMOS :
   //edm::Handle<edm::PCaloHitContainer> pcalohits;
   //iEvent.getByLabel("famosSimHits","EcalHitsEB",pcalohits);
   // using RecHits :
   edm::Handle<EcalRecHitCollection> pcalohits;
   iEvent.getByLabel("ecalRecHit","EcalRecHitsEB",pcalohits);
   // Geant's pcaloHits :
   //// edm::Handle<edm::PCaloHitContainer> pcalohits;
   //// iEvent.getByLabel("g4SimHits","EcalHitsEB",pcalohits);

   for(auto hit : *pcalohits.product())
   {
      if(hit.energy() > 0.2)
      {
         EBDetId EBid = EBDetId(hit.id()) ;
         auto cell = myGeometry.getEcalBarrelGeometry()->getGeometry(hit.id());
         double theta =  cell->getPosition().theta() ;
         double phi =  cell->getPosition().phi() ;
         double eta = -1.*log(tan(theta/2.)) ;
         l1slhc::L1EGCrystalClusterTest cluster_hit;
         cluster_hit.et = (hit.energy())*sin(theta) ;
         cluster_hit.eta = eta ;
         cluster_hit.phi = phi ;
         cluster_hit.e = hit.energy() ;
         cluster_hit.x = cell->getPosition().x() ;
         cluster_hit.y = cell->getPosition().y() ;
         cluster_hit.z = cell->getPosition().z() ;
         ecalhits.push_back(cluster_hit);
         if (DEBUG) std::cout << " EB Hits " <<  hit.energy() <<  " phi " << phi << " eta " << eta << " eta1 " << EBid.ieta() << " theta " << theta << std::endl;
      }
   }

   //iEvent.getByLabel("famosSimHits","EcalHitsEE",pcalohits);
   iEvent.getByLabel("ecalRecHit","EcalRecHitsEE",pcalohits);
   // iEvent.getByLabel("g4SimHits","EcalHitsEE",pcalohits);

   for(auto hit : *pcalohits.product())
   {
      if(hit.energy() > 0.2)
      {
         double theta =  myGeometry.getEcalEndcapGeometry()->getGeometry(hit.id())->getPosition().theta() ;
         double phi =  myGeometry.getEcalEndcapGeometry()->getGeometry(hit.id())->getPosition().phi() ;
         double eta = -1.*log(tan(theta/2.)) ;
         l1slhc::L1EGCrystalClusterTest cluster_hit;
         cluster_hit.et = (hit.energy())*sin(theta);
         cluster_hit.eta = eta ;
         cluster_hit.phi = phi ;
         cluster_hit.e = (hit.energy()) ;
         cluster_hit.x = myGeometry.getEcalEndcapGeometry()->getGeometry(hit.id())->getPosition().x() ;
         cluster_hit.y = myGeometry.getEcalEndcapGeometry()->getGeometry(hit.id())->getPosition().y() ;
         cluster_hit.z = myGeometry.getEcalEndcapGeometry()->getGeometry(hit.id())->getPosition().z() ;
         ecalhits.push_back(cluster_hit);
         if (DEBUG) std::cout << " EE Hits " << " energy " << hit.energy() << " phi " << phi << " eta " << eta <<  std::endl;
      }
   }

   edm::ESHandle<CaloGeometry> pG1;
   iSetup.get<CaloGeometryRecord>().get(pG1);
   const CaloGeometry* geometry = pG1.product();

   edm::Handle<HBHERecHitCollection> hbhecoll;
   iEvent.getByLabel("hbheprereco", hbhecoll);

   for (HBHERecHitCollection::const_iterator j=hbhecoll->begin(); j != hbhecoll->end(); j++) {
      HcalDetId cell(j->id());
      const CaloCellGeometry* cellGeometry = geometry->getSubdetectorGeometry(cell)->getGeometry(cell);
      if ( j->energy() > 0.1 )
      {
         l1slhc::L1EGCrystalClusterTest cluster_hit;
         cluster_hit.e = (j->energy()) ;      
         cluster_hit.eta = cellGeometry->getPosition().eta() ;
         cluster_hit.phi = cellGeometry->getPosition().phi() ;
         hcalhits.push_back(cluster_hit);
         if(DEBUG && cluster_hit.e > 10) std::cout << " id " << cell << " Energy " << j->energy() << " eta " << cluster_hit.eta << " phi " << cluster_hit.phi <<  std::endl ;
      }
   }
   
   // Find a cluster that 
   // matches to gen particle
   edm::Handle<reco::GenParticleCollection> genParticleHandle;
   iEvent.getByLabel("genParticles", genParticleHandle);
   reco::GenParticleCollection genParticles = *genParticleHandle.product();
   double dRmin = 999.;
   auto centerhit = std::begin(ecalhits);
   for(auto ecalhit=std::begin(ecalhits); ecalhit!=std::end(ecalhits); ecalhit++)
   {
      reco::Candidate::PolarLorentzVector hitP4(ecalhit->et, ecalhit->eta, ecalhit->phi, 0.);
      if ( reco::deltaR(hitP4, genParticles[0].polarP4()) < dRmin )
      {
         dRmin = reco::deltaR(hitP4, genParticles[0].polarP4());
         centerhit = ecalhit;
      }
   }
   for(auto ecalhit : ecalhits)
   {
      if ( fabs(centerhit->eta-ecalhit.eta) < 0.2 && fabs(centerhit->phi-ecalhit.phi) < 0.2 )
      {
         heatmap->Fill(ecalhit.eta-centerhit->eta, ecalhit.phi-centerhit->phi, ecalhit.e);
      }
   }
}

// ------------ method called once each job just before starting event loop  ------------
void 
L1EGCrystalsHeatMap::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
L1EGCrystalsHeatMap::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
L1EGCrystalsHeatMap::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
L1EGCrystalsHeatMap::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
L1EGCrystalsHeatMap::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
L1EGCrystalsHeatMap::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
L1EGCrystalsHeatMap::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1EGCrystalsHeatMap);