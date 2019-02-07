#!/usr/bin/env python
import os, sys
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
#from argparse import ArgumentParser
#This takes care of converting the input files from CRAB. It is the reason for which you need the file PSet.py also in the python directory.
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#User inputs
#parser = ArgumentParser()
#parser.add_argument('-c', '--channel', dest='channel', action='store', choices=['tautau','mutau','eletau','muele','mumu','ee'], type=str, default='mumu')
#parser.add_argument('-t', '--type',    dest='type',    action='store', choices=['data','mc'],                                             default='mc')
#parser.add_argument('-y', '--year',    dest='year',    action='store', choices=[2016,2017,2018],                                type=int, default=2017)
#args = parser.parse_args()
channel  = 'mumu' #args.channel
dataType = 'mc' #'data'#'mc' #args.type
year     = 2017 #args.year

kwargs = {
 #User inputs
 'channel': channel,
 'dataType': dataType,
 'year': year,
 #
 'maxNumEvt': -1, #It is the maximum number of events you want to analyze. -1 means all entries from the input file. 
 'prescaleEvt': 1, #It allows to analyze 1 event every N. 1 means analyze all events.
 #Analysis quantities
 'mu_minPt': 23, #GeV
 'mu_minEta': 2.4,
 'mu_minNum': 2 #It refers to the minimum number of muons after the the muon ID/Iso 
}

#Input files
if dataType=='data':
 if year==2017:
  infiles = ['root://cms-xrd-global.cern.ch//store/data/Run2017B/Tau/NANOAOD/31Mar2018-v1/10000/04463969-D044-E811-8DC1-0242AC130002.root' ]
 else:
  infiles = ['root://cms-xrd-global.cern.ch//store/group/phys_tau/ProdNanoAODv4Priv/16dec18/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4Priv-from_102X_upgrade2018_realistic_v15_ver2/181216_125027/0000/myNanoRunMc2018_NANO_75.root'
            ] 
if dataType=='mc':
 if year==2017:
  infiles = ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/90000/54362765-8948-E811-9E4A-001F29085CDE.root', #   84396
            ]
 else:
  infiles = ['root://cms-xrd-global.cern.ch//store/group/phys_tau/ProdNanoAODv4Priv/16dec18/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4Priv-from_102X_upgrade2018_realistic_v15_ver1/181216_125011/0000/myNanoRunMc2018_NANO_101.root'
            ]      

#Modules
if channel=='tautau':
 from PicoFramework.TreeProducer.ModuleTauTau import *
 module2run = lambda : ProducerTauTau(**kwargs)
elif channel=='mutau':
 from PicoFramework.TreeProducer.ModuleMuTau import *
 module2run = lambda : ProducerMuTau(**kwargs)
elif channel=='eletau':
 from PicoFramework.TreeProducer.ModuleEleTau import *
 module2run = lambda : ProducerEleTau(**kwargs)
elif channel=='mumu':
 from PicoFramework.TreeProducer.ModuleMuMu import *
 module2run = lambda : ProducerMuMu(**kwargs)
elif channel=='muele':
 from PicoFramework.TreeProducer.ModuleMuEle import *
 module2run = lambda : ProducerMuEle(**kwargs)
else:
 print 'Invalid channel name'

#Run
#All options
#PostProcessor(outputDir,inputFiles,cut=None,branchsel=None,modules=[],compression="LZMA:9",friend=False,postfix=None,jsonInput=None,noOut=False,justcount=False,provenance=False,haddFileName=None,fwkJobReport=False,histFileName=None,histDirName=None,outputbranchsel=None)
#Local run
#p = PostProcessor(outputDir=".",inputFiles=infiles,modules=[module2run()],noOut=True)
#Crab run
p = PostProcessor(outputDir=".",inputFiles=inputFiles(),modules=[module2run()],noOut=True,fwkJobReport=True)
p.run()
print "DONE"
