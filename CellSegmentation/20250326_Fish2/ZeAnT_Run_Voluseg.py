# Import relevant libraries
import os
import voluseg

# --------------- Setting up parameters ---------------

fish_folder = os.path.join(os.getcwd())
tutorial_folder = os.path.dirname(fish_folder)

parameters0 = voluseg.parameter_dictionary()
parameters0['dir_ants'] = os.path.join(tutorial_folder, 'install/bin/')
parameters0['dir_input'] = os.path.join(fish_folder, 'input/')
parameters0['dir_output'] = os.path.join(fish_folder, 'output/')
parameters0['registration'] = 'high'
parameters0['diam_cell'] = 6.0 #diam_cell is the diameter of the cell in microns. The default is 6.0.
                               #I would recommend keeping it at 6.0. I tried 5.0 too but I stick to 6.0.
                               
parameters0['f_volume'] = 1 #Temporal resolution in Hz. In my case, it is 1 sec per volume, so f_volume = 1
parameters0['t_section'] = 0.02 #t_section is the exposure time per plane. In my case, it is 1 sec per volume. 50 planes per volume.
                                #t_section  = 1sec/50planes = 0.02 seconds per plane
parameters0['ds'] = 1 #ds is down-sampling. I usually do not downsample, that is why it is 1. If you choose 2, it would downstable by 2.
parameters0['res_x'] = 1.52*1 #res_x is our microscope resolution in x which is 1.52 if you use binning =1 (i.e. no binning).
                              #If you used binning = 2 during your imaging, it would be 1.52*2
parameters0['res_y'] = 1.52*1  #res_x is our microscope resolution in y which is 1.52. Binning same as in x.
parameters0['res_z'] = 5       #res_z =  z_range per volume in microns divided by number of planes.
                               #z_range is the parameter in MATLAB in the acquisition computer that we use to specify the span in microns.
                               #In my case, res_z = 250 microns per vol/50 planes = 5 microns per one plane.
                               

# --------------- Running Initial ---------------

print('Running step0_process_parameters() ...')
voluseg.step0_process_parameters(parameters0)
print('Parameters0: {0}\n--------------------\n'.format(parameters0))

# load and print parameters
filename_parameters = os.path.join(parameters0['dir_output'], 'parameters.pickle')
parameters = voluseg.load_parameters(filename_parameters)
print('Parameters: {0}\n--------------------\n'.format(parameters))

# 
print('Running step1_process_volumes ...')
voluseg.step1_process_volumes(parameters)
print('---- Ran step1 successfully!')
print('Running step2_align_volumes ...')
voluseg.step2_align_volumes(parameters)
print('---- Ran step2 successfully!')
print('Running step3_mask_volumes ...')
voluseg.step3_mask_volumes(parameters)
print('Running step4_detect_cells ...')
voluseg.step4_detect_cells(parameters)
print('Running step5_clean_cells ...')
voluseg.step5_clean_cells(parameters)
print('Voluseg is complete!')