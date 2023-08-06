import os
#os.environ['CRDS_PATH'] = '/fenrirdata1/kg_data/crds_cache/' #These pathways should be defined in your ~./bash profile. If not, you can set them within the notebook.
#os.environ['CRDS_SERVER_URL']= 'https://jwst-crds.stsci.edu'
#os.environ['CRDS_CONTEXT']='jwst_0756.pmap' #Occasionally, the JWST CRDS pmap will be updated. Updates may break existing code. Use this command to revert to an older working verison until the issue is fixed.


import jwst
print(jwst.__version__) #Print what version of the pipeline you are using.

from jwst.pipeline.calwebb_detector1 import Detector1Pipeline #Stage 1
from jwst.pipeline.calwebb_image2 import Image2Pipeline #Stage 2
from jwst.pipeline.calwebb_tso3 import Tso3Pipeline #Stage 3
from jwst.associations.asn_from_list import asn_from_list #Association file imports
from jwst.associations.lib.rules_level2_base import DMSLevel2bBase

#General
from astropy.io import fits, ascii
import matplotlib.pyplot as plt
import csv
import numpy as np
import asdf
import astropy.units as u
import glob
import time
import yaml

import pdb

from copy import deepcopy

import pkg_resources

# Individual steps that make up calwebb_detector1
from jwst.dq_init import DQInitStep
from jwst.saturation import SaturationStep
from jwst.superbias import SuperBiasStep
from jwst.ipc import IPCStep                                                                                    
from jwst.refpix import RefPixStep                                                                
from jwst.linearity import LinearityStep
from jwst.persistence import PersistenceStep
from jwst.dark_current import DarkCurrentStep
from jwst.jump import JumpStep
from jwst.ramp_fitting import RampFitStep
from jwst import datamodels


# In[359]:


## ES custom pipeline
from tshirt.pipeline import phot_pipeline
from tshirt.pipeline.instrument_specific import rowamp_sub
import tqdm

defaultParamPath = pkg_resources.resource_filename('jtow',path_to_defaults)


def read_yaml(filePath):
    with open(filePath) as yamlFile:
        yamlStructure = yaml.safe_load(yamlFile)
    return yamlStructure

class jw(object):
    def __init__(self,paramFile=defaultParamPath,directParam=directParam):
        """
        An wrapper object to run the jwst pipeline (with some modifications)
        
        Parameters
        -----------
        paramFile: str
            Location of the YAML file containing the parameters.
        
        directParam: dict
            A dictionary of parameters. Overrides the paramFile
        """
        
        self.get_parameters(paramFile,directParam=directParam)
        
        defaultParams = read_yaml(defaultParamPath)
        
        for oneKey in defaultParams.keys():
            if oneKey not in self.param:
                self.param[oneKey] = defaultParams[oneKey]
                
        self.get_files(self)
        
        self.max_cores = "half"
        

        
        #photParam = {'refStarPos': [[67.0 - 1.0,30.0 - 1.0]],'backStart':49,'backEnd': 50,
        self.photParam = {'refStarPos': [[1052,57]],'backStart':100,'backEnd': 101,
                          'FITSextension': 1,
                          'isCube': True,'cubePlane':0,'procFiles':'*.fits'}
        
    
    def get_parameters(self,paramFile,directParam=None):
        if directParam is None:
            self.paramFile = paramFile
            self.param = read_yaml(paramFile)
        else:
            self.paramFile = 'direct dictionary'
            self.param = directParam
        
        
    def get_files(self):
        
        all_uncal_files = [] 
        #output_dir = '/fenrirdata1/es_tso/sim_data/mirage_035_hatp14_short_for_pipe_tests/stsci_proc/'
        #output_dir = '/fenrirdata1/es_tso/sim_data/mirage_032_hatp14_car33_no_backg/stsci_proc/'
        #output_dir = '/fenrirdata1/es_tso/sim_data/mirage_032_hatp14_car33_no_backg/stsci_proc_003_es_refcor/'
        #rawFileSearch = "/fenrirdata1/es_tso/sim_data/mirage_029_hd189733b_transit/raw/*nrca1_uncal.fits"
        #output_dir = '/fenrirdata1/es_tso/sim_data/mirage_029_hd189733b_transit/proc_roeba_nrca1/'
        #rawFileSearch = "/fenrirdata1/es_tso/sim_data/mirage_029_hd189733b_transit/raw/*nrca1_uncal.fits"
        #rawFileSearch = "/fenrirdata1/es_tso/sim_data/mirage_037_hatp14_lower_well_frac/raw/*nrca3_uncal.fits"
        #output_dir = "/fenrirdata1/es_tso/sim_data/mirage_037_hatp14_lower_well_frac/proc_roeba_nrca3"
        
        output_dir = self.param["outputDir"]
        if os.path.exists(output_dir) == False:
            os.makedirs(output_dir)
        
        rawList = np.sort(glob.glob(self.param['rawFileSearch']))
        
        for fitsName in rawList: #Grabbing only these files from the directory
        
            HDUList = fits.open(fitsName, 'update')
            HDUList[0].header['NOUTPUTS'] = (4, 'Number of output amplifiers') #This was not input at the time of the simulation. Therefore, we manually must input this information.
            HDUList.close()
            all_uncal_files.append(fitsName)
    
        self.all_uncal_files = sorted(all_uncal_files) #sort files alphabetically.
    
    def run_jw(self):
        """
        Run the JWST pipeline for all uncal files
        """
        
        startTime = time.time() #Time how long this step takes
        
        for uncal_file in self.all_uncal_files:
                # Using the run() method. Instantiate and set parameters
            dq_init_step = DQInitStep()
            dq_init = dq_init_step.run(uncal_file)
    
    
            # ## Saturation Flagging
            # Using the run() method
            saturation_step = SaturationStep()
            # Call using the the output from the previously-run dq_init step
            saturation = saturation_step.run(dq_init)
            del dq_init ## try to save memory
    
            # Using the run() method
            superbias_step = SuperBiasStep()
            # superbias_step.output_dir = output_dir
            # superbias_step.save_results = True
    
            # Call using the the output from the previously-run saturation step
            superbias = superbias_step.run(saturation)
            del saturation ## try to save memory
    
    
            # Instantiate and set parameters
            refpix_step = RefPixStep()
            #refpix_step.output_dir = output_dir
            #refpix_step.save_results = True
    
            # try using a copy of the bias results as the refpix output
            # refpix = refpix_step.run(superbias)
            # es_refpix = deepcopy(refpix)
            # the old way was to run the refpix and then replace it
            es_refpix = deepcopy(superbias)
    
            ngroups = superbias.meta.exposure.ngroups
            nints = superbias.data.shape[0] ## use the array size because segmented data could have fewer ints
            ## (instead of 
    
            # First, make sure that the aperture looks good. Here I have cheated and used a final rampfit result.
    
            # In[389]:
    
    
            phot = phot_pipeline.phot(directParam=self.photParam)
    
    
            # In[390]:
    
    
            #phot.showStamps(showPlot=True,boxsize=200,vmin=0,vmax=1)
    
    
            # Everything inside the larger blue circle will be masked when doing reference pixel corrections
    
            # In[391]:
    
    
            for oneInt in tqdm.tqdm(np.arange(nints)):
                for oneGroup in np.arange(ngroups):
            
                    rowSub, modelImg = rowamp_sub.do_backsub(superbias.data[oneInt,oneGroup,:,:],phot)
                    es_refpix.data[oneInt,oneGroup,:,:] = rowSub
    
    
            # # Linearity Step
    
            # In[328]:
            del superbias ## try to save memory
    
            # Using the run() method
            linearity_step = LinearityStep()
            # refpix step
            linearity = linearity_step.run(es_refpix)
            del es_refpix ## try to save memory
    
            # # Persistence Step
    
            # Using the run() method
            persist_step = PersistenceStep()

            # skip for now since ref files are zeros
            persist_step.skip = True
    
            persist = persist_step.run(linearity)
            del linearity ## try to save memory
    
            # # Dark current step
    
            # Using the run() method
            dark_step = DarkCurrentStep()
    
            # There was a CRDS error so I'm skipping
            dark_step.skip = True
    
            # Call using the persistence instance from the previously-run
            # persistence step
            dark = dark_step.run(persist)

            del persist ## try to save memory
    
            # # Jump Step
    
            # In[335]:
    
    
            # Using the run() method
            jump_step = JumpStep()
            #jump_step.output_dir = output_dir
            #jump_step.save_results = True
            jump_step.rejection_threshold = 15

            jump_step.maximum_cores = max_cores
            # Call using the dark instance from the previously-run
            # dark current subtraction step
            jump = jump_step.run(dark)
            del dark ## try to save memory
    
            # # Ramp Fitting
    
            # In[344]:
    
    
            # Using the run() method
            ramp_fit_step = RampFitStep()
            ramp_fit_step.maximum_cores = max_cores
    
            ramp_fit_step.output_dir = output_dir
            ramp_fit_step.save_results = True
    
            # Let's save the optional outputs, in order
            # to help with visualization later
            #ramp_fit_step.save_opt = True
    
            # Call using the dark instance from the previously-run
            # jump step
            ramp_fit = ramp_fit_step.run(jump)
            del jump ## try to save memory
            del ramp_fit ## try to save memory
    
    
        executionTime = (time.time() - startTime)
        print('Stage 1 Execution Time in Seconds: ' + str(executionTime)) #Time how long this step takes
