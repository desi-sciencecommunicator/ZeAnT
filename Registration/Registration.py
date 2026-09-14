from skimage import io
from scipy.cluster.vq import kmeans2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mc

# %matplotlib inline
plt.ion()

import os
import multiprocessing
num_cores = multiprocessing.cpu_count()
print("Number of cores:", num_cores)
os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = str(num_cores)

import pandas as pd
import h5py
from PIL import Image
# import skimage.io as skio
# from skimage import io
import numpy as np
from scipy.optimize import minimize
from scipy.io import loadmat
from scipy import stats
import scipy.signal as sc
import datetime
import time
from  matplotlib.dates import num2date, date2num
import itertools
from tqdm import tqdm
import shutil
import ants as ants

# ------------ set up parameters ----------------

base_folder = '/central/groups/Proberlab/dascenci/'
ants_folder = base_folder + 'ANTS_output/'
proj_ID = 'cmpk2'
date_ID = '20240401'
fish_ID = 'fish1_test'
expt_ID = '{0}_{1}'.format(date_ID, fish_ID)
expt_ID_list = [expt_ID]

mapzebrain_folder = base_folder + 'mapzebrain/ants_template/' 
mapzebrain_template_name = 'live_standard_nlsGCaMP.nrrd'
mapzebrain_template_path = mapzebrain_folder + mapzebrain_template_name

volume_id = 1000
volume_path = '/central/groups/Proberlab/dascenci/caiman_repo/demos/notebooks/data_prep/volume{0}.h5'.format(volume_id)

#imaging parameters for loading volume mean
pixel_size = 1.62 #microns 
depth = 250 #microns for one whole volume 
num_slice = 50

# ------------ body ----------------

import DA_edit_library_registration_cmpk2

stim = 0

for expt_ID in expt_ID_list:

    print('creating_folder ...')
    output_folder = DA_edit_library_registration_cmpk2.create_folder(ants_folder, proj_ID, expt_ID)
    print('    - DONE\nloading mapzebrain ...')
    mapZebrain_ants = DA_edit_library_registration_cmpk2.load_mapzebrain_reference_brain(mapzebrain_template_path, save_fig=True, to_save_folder=output_folder)
    # print('MAP: {0}\ntype {1}'.format(mapzebrain_template_path, type(mapzebrain_template_path)))
    print('    - DONE\nloading volume mean ...')
    volume_mean_ants = DA_edit_library_registration_cmpk2.load_volume_mean(volume_path, pixel_size, depth, num_slice, save_fig=True, to_save_folder=output_folder) 
    print('    - DONE\nGetting pad widths ...')
#THIS IS SPECIFICALLY FOR MY CURRENT USE CASE, MAKE MORE DYNAMIC LATER
    pad_width = DA_edit_library_registration_cmpk2.get_padding_width(mapZebrain_ants, volume_mean_ants, save_fig=True, to_save_folder=output_folder)

    # # ----------------------------- debugging section -----------------------------

    # # fixed_norm = ants.iMath_normalize(mapZebrain_ants)
    # # moving_norm = ants.iMath_normalize(volume_mean_ants)
    # # moving_pad = ants.pad_image(moving_norm, pad_width=pad_width)
    
    # # print("Fixed shape:", fixed_norm.shape)
    # # print("Moving (padded) shape:", moving_pad.shape)
    # # print("Estimated memory use (MB):", (fixed_norm.numpy().nbytes + moving_pad.numpy().nbytes) / 1e6)


    # # ----------------------------- resume to registration -----------------------------
    print('Rigid registration ...')
    rigid_registration, fixed_norm = DA_edit_library_registration_cmpk2.rigid_registration(mapZebrain_ants, volume_mean_ants, pad_width,output_folder, stim=stim)
    print('Done with Rigid registration!\n\n------------------\n\n')
    
    # print('Affine registration ...')
    # affine_registration = DA_edit_library_registration_cmpk2.affine_registration(rigid_registration, fixed_norm, proj_ID, expt_ID, stim=stim)
    # print('Done with Affine registration!\n\n------------------\n\n')

    # print('Elastic registration ...')
    # els_registration = DA_edit_library_registration_cmpk2.elastic_registration_confocal(affine_registration, fixed_norm, proj_ID, expt_ID, stim=stim)
    # print('Done with Elastic registration!\n\n------------------\n\n')

    # print('Creating image ...')
    # DA_edit_library_registration_cmpk2.create_image(proj_ID, expt_ID, mapZebrain_ants)
    # print('Done with creating image!\n\n------------------\n\n')

    # print('Done with registration!')