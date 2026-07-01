# Example 4

To generate a CSV file with ROC data points, one or more CSV files that contain the ensembles selected using either the exhaustive, slow heuristic or fast heuristic methods, along with an input are required. Assume fh_1_queries.csv and fh_2_queries.csv contain two ensembles selected using the fast heuristic method (generated here), CSV files with ROC data points can be generated using the training_set (found here) using the following command 
    
    
    ensemblebuilder postanalysis --input ../training_set.csv --outname fh --ensemble_list fh_2_queries.csv --write_roc

A directory named "ROC_DATA" will be generated, and a file named "fh_2_queries_roc.csv" can be found there. This file can be viewed using a spreadsheet program. The results are shown below 

[![Roc data.png](/mediawiki/images/thumb/b/b3/Roc_data.png/600px-Roc_data.png)](</mediawiki/index.php/File:Roc_data.png>)

The contents of each column are described below. 

    id: Contains the unique alphanumeric columns of each compound.
    score: The ensemble score of each column.
    score source: The receptor conformation from which the ensemble score was taken.
    status: The experimental status of the compound. A '1' denotes an active compound while a '0' denotes an inactive compound.
    fpf: The false positive fraction of the compound.
    tpf: The true positive fraction of the compound.
    Status API Training Shop Blog About Pricing
