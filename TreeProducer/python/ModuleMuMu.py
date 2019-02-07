import os, sys
import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TreeProducerMuMu import *

class declareVariables(TreeProducerMuMu):
 def __init__(self, name):
  super(declareVariables, self).__init__(name)

class ProducerMuMu(Module):
 def __init__(self, **kwargs):
  #Here is where you initialize the arguments of "self"
  #User inputs
  self.channel   = kwargs.get('channel') 
  self.isData    = kwargs.get('dataType')=='data'
  self.year      = kwargs.get('year') 
  #
  self.evtcount  = 0
  self.maxNumEvt = kwargs.get('maxNumEvt')
  self.prescaleEvt = kwargs.get('prescaleEvt')
  #Analysis quantities
  self.mu_minPt  = kwargs.get('mu_minPt')
  self.mu_minEta = kwargs.get('mu_minEta')
  self.mu_minNum = kwargs.get('mu_minNum')

  #Set year, variables. Help function to change the name of some variables that depend on the year.
  setYear(self.year)

  #Trigger
  #if year==2017:
  # self.trigger = lambda e: e.HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg or e.HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg or e.HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg
  #else:
  # if self.isData:
  #  self.trigger = lambda e: e.HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg or e.HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg or e.HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg \
  #                           if e.run<317509 else e.HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg
  # else:
  #  self.trigger = lambda e: e.HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg

  #ID
  #self.vlooseIso = getVLooseTauIso(year)
  # self.tauCutPt    = 20
  
  #Corrections

  #Cut flow table
        
 def beginJob(self):
  print "Here is beginJob"
  #pass
        
 def endJob(self):
  print "Here is endJob"
  #pass
        
 def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
  print "Here is beginFile"
  self.out = declareVariables(inputFile) 
  #pass
        
 def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):        
  print "Here is endFile"
  self.out.numparsedevt[0] = self.evtcount
  self.out.evtree.Fill()
  self.out.outputfile.Write()
  self.out.outputfile.Close()
  #pass
        
 def analyze(self, event):
  """process event, return True (go to next module) or False (fail, go to next event)"""
  #For all events
  if(self.evtcount>=self.maxNumEvt and self.maxNumEvt!=-1):
   return False
  self.evtcount = self.evtcount+1
  if(not (self.evtcount%self.prescaleEvt==0)):
   return False

  #Analysis specific
  #Primary vertex

  #Trigger        
  #if event.HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg or : 
  #if not self.trigger(event):
  # return False

  #Object selection
  idx_goodmuons = []
  for imuon in range(event.nMuon):
   if event.Muon_pt[imuon] < self.mu_minPt: continue
   if abs(event.Muon_eta[imuon]) > self.mu_minEta: continue
   #if abs(event.Muon_dz[imuon]) > 0.2: continue
   #if abs(event.Muon_dxy[imuon]) > 0.045: continue
   #if not event.Muon_mediumId[imuon]: continue
   #if event.Muon_pfRelIso04_all[imuon]>0.50: continue
   idx_goodmuons.append(imuon)

  #Event selection
  if len(idx_goodmuons)<self.mu_minNum:
   return False        

  muons = Collection(event, 'Muon')
  mu0 = muons[idx_goodmuons[0]].p4() 
  mu1 = muons[idx_goodmuons[1]].p4() 

  #Save tree info  
  #MuMu
  self.out.mu0_pt[0] = mu0.Pt()
  self.out.mu0_eta[0] = mu0.Eta()
  self.out.mu1_pt[0] = mu1.Pt()
  self.out.mu1_eta[0] = mu1.Eta()
  #Common
  self.out.run[0] = event.run 
  self.out.luminosityBlock[0] = event.luminosityBlock
  self.out.event[0] = event.event #& 0xffffffffffffffff
  #Event
  self.out.mu0mu1_mass[0] = (mu0+mu1).M() 
 
  #Save tree
  self.out.Events.Fill() 
  return True
