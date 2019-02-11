import ROOT
import math 
import numpy as num 
from TreeProducerCommon import *

class TreeProducerMuMu(TreeProducerCommon):
 def __init__(self, name):
  super(TreeProducerMuMu, self).__init__(name)

  #Tree branches
  #Muon
  self.add_branch("mu0_pt")
  self.add_branch("mu0_eta")
  self.add_branch("mu1_pt")
  self.add_branch("mu1_eta")

  #Event variables
  self.add_branch("mu0mu1_mass")
