# Example 3

To generate PDF files that contain ROC plots of each input ensemble, CSV files that contain the ensemble(s) selected using either the exhaustive, slow heuristic or fast heuristic methods, along with an input are required. Assume fh_2_queries.csv contains a two-membered ensemble selected using the fast heuristic method (generated here), the ROC curve describing it's performance on the training set found here) can be generated using the following command 
    
    
    ensemblebuilder postanalysis --input ../training_set.csv --outname roc --ensemble_list fh_2_queries.csv --plot

The PDF file, roc_fh_2_queries.pdf is generated. It can be opened using any pdf viewer. The results are shown below 

[![Roc.png](/mediawiki/images/thumb/0/00/Roc.png/600px-Roc.png)](</mediawiki/index.php/File:Roc.png>)
