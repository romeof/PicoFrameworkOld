# PicoFramework/TreeProducer
It reads centrally-produced NanoAOD and saves the information you need in your analysis-tree.
The master branch contains a very simple example of analysis selecting 2 muons. 
Hints are provided for exending it to the case of an analysis interested in multi-channels (e.g. ee,mumu or tautau->tauhtauh, mutauh, eletauh, elemu).

## Installation
Install `CMSSW`
```
scram p -n CMSSW_10_2_9_Label CMSSW CMSSW_10_2_9 #It is the equivalent of cmsrel CMSSW_10_2_9, with the possibility to add a "Label" to the working directory.
cd CMSSW_10_2_9_Label/src
cmsenv
```

Install the centrally-maintained `PhysicsTools/NanoAODTools`
```
git cms-init #not really needed unless you later want to add some other cmssw stuff
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
```

Install the framework `PicoFramework/TreeProducer`
```
git clone 
```

Make `PhysicsTools/NanoAODTools` compatible with `PicoFramework/TreeProducer`
```
cp ./PicoFramework/TreeProducer/utils/postprocessor.py ./PhysicsTools/NanoAODTools/python/postprocessing/framework/postprocessor.py
```

Compile all
```
scram b 
```

## Analysis code
The files you are interested in to set up your analysis are in `PicoFramework/TreeProducer/python`. They are
**analyzer.py**
Here you fix your analysis deciding analysis quantities (e.g. mu_minPt), input files, and modules (how to process the events). 

**ModuleMuMu.py**
Here you implement the code on how to process the events (e.g. dimuon selection).

**TreeProducerMuMu.py**
Here you specify the quantities you want to save.

**TreeProducerCommon.py**
Here you specify the quantities you want to save, if they have an event basis (e.g. run, luminosityBlock info, or dilepton mass for a multi-channel dilepton analysis).
You also implement the functions useful for your analysis.

## Run

### Locally
In PicoFramework/TreeProducer/python
```
python analyzer.py
```
Remember that you need `p = PostProcessor(outputDir=".",inputFiles=infiles,modules=[module2run()],noOut=True)` in analyzer.py. This can be automatized.


### Crab
In PicoFramework/TreeProducer/crab
```
python multicrab.py
```
Remember that you need `p = PostProcessor(outputDir=".",inputFiles=inputFiles(),modules=[module2run()],noOut=True,fwkJobReport=True)` in analyzer.py. This can be automatized.

## Notes

### NanoAOD

* **working book**: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD
* **2016 `9_4_X`**: https://cms-nanoaod-integration.web.cern.ch/integration/master/mc94X2016_doc.html
* **2017 `9_4_X`**: https://cms-nanoaod-integration.web.cern.ch/integration/master/mc94X_doc.html
* **2017 `10_2_X`**: https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html

More [notes](https://www.evernote.com/l/Ac8PKYGpaJxJArj4eng5ed95_wvpzwSNTgc).

### Samples

* [2016](https://www.evernote.com/l/Ac9nVeF2tcdJI7R-is1KPT2Ukv7A260zNX0)
* [2017](https://www.evernote.com/l/Ac8WfL3Mzx1MrKdm1LfIOl-F-j7NeScPKxs)
* [2018](https://www.evernote.com/l/Ac9yyi7wtg9LaYgxOIz11jFyzLV0ztkemtE)

### Luminosity

* [2017](https://ineuteli.web.cern.ch/ineuteli/lumi/2017/)
* [2018](https://ineuteli.web.cern.ch/ineuteli/lumi/2018/)

### Pileup 

* [2017](https://ineuteli.web.cern.ch/ineuteli/pileup/2017/)
* [2018](https://ineuteli.web.cern.ch/ineuteli/pileup/2018/)
