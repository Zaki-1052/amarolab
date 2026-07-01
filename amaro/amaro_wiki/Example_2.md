# Example 2

To generate a table comparing the performance of each ensemble, exactly two CSV files that contain the ensembles selected using either the [exhaustive](</mediawiki/index.php/Exhaustive> "Exhaustive"), [slow heuristic](</mediawiki/index.php/Slow_heuristic> "Slow heuristic") or [fast heuristic](</mediawiki/index.php/Fast_heuristic> "Fast heuristic") methods, along with an [input](</mediawiki/index.php/Input> "Input") are required. Assume fh_1_queries.csv and fh_2_queries.csv contain two ensembles selected using the fast heuristic method ([generated here](</mediawiki/index.php/Fast_heuristic#Example> "Fast heuristic")), their performance can be determined on the training_set (found [here](<https://github.com/rvswift/EB/blob/master/data/training_set.csv>)) using the following command 
    
    
    ensemblebuilder postanalysis --input ../training_set.csv --outname fh --ensemble_list fh_1_queries.csv fh_2_queries.csv --compare

The file fh_diff_stats.csv is produced. It can be viewed using a spreadsheet editor. The results are shown below 

[![Fh diff stats.png](/mediawiki/images/thumb/1/1f/Fh_diff_stats.png/600px-Fh_diff_stats.png)](</mediawiki/index.php/File:Fh_diff_stats.png>)

The contents of each column are described below. 

    column one: The first column contains the names of ROC derived classification performance metrics. AUC is the area under the ROC curve. E0.001, E0.01, and E0.05 are the ROC enrichment factors at false positive fractions of 0.001, 0.01, and 0.05.
    fh_1_queries: Contains the values of the ROC derived classification performance metrics for the ensemble contained in the file fh_1_queries.csv.
    fh_2_queries: Contains the values of the ROC derived classification performance metrics for the ensemble contained in the file fh_2_queries.csv.
    Difference: The difference between the performance values of each ensemble. The fh_2_queries values are subtracted from the fh_1_queries values.
    95% CI: The 95% confidence intervals of the differences
    p-value: The one-sided p-values of the differences.
