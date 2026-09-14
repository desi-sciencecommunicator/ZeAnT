# Cell Segmentation 
All credit for the cell segmentation software goes Dr. Rubinov and colleagues. Reference: DOI: 10.1016/j.cell.2019.05.050. Mu Y*, Bennett DV*, Rubinov M*, Narayan S, Yang CT, Tanimoto M, Mensh BD, Looger LL, Ahrens MB. Glia accumulate evidence that actions are futile and suppress unsuccessful behavior. Cell 2019 178:27-43.


### Edited Voluseg files 
Because I am hosting Voluseg in Caltech's Resnick HPC and using GPU resources, I removed (or commented out) any lines that initiate a pySpark session. These edits are included inside Voluseg's source code, specifically in the directory /_steps. Edits were made to the following files: 

* step3.py
* step4.py
* step4e.py
* step5.py

