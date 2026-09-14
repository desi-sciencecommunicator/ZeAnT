# Cell Segmentation 
All credit for the cell segmentation software goes Dr. Rubinov and colleagues. Reference: DOI: 10.1016/j.cell.2019.05.050. Mu Y*, Bennett DV*, Rubinov M*, Narayan S, Yang CT, Tanimoto M, Mensh BD, Looger LL, Ahrens MB. Glia accumulate evidence that actions are futile and suppress unsuccessful behavior. Cell 2019 178:27-43.


### Edited Voluseg files 
Because I am hosting Voluseg in Caltech's Resnick HPC and using GPU resources, I removed (or commented out) any lines that initiate a pySpark session. These edits are included inside Voluseg's source code, specifically in the directory /_steps/. Edits were made to the following files: 

* step3.py
* step4.py
* step4e.py
* step5.py

### Running Voluseg in Caltech's Resnick HPC 
Once the Voluseg source code /_steps/ files are edited, the following steps should be followed 
1. Use the data_preparation.ipynb file to input the data and format it into a series of .hdf5 files
2. Run Voluseg using the ZeAnT_Run_Voluseg.sh script. There is a field where you should specificy the path of the /output/ folder


### Notes for developers 
* The data preparation step using the data_preparation.ipynb notebook can be done in a python script to remove any manual intervention for this preparation step. The single advantage to using the notebook for data preparation is that it is easier to catch any errors in the way the light-sheet sequentially scanned the brain along the z-axis. 
