# Graph Theory 

Here, you will find the notebooks I used for quanityfing the graph theory metrics. The data used here is from the registration output, where cells are region-assigned. The time series of each region-assigned cell is used for averaging the activity in each region. 

A cross-correlation matrix for all brain regions can be constructed. A correlation coefficient threshold value is set (for example, .85 is a fairly strict threshold) and any region correlation values below the threshold are set to zero. 

This adapted weighted matrix is then used to created the undirected, weighted graph. I calculated the strength and weighted clustering coefficient metrics.
