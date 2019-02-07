if __name__ == '__main__':
 #####
 ##   User inputs 
 #####
 task          = 'Test_2' #Name of the task (e.g. Test, SignalRegion, ControlRegion, FullAnalysis, ...)
 analysis      = 'LQtop' #Name of the analysis (e.g. VBFHN, LQtop, ...)
 unitsPerJob   = 2 #Units (usually number of root files) per job
 storageSite   = 'T2_CH_CERN' #Site where you redirect the output
 datasetnames  = [ #Name of the folder created by crab and corresponding to its datasetinputs
'2017_DYJetsToLLM50',
'2017_ZZ'
                 ]
 datasetinputs = [ #Name of in the input dataset
'/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM',
'/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
                 ]
 #####
 ##   Multicrab configuration
 #####
 from CRABClient.UserUtilities import config, getUsernameFromSiteDB
 config = config()
 from CRABAPI.RawCommand import crabCommand
 from CRABClient.ClientExceptions import ClientException
 from httplib import HTTPException
 config.General.workArea = '%s' % (task) 
 
 def submit(config):
  try:
   crabCommand('submit', config = config)
  except HTTPException as hte:
   print "Failed submitting task: %s" % (hte.headers)
  except ClientException as cle:
   print "Failed submitting task: %s" % (cle)
 #####
 ##   Crab configuration
 #####
 for d in range(0,len(datasetnames)):
  config.section_('General')
  config.General.requestName      = datasetnames[d]
  config.General.transferLogs=True
  config.section_('JobType')
  config.JobType.pluginName       = 'Analysis'
  config.JobType.psetName         = 'PSet.py'
  config.JobType.scriptExe        = 'crab_script.sh'
  config.JobType.inputFiles       = ['../python/analyzer.py','../../../PhysicsTools/NanoAODTools/scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
  config.JobType.sendPythonFolder = True
  config.section_('Data')
  config.Data.inputDataset        = datasetinputs[d]
  config.Data.inputDBS            = 'global'
  config.Data.splitting           = 'FileBased'
  #config.Data.totalUnits         = 2500 #With 'FileBased' splitting tells how many files to analyse
  config.Data.unitsPerJob         = unitsPerJob 
  config.Data.outLFNDirBase       = '/store/user/%s/%s' % (getUsernameFromSiteDB(),analysis) 
  config.Data.outputDatasetTag    = '%s' % (task) 
  config.Data.publication         = False
  config.section_('Site')
  config.Site.storageSite         = '%s' % (storageSite) 
  submit(config)
