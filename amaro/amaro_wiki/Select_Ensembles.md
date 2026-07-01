# Select Ensembles

#### Overview: The Ensemble Selection Problem[edit](</mediawiki/index.php?title=Select_Ensembles&action=edit&section=1> "Edit section: Overview: The Ensemble Selection Problem")]

When a subset of k items is selected from a larger set of N items, the number of ways of selecting that subset is described by the binomial coefficient, N!/k!(N-k)!. This is exactly the nature of the ensemble selection problem, and the binomial coefficient provides the number of ensembles of a given size that can be constructed. When the number of receptor conformations is large, the combinatorial nature of the problem results in a significant number of possible ensembles. Since it is difficult or impossible to know a priori, ensemble selection can be challenging. Three knowledge-based ensemble training methods are available to address this challenge. 

#### Training Methods[edit](</mediawiki/index.php?title=Select_Ensembles&action=edit&section=2> "Edit section: Training Methods")]

[Exhaustive](</mediawiki/index.php/Exhaustive> "Exhaustive"): All combinatorial possibilities are evaluated, and the best performing ensembles at each size are retained. The exhaustive method scales as O(2N). 

[Slow heuristic](</mediawiki/index.php/Slow_heuristic> "Slow heuristic"): The performance of each ensemble is considered individually, and the best performer becomes the first ensemble member. Next, the remaining receptor conformations are added in turn, forming a series of two-membered ensembles, and the best performer is retained. The process is repeated until all receptor conformations have been added to the ensemble. The slow heuristic method scales as O(N2). 

[Fast heuristic](</mediawiki/index.php/Fast_heuristic> "Fast heuristic"): The performance of each ensemble is considered individually, and the best performer becomes the first ensemble member. Ensembles of increasing size are then constructed by merging conformations of successively decreasing performance. The fast heuristic method scales as O(N).
