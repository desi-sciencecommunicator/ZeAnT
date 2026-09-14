s#!/usr/bin/env python
# coding: utf-8

# In[1]:


from skimage import io
from scipy.cluster.vq import kmeans2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mc

# get_ipython().run_line_magic('matplotlib', 'inline')
plt.ion()

import os
import multiprocessing
num_cores = multiprocessing.cpu_count()
print("Number of cores:", num_cores)
os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = str(num_cores)

import pandas as pd
import h5py
from PIL import Image
import skimage.io as skio
from skimage import io
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
import ants
import sys

# ===============================
fr_per_vol = 25
sec_per_vol = 1
z_range = 250
binning = 1

# ========== Parameters ==========
binning=1
res_x=0.585*binning
res_y=0.585*binning
res_z=250/25

# base = '/central/groups/Proberlab/Yun/'
base = '/central/groups/Proberlab/dascenci/'

import os 

def create_folder(ants_folder, proj_ID, expt_ID):
    '''
    ants_folder = str, path to folder where to save relevant ANTS output 
    proj_ID = str, projectID - genetic line is appropriate 
    expt_ID = str, experiment ID, a combination of the imaging date and fish sample ID 

    returns output_folder, str, path to where the output folder was created or ID'd to be at
    '''
    
    output_folder = ants_folder + proj_ID + '/' + expt_ID + '/'
    print('Stitched output_folder path: ', output_folder)
    
    try:
        os.makedirs(output_folder)
        print('Created folder: ', output_folder)
    except:
        print('Folder exists: ', output_folder)

    return output_folder

import numpy as np
from skimage import io
import ants
import matplotlib.pyplot as plt

def load_mapzebrain_reference_brain(mapZebrain_template_path, save_fig=False, to_save_folder=None):
    '''
    mapZebrain_template_path: str, Pass in the file path and name for the reference brain
    save_fig: bool, to save in same folder as output folder
    to_save_folder: None default, if save_fig, then have to pass in the output folder
    '''
    # print('MAPZEBRAN: ', mapZebrain_name)
    mapZebrain_name = mapZebrain_template_path.split('.')[0].split('/')[-1]

    mapZebrain_file = io.imread(mapZebrain_template_path)
    print('Reading mapZebrain_file shape: ', np.shape(mapZebrain_file)) #=> ANTs read data as XYZ (512, 265, 60)

    mapZebrain_file = np.transpose(mapZebrain_file, axes=(1, 2, 0))
    print(mapZebrain_file.shape)
    
    mapZebrain_ants = ants.from_numpy(np.asarray(mapZebrain_file, dtype='float'))
    mapZebrain_ants.set_spacing((0.9940709, 0.9939616, 1)) # from ZBrain paper / outside sources"
    
    # get_ipython().run_line_magic('matplotlib', 'inline')
    plt.close()
    plt.figure()
    plt.imshow(mapZebrain_ants.numpy()[:, :, 130])
    plt.title('Load Reference Brain: '+str(mapZebrain_name))
    if save_fig == True:
        assert to_save_folder is not None, 'Must pass path to save figure to parameter to_save_folder!'
        figure_save_path = to_save_folder + mapZebrain_name + '.pdf'
        print('Saving figure to : {0}'.format(figure_save_path))
        plt.savefig(figure_save_path)
    
    plt.show()

    return mapZebrain_ants


# In[3]:


import h5py
import numpy as np
import ants

def load_volume_mean(volume_path, pixel_size, depth, num_slice, save_fig=False, to_save_folder=None):
    '''
    volume_path: str, path to volume hdf5 file with shape slice, y-dim, x-dim
        axes get swapped to format acceptable for ants

    '''
    # base = '/central/groups/Proberlab/Yun/'
    # base = '/central/groups/Proberlab/dascenci/'
    
    binning=1
    res_x=pixel_size*binning
    res_y=pixel_size*binning
    res_z=depth/num_slice

    ### access the the 'volume_mean' in order to register it to the mapzebrain space later 
    with h5py.File(volume_path, "r") as f:
        print("Keys: %s" % f.keys())
        volume_mean = f["default"][:]
    # print(np.shape(volume_mean))

    volume_mean = np.swapaxes(volume_mean, 0, 2)
    print(np.shape(volume_mean))
    volume_mean_ants = ants.from_numpy(np.asarray(volume_mean, dtype='float'))
    #volume_mean_ants.set_spacing((0.9940709, 0.9939616, 1))
    volume_mean_ants.set_spacing((res_x, res_y, res_z))
    # Rotate the brain for 180 degrees
    rotated_data = np.rot90(volume_mean_ants.numpy(), k=2, axes=(0, 1))  # k=2 means 180 degrees rotation
    volume_mean_ants = ants.from_numpy(rotated_data)
    
    plt.close()
    plt.figure()
    plt.imshow(volume_mean_ants.numpy()[:, :, 15])
    plt.title('volume mean ants example slice')
    if save_fig == True:
        assert to_save_folder is not None, 'Must pass path to save figure to parameter to_save_folder!'
        figure_save_path = to_save_folder +  'MapZebrain.pdf'
        print('Saving figure to : {0}'.format(figure_save_path))
        plt.savefig(figure_save_path)
    plt.show()

    return volume_mean_ants



# def load_els_template(template_path, output_folder):
#     '''
#     Very roughly written for use-case, make better later 
    
#     template_path: str, path to numpy file 
#     '''

#     print('    - Loading els template from path: {0}'.format(template_path))

#     binning=1
#     res_x=1.62*binning
#     res_y=1.62*binning
#     res_z=250/63

#     template_npy = np.load(template_path)
    
#     print("Template shape: {0}".format(template_npy.shape))
    
#     template_npy = np.swapaxes(template_npy, 0, 2)
#     print('After swapping axes, template shape: {0}'.format(np.shape(template_npy)))
    
#     template_ants = ants.from_numpy(np.asarray(template_npy, dtype='float'))
#     #volume_mean_ants.set_spacing((0.9940709, 0.9939616, 1))
#     template_ants.set_spacing((res_x, res_y, res_z))
    
#     plt.figure()
#     plt.imshow(template_ants.numpy()[:, :, 15])
#     plt.title('volume mean ants example slice')
#     plt.show()

#     # Rotate the brain for 180 degrees
#     rotated_data = np.rot90(template_ants.numpy(), k=2, axes=(0, 1))  # k=2 means 180 degrees rotation
#     template_ants = ants.from_numpy(rotated_data)

#     # Visualize the rotated result
#     plt.imshow(template_ants.numpy()[:, :, 15])  # Adjust slice as necessary
#     plt.title('Rotated 180 degrees - volume mean ants example slice')
#     plt.savefig(output_folder + 'ants_template.png')
#     plt.show()

#     return volume_mean_ants





def load_volume_mean_USC(proj_ID, expt_ID):

    # base = '/central/groups/Proberlab/Yun/'
    # base = '/central/groups/Proberlab/dascenci/mufanw_copy/optogenetic_analysis/ANTS_output/'

    # dir_output = base + proj_ID + '/' + expt_ID + '/' + 'output/'

    hdf5_path = '/central/groups/Proberlab/dascenci/mufanw_copy/optogenetic_analysis/ANTS_output/hcrt-reachr/240926_hcrt-reachr_huc-h2b-g7f_USC_fish3/output/volume0.hdf5'

    binning=1
    res_x=1.62*binning
    res_y=1.62*binning
    res_z=250/63

    ### access the the 'volume_mean' in order to register it to the mapzebrain space later 
    with h5py.File(hdf5_path, "r") as f:
        print("Keys: %s" % f.keys())
        volume_mean = f["volume_mean"][()]
    print(np.shape(volume_mean))
    
    #print(np.shape(volume_mean))
    volume_mean = np.swapaxes(volume_mean, 0, 2)
    print(np.shape(volume_mean))
    
    volume_mean_ants = ants.from_numpy(np.asarray(volume_mean, dtype='float'))
    #volume_mean_ants.set_spacing((0.9940709, 0.9939616, 1))
    volume_mean_ants.set_spacing((res_x, res_y, res_z))
    
    plt.figure()
    plt.imshow(volume_mean_ants.numpy()[:, :, 15])
    plt.title('volume mean ants example slice')
    plt.show()

    # Rotate the brain for 180 degrees
    rotated_data = np.rot90(volume_mean_ants.numpy(), k=2, axes=(0, 1))  # k=2 means 180 degrees rotation
    volume_mean_ants = ants.from_numpy(rotated_data)

    # Visualize the rotated result
    plt.imshow(volume_mean_ants.numpy()[:, :, 15])  # Adjust slice as necessary
    plt.title('Rotated 180 degrees - volume mean ants example slice')
    plt.show()

    return volume_mean_ants

def load_volume_mean_confocal(proj_ID, expt_ID, fish_ID, pixel_size, depth, num_slice, reference_channel):

    # base = '/central/groups/Proberlab/Yun/confocal/data/'
    base = '/central/groups/Proberlab/dascenci/mufanw_copy/optogenetic_analysis/ANTS_output/'

    confocal_file_path = base + proj_ID + '/' + expt_ID + '/' + fish_ID

    binning=1
    res_x=pixel_size*binning
    res_y=pixel_size*binning
    res_z=depth/num_slice

    ### Load the reference channel of the .czi file as numpy array
    from aicsimageio import AICSImage
    # Get an AICSImage object
    img = AICSImage(confocal_file_path)

    # Only load the reference channel (tERK)
    ref_channel_data = img.get_image_data("ZYX", C=reference_channel, S=0, T=0)
    print("Loaded reference channel as numpy array, original shape (ZYX): ", ref_channel_data.shape)
    
    volume_mean = np.swapaxes(ref_channel_data, 0, 1) # (ZYX) -> (YZX)
    print("Swapped axes to (YZX):", np.shape(volume_mean))
    
    volume_mean = np.swapaxes(volume_mean, 1, 2) # (YZX) -> (YXZ)
    print("Swapped axes (YXZ):", np.shape(volume_mean))
    
    volume_mean_ants = ants.from_numpy(np.asarray(volume_mean, dtype='float'))
    #volume_mean_ants.set_spacing((0.9940709, 0.9939616, 1))
    volume_mean_ants.set_spacing((res_x, res_y, res_z))
    
    plt.figure()
    plt.imshow(volume_mean_ants.numpy()[:, :, 15])
    plt.title('Volume mean ants example slice: ')
    plt.show()

    return volume_mean_ants


import math

def get_padding_width(mapZebrain_ants, volume_mean_ants, save_fig=False, to_save_folder=None):
    y1, x1, z1 = mapZebrain_ants.shape
    y2, x2, z2 = volume_mean_ants.shape
    
    print(mapZebrain_ants.shape)
    print(volume_mean_ants.shape)
    
    # Calculate padding values (based on the above calculation)
    pad_width = [(math.floor((y1-y2)/2), math.floor((y1-y2)/2)), (math.floor((x1-x2)/2), math.floor((x1-x2)/2)), (math.floor((z1-z2)/2), math.floor((z1-z2)/2))]  # (Y, X, Z) padding
    print(pad_width)

    plt.close()
    plt.figure()
    plt.imshow(volume_mean_ants.numpy()[:, :, 15], cmap="gray")
    plt.title('Padding Width')
    plt.colorbar()
    if save_fig == True:
        assert to_save_folder is not None, 'Must pass path to save figure to parameter to_save_folder!'
        figure_save_path = to_save_folder +  'Padding.pdf'
        print('Saving figure to : {0}'.format(figure_save_path))
        plt.savefig(figure_save_path)
    plt.show()

    return pad_width 


def reshape_image(mapZebrain_ants, volume_mean_ants):
    physical_sizes_ref = [dim * sp for dim, sp in zip(mapZebrain_ants.shape, mapZebrain_ants.spacing)]
    physical_sizes_volume = [dim * sp for dim, sp in zip(volume_mean_ants.shape, volume_mean_ants.spacing)]

    padding_physical = [ref - vol for ref, vol in zip(physical_sizes_ref, physical_sizes_volume)]
    padding_voxels = [
        int(np.round(pad / sp)) if pad > 0 else 0
        for pad, sp in zip(padding_physical, volume_mean_ants.spacing)
    ]
    
    pad_x = padding_voxels[0]
    pad_y = padding_voxels[1]
    pad_z = padding_voxels[2]
    padding_tuples = [
        (pad_x // 2, pad_x - pad_x // 2),  # Split padding evenly on both sides (x-axis)
        (pad_y // 2, pad_y - pad_y // 2),  # Split padding evenly on both sides (y-axis)
        (pad_z, 0)                         # Add padding only at the beginning (z-axis)
    ]

    padded_array = np.pad(
        volume_mean_ants.numpy(),  # Convert ANTsImage to NumPy array
        pad_width=padding_tuples, # Use calculated padding
        mode="constant",          # Zero padding (you can customize this if needed)
        constant_values=0
    )
    padded_image = ants.from_numpy(
        padded_array,
        origin=volume_mean_ants.origin,
        spacing=volume_mean_ants.spacing,
        direction=volume_mean_ants.direction
    )

    return padded_image, padding_tuples


# In[20]:


import ants


def rigid_registration(mapZebrain_ants, volume_mean_ants, pad_width,
output_folder, stim=-1):

    #dir_ants_output = f"/central/groups/Proberlab/mufanw/optogenetic_analysis/ANTS_output/{proj_ID}/{expt_ID}/"
    # dir_ants_output = f"/central/groups/Proberlab/Yun/mufanw_copy/optogenetic_analysis/ANTS_output/{proj_ID}/{expt_ID}/"
    dir_ants_output = output_folder

    print('Rigid registration called!')
    
    fixed_norm = ants.iMath_normalize(mapZebrain_ants)
    moving_norm = ants.iMath_normalize(volume_mean_ants)
    moving_pad = ants.pad_image(moving_norm, pad_width=pad_width)
    #moving_pad = moving_norm
    
    ### Step 1: Rigid Registration ###
    rigid_registration = ants.registration(
        fixed=fixed_norm,
        moving=moving_pad,
        type_of_transform="Rigid",
        metric="MI",
        sampling_strategy="Regular",
        sampling_percentage=0.25,
        reg_iterations=(200, 200, 200, 0),
        shrink_factors=(12, 8, 4, 2),
        smoothing_sigmas=(4, 3, 2, 1),
        use_histogram_matching=False,
        interpolation="WelchWindowedSinc",
        verbose=True
    )
    
    # Save rigid transformation matrix
    rigid_matrix = rigid_registration['fwdtransforms'][0]  # Only one file (transformation matrix) for Rigid
    
    if stim == -1:
        shutil.copy(rigid_matrix, dir_ants_output + "rigid_transform.mat")
    else:
        shutil.copy(rigid_matrix, dir_ants_output + f"rigid_transform_stim_{stim}.mat")
    print(f"Rigid transform matrix saved: {rigid_matrix}")

    return rigid_registration['warpedmovout'], fixed_norm

def affine_registration(rigid_registration, fixed_norm, proj_ID, expt_ID, stim=-1):

    #dir_ants_output = f"/central/groups/Proberlab/mufanw/optogenetic_analysis/ANTS_output/{proj_ID}/{expt_ID}/"
    # dir_ants_output = f"/central/groups/Proberlab/Yun/mufanw_copy/optogenetic_analysis/ANTS_output/{proj_ID}/{expt_ID}/"
    dir_ants_output = f"/central/groups/Proberlab/dascenci/mufanw_copy/optogenetic_analysis/ANTS_output/{proj_ID}/{expt_ID}/"

    
    ### Step 2: Affine Registration ###
    affine_registration = ants.registration(
        fixed=fixed_norm,
        moving=rigid_registration,
        type_of_transform="Affine",
        metric="MI",
        sampling_strategy="Regular",
        sampling_percentage=0.25,
        reg_iterations=(200, 200, 200, 0),
        shrink_factors=(12, 8, 4, 2),
        smoothing_sigmas=(4, 3, 2, 1),
        use_histogram_matching=False,
        interpolation="WelchWindowedSinc",
        verbose=True
    )
    
    # Save affine transformation matrix
    affine_matrix = affine_registration['fwdtransforms'][0]  # Only one file (transformation matrix) for Affine
    if stim == -1:
        shutil.copy(affine_matrix, dir_ants_output + "affine_transform.mat")
    else:
        shutil.copy(affine_matrix, dir_ants_output + f"affine_transform_stim_{stim}.mat")
    print(f"Affine transform matrix saved: {affine_matrix}")

    return affine_registration['warpedmovout']


def syn_registration(affine_registration, fixed_norm, proj_ID, expt_ID, stim=-1):

    #dir_ants_output = f"/central/groups/Proberlab/mufanw/optogenetic_analysis/ANTS_output/{proj_ID}/{expt_ID}/"
    # dir_ants_output = f"/central/groups/Proberlab/Yun/mufanw_copy/optogenetic_analysis/ANTS_output/{proj_ID}/{expt_ID}/"
    dir_ants_output = f"/central/groups/Proberlab/dascenci/mufanw_copy/optogenetic_analysis/ANTS_output/{proj_ID}/{expt_ID}/"

    ### Step 3: SyN Registration ###
    
    syn_registration = ants.registration(
        fixed=fixed_norm,
        moving=affine_registration,
        type_of_transform="Elastic",
        metric="CC",  # Switch to Mutual Information for faster computation
        sampling_strategy="Regular",
        sampling_percentage=0.1,  # Use only 10% of pixels
        reg_iterations=(200, 200, 200, 200, 10),  # Reduce iterations
        shrink_factors=(12, 8, 4, 2, 1),  # Fewer pyramid levels
        smoothing_sigmas=(4, 3, 2, 1, 0),  # Increase smoothing
        use_histogram_matching=False,  # Skip histogram matching
        interpolation="WelchWindowedSinc",
        verbose=True,
    )

    syn_warp = syn_registration['fwdtransforms'][0]  # warp field (.nii.gz)
    syn_affine = syn_registration['fwdtransforms'][1]  # transformation matrix (.mat)
    if stim == -1:
        shutil.copy(syn_warp, dir_ants_output + "syn_warp_field.nii.gz")
        shutil.copy(syn_affine, dir_ants_output + "syn_affine_transform.mat")
        ants.image_write(syn_registration['warpedmovout'], dir_ants_output + expt_ID + '_registered.nii.gz', ri=False)
    else:
        shutil.copy(syn_warp, dir_ants_output + f"syn_warp_field_stim_{stim}.nii.gz")
        shutil.copy(syn_affine, dir_ants_output + f"syn_affine_transform_stim_{stim}.mat")
        ants.image_write(syn_registration['warpedmovout'], dir_ants_output + expt_ID + f'_registered_stim_{stim}.nii.gz', ri=False)
        
    print(f"SyN warp field saved: {syn_warp}")
    print(f"SyN affine transform saved: {syn_affine}")
    print("Final registered image saved!")
    
    return syn_registration['warpedmovout']

def elastic_registration_confocal(mapZebrain_ants, volume_mean_ants, proj_ID, expt_ID, stim=-1):

    #dir_ants_output = f"/central/groups/Proberlab/mufanw/optogenetic_analysis/ANTS_output/{proj_ID}/{expt_ID}/"
    # dir_ants_output = f"/central/groups/Proberlab/Yun/confocal/data/{proj_ID}/{expt_ID}/registered/"
    dir_ants_output = f"/central/groups/Proberlab/dascenci/confocal/data/{proj_ID}/{expt_ID}/registered/"
    fixed_norm = ants.iMath_normalize(mapZebrain_ants)
    moving_norm = ants.iMath_normalize(volume_mean_ants)

    # print(f"Processing {fish_ID}: Starting Elastic Registration...")
    sys.stdout.flush()    

    ### One Step Elastic Registration ###
    
    els_registration = ants.registration(
        fixed=fixed_norm,
        moving=moving_norm,
        type_of_transform="Elastic",
        metric="CC",  # Switch to Mutual Information for faster computation
        sampling_strategy="Regular",
        sampling_percentage=0.05,  # Use only 10% of pixels
        reg_iterations=(100, 50, 10),  # Reduce iterations
        shrink_factors=(8, 4, 2, 1),  # Reduce number of pyramid levels
        smoothing_sigmas=(3, 2, 1, 0),  # Increase smoothing
        use_histogram_matching=False,
        interpolation="WelchWindowedSinc",
        verbose=True,
    )
    


    els_warp = els_registration['fwdtransforms'][0]  # warp field (.nii.gz)
    els_affine = els_registration['fwdtransforms'][1]  # transformation matrix (.mat)

    shutil.copy(els_warp, dir_ants_output  + "_els_warp.nii.gz")
    shutil.copy(els_affine, dir_ants_output + "_els_transform.mat")
    ants.image_write(els_registration['warpedmovout'], dir_ants_output + fish_ID + '_registered.nii.gz', ri=False)

    print(f"Elastic warp field saved: {els_warp}")
    print(f"Elastic affine transform saved: {els_affine}")
    print("Final registered image saved!")
    
    return els_registration['warpedmovout']


# In[21]:


import nibabel as nib
import matplotlib.pyplot as plt
import os

def create_image(proj_ID, expt_ID, mapZebrain_ants, stim=-1):

    #dir_ants_output = f"/central/groups/Proberlab/mufanw/optogenetic_analysis/ANTS_output/{proj_ID}/{expt_ID}/"
    # dir_ants_output = f"/central/groups/Proberlab/Yun/confocal/data/{proj_ID}/{expt_ID}/registered/"
    dir_ants_output = f"/central/groups/Proberlab/dascenci/confocal/data/{proj_ID}/{expt_ID}/registered/"
    file_path = dir_ants_output + exp_ID + '_registered.nii.gz'

    if os.path.exists(file_path):
        print("The path exists.")
    else:
        print("The path does not exist.")
    
    img = nib.load(file_path)
    data = img.get_fdata()
    
    z = 50

    slice_data = mapZebrain_ants.numpy()[:, :, :]
    print("Size of the slice:", slice_data.shape)

    slice_data = data[:, :, :]
    print("Size of the slice:", slice_data.shape)

    plt.figure()
    plt.imshow(data[:, :, z], cmap='viridis', alpha=0.9)
    plt.tight_layout()
    if stim == -1:
        plt.title(f'Transformed Image (z = 240) \n {fish_ID}')
        plt.savefig(f"/central/groups/Proberlab/dascenci/confocal/data/{proj_ID}/{expt_ID}/figures_registration/transformed_image_{fish_ID}_{z}.pdf")
    else:
        plt.title(f'Transformed Image (z = 240, Stim {stim}) \n {expt_ID}')
        plt.savefig(f"../figures_registration/transformed_image_{z}_{proj_ID}_{expt_ID}_stim_{stim}.pdf")


# In[22]:


def get_new_index_after_padding(coord, padding_tuples):

    pad_x_left, _ = padding_tuples[0]
    pad_y_left, _ = padding_tuples[1]
    pad_z_left, _ = padding_tuples[2]


    if isinstance(coord, tuple):
        x, y, z = coord
        new_x = x + pad_x_left
        new_y = y + pad_y_left
        new_z = z + pad_z_left
        
        return (new_x, new_y, new_z)
        
    if isinstance(coord, pd.DataFrame):
        coord['x'] = coord['x'] + pad_x_left
        coord['y'] = coord['y'] + pad_y_left
        coord['z'] = coord['z'] + pad_z_left
    
        return coord

    return None


# In[ ]:




