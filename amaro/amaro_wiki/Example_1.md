# Example 1

To generate a table describing the performance of each ensemble, one or mores CSV files that contain the ensemble(s) selected using either the [exhaustive](</mediawiki/index.php/Exhaustive> "Exhaustive"), [slow heuristic](</mediawiki/index.php/Slow_heuristic> "Slow heuristic") or [fast heuristic](</mediawiki/index.php/Fast_heuristic> "Fast heuristic") methods, along with an [input](</mediawiki/index.php/Input> "Input") are required. Assume fh_1_queries.csv and fh_2_queries.csv contain two ensembles selected using the fast heuristic method ([generated here](</mediawiki/index.php/Fast_heuristic#Example> "Fast heuristic")), their performance can be determined on the training_set (found [here](<https://github.com/rvswift/EB/blob/master/data/training_set.csv>)) using the following command 
    
    
    ensemblebuilder postanalysis --input training_set.cv --ensemble_list fh_1_queries.csv fh_2_queries.csv

The file fh_stats.csv file is produced. It can be viewed using a spreadsheet editor. The results are shown below 

[![Fh stats.png](/mediawiki/images/thumb/a/a2/Fh_stats.png/600px-Fh_stats.png)](</mediawiki/index.php/File:Fh_stats.png>)

The contents of each column are described below. 

    Ensemble name: The name of the ensemble, taken from the filenames specified by the --ensemble_list flat
    AUC: The [AUC](<https://en.wikipedia.org/wiki/Receiver_operating_characteristic#Area_under_the_curve>) of the ROC curve.
    95% CI: The 95% confidence interval of the AUC.
    E0.001: The ROC enrichment factor determined at a false positive fraction of 0.001.
    95% CI: The 95% confidence interval of the ROC enrichment factor at a false positive fraction of 0.001.
    E0.01: The ROC enrichment factor determined at a false positive fraction of 0.01.
    95% CI: The 95% confidence interval of the ROC enrichment factor at a false positive fraction of 0.01.
    E0.05: The ROC enrichment factor determined at a false positive fraction of 0.05.
    95% CI: The 95% confidence interval of the ROC enrichment factor at a false positive fraction of 0.05
