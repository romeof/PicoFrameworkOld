import os, sys
import ROOT
import math 
import numpy as num 

class TreeProducerCommon(object):
 def __init__(self, name):

  #Create file (Do not change this paragraph!)
  inputFile = name
  outputFileName = os.path.basename(str(inputFile)).split(".root", 1)[0]+"_Skim.root"
  compression = "LZMA:9"
  ROOT.gInterpreter.ProcessLine("#include <Compression.h>")
  (algo, level) = compression.split(":")
  compressionLevel = int(level)
  if   algo == "LZMA": compressionAlgo  = ROOT.ROOT.kLZMA
  elif algo == "ZLIB": compressionAlgo  = ROOT.ROOT.kZLIB
  else: raise RuntimeError("Unsupported compression %s" % algo)
  self.outputfile = ROOT.TFile(outputFileName, 'RECREATE',"",compressionLevel)
  self.outputfile.SetCompressionAlgorithm(compressionAlgo)
  
  #Meta data (Do not change this paragraph!)
  self._otherTrees = {}
  self._otherObjects = {}
  for k in inputFile.GetListOfKeys():
   kn = k.GetName()
   if kn == "Events":
    continue # this we are doing
   #elif kn in ("MetaData", "ParameterSets", "LuminosityBlocks", "Runs"):
   elif kn in ("MetaData", "ParameterSets"):
    self._otherTrees[kn] = inputFile.Get(kn).CopyTree('1')
   elif k.GetClassName() == "TTree":
    print "Not copying unknown tree %s" % kn
   else:
    self._otherObjects[kn] = inputFile.Get(kn)
    print "Not copying" #self._otherObjects[kn] = inputFile.Get(kn)  
  for t in self._otherTrees.itervalues():
   t.Write()
  for on,ov in self._otherObjects.iteritems():
   self.outputfile.WriteTObject(ov,on)

  #All entries (Do not change this paragraph!)
  self.evtree = ROOT.TTree('evtree','evtree')
  self.add_branch("numparsedevt")
        
  #Common variables (Do not change this paragraph!)
  self.Events = ROOT.TTree('Events','Events')
  self.add_branch("run")
  self.add_branch("luminosityBlock")
  self.add_branch("event")

  #Event variables. Add your variables here. 
  self.add_branch("mu0mu1_mass")

  #Histogram for cutflow
  #self.cutflow = ROOT.TH1F('cutflow', 'cutflow',  25, 0,  25)
  #self.pileup  = ROOT.TH1F('pileup',  'pileup',  100, 0, 100)

 def add_branch(self, name, dtype=num.dtype(float)):
  #name should be a string
  #dtype should be a numpy.dtype

  #used to translate numpy to root nomenclature
  dtype_translation={
   '?': "O",
   'b': "B",
   'B': "b",
   'i': "I",
   'u': "i",
   'f': "D"
   # 'c':
   # 'm':
   # 'M':
   # 'O':
   # 'S':
   # 'a':
   # 'U':
   # 'V':
  }

  #numpy:
  # '?' 	boolean
  # 'b' 	(signed) byte
  # 'B' 	unsigned byte
  # 'i' 	(signed) integer
  # 'u' 	unsigned integer
  # 'f' 	floating-point
  # 'c' 	complex-floating point
  # 'm' 	timedelta
  # 'M' 	datetime
  # 'O' 	(Python) objects
  # 'S', 'a' 	zero-terminated bytes (not recommended)
  # 'U' 	Unicode string
  # 'V' 	raw data (void)

  #root:
  # C : a character string terminated by the 0 character
  # B : an 8 bit signed integer (Char_t)
  # b : an 8 bit unsigned integer (UChar_t)
  # S : a 16 bit signed integer (Short_t)
  # s : a 16 bit unsigned integer (UShort_t)
  # I : a 32 bit signed integer (Int_t)
  # i : a 32 bit unsigned integer (UInt_t)
  # F : a 32 bit floating point (Float_t)
  # D : a 64 bit floating point (Double_t)
  # L : a 64 bit signed integer (Long64_t)
  # l : a 64 bit unsigned integer (ULong64_t)
  # O : [the letter o, not a zero] a boolean (Bool_t)

  setattr(self,name,num.full((1),-1, dtype=dtype))
  if(name=="numparsedevt"):
   self.evtree.Branch(name, getattr(self,name) , "{0}/{1}".format(name,dtype_translation[dtype.kind]))
  else:
   self.Events.Branch(name, getattr(self,name) , "{0}/{1}".format(name,dtype_translation[dtype.kind]))

var_dict = {
  'Electron_mvaFall17Iso_WP90': 'Electron_mvaFall17Iso_WP90',
  'Electron_mvaFall17Iso_WPL':  'Electron_mvaFall17Iso_WPL',
}
def setYear(year):
 """Help function to change the name of some variables that depend on the year."""
 if year==2018:
  print "setYear: setting var_dict to year %s"%(year)
  var_dict['Electron_mvaFall17Iso_WPL']  = 'Electron_mvaFall17V1Iso_WPL'
  var_dict['Electron_mvaFall17Iso_WP90'] = 'Electron_mvaFall17V1Iso_WP90'
