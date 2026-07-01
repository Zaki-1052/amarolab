# Training Ensembles

## Overview[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=1> "Edit section: Overview")]

The ensemble builder application encodes 3 knowledge-based methods that enumerate and select ensembles optimized for virtual screening (VS) performance. Currently, the application is tailored specifically for docking programs that report predicted binding free energies (e.g. -10 kcal/mol). Ensemble builder can generate training and test sets and analyze the classification performance using Receiver Operating Characteristic (ROC) based metrics. 

## Installation[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=2> "Edit section: Installation")]

### Installation prerequisites[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=3> "Edit section: Installation prerequisites")]

Numpy: [www.numpy.org](<http://www.numpy.org/>)

SciPy: [www.scipy.org](<http://www.scipy.org>)

### Install with pip[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=4> "Edit section: Install with pip")]
    
    
    pip install EB

### Install by cloning the GitHub repo[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=5> "Edit section: Install by cloning the GitHub repo")]
    
    
    git clone https://github.com/rvswift/EB
    
    cd EB
    
    make install

## Workflow[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=6> "Edit section: Workflow")]

### [Step 1: Create Training and Test Sets](</mediawiki/index.php/Create_Training_and_Test_Sets> "Create Training and Test Sets")[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=7> "Edit section: Step 1: Create Training and Test Sets")]

### [Step 2: Select Ensembles](</mediawiki/index.php/Select_Ensembles> "Select Ensembles")[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=8> "Edit section: Step 2: Select Ensembles")]

### [Step 3: Evaluate VS Performance](</mediawiki/index.php/Evaluate_VS_Performance> "Evaluate VS Performance")[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=9> "Edit section: Step 3: Evaluate VS Performance")]

### Step 4: Use the Vetted, Trained Ensemble to Perform a Prospective Screen[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=10> "Edit section: Step 4: Use the Vetted, Trained Ensemble to Perform a Prospective Screen")]

## Tutorial[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=11> "Edit section: Tutorial")]

### Required Files[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=12> "Edit section: Required Files")]

Input: [input.csv](<https://github.com/rvswift/EB/blob/master/data/andr_merged.csv>)

### Creating Training and Test Sets[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=13> "Edit section: Creating Training and Test Sets")]

The example input file, [input.csv](<https://github.com/rvswift/EB/blob/master/data/andr_merged.csv>), contains 112 active and 12681 inactive compounds, giving a decoy to active ratio of ~56. Running ensemble builder in the splitter mode with default values for the --training_fraction and --decoy_to_active flags: 
    
    
    ensemblebuilder splittter --input input.csv

produces [training_set.csv](<https://github.com/rvswift/EB/blob/master/data/training_set.csv>) and [test_set.csv](<https://github.com/rvswift/EB/blob/master/data/test_set.csv>), which each contain 112 active compounds and 6,272 inactive or decoy compounds and have decoy to active ratios of ~56. If you perform the example yourself, the compounds in the training and test sets will be different, since the active and decoy selection is random. However, the numbers of active and decoy compounds in each set should be the same. 

### Selecting Ensembles[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=14> "Edit section: Selecting Ensembles")]

There are three methods for selecting ensembles, exhaustive, fast heuristic, and slow heuristic. The details for running each of these are outlined below. 

#### Exhaustive[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=15> "Edit section: Exhaustive")]

To generate ensembles of size 1 through 3, optimized to produce the largest AUC, using two cpus, run the following command. 
    
    
    ensemblebuilder exhaustive --input training_set.csv --outname exh --ensemble_size 5 --fpf 1 --ncpu 2

If the command above is run with the example training set found [here](<https://github.com/rvswift/EB/blob/master/data/training_set.csv>), which contains docking scores from 10 receptor conformations, 3 files (exh_1_queries.csv, exh_2_queries.csv, and exh_3_queries.csv) should be produced. They should contain the following contents. 

    **exh_1_queries.csv** : receptor_8
    **exh_2_queries.csv** : receptor_8, receptor_2
    **exh_3_queries.csv** : receptor_10, receptor_8, receptor_2

Each file contains the receptor conformations that produce the largest AUC value of the indicated size. For example, of the 45 possible two-membered ensembles (10 choose 2), receptor_8 and receptor_2 make up the two-membered ensemble that produces the largest AUC value when the training set is screened. 

#### Slow Heuristic[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=16> "Edit section: Slow Heuristic")]

To generate ensembles of size 1 through 2, optimized to produce the largest EF at a false positive fraction of 0.01, run the following command. 
    
    
    ensemblebuilder slowheuristic --input training_set.cv --outname sh --ensemble_size 2 --fpf 0.01

If the command above is run with the example training set found [here](<https://github.com/rvswift/EB/blob/master/data/training_set.csv>), which contains docking scores from 10 receptor conformations, 2 files (sh_1_queries.csv, and sh_2_queries.csv) should be produced. They should contain the following contents. 

    **exh_1_queries.csv** : receptor_2
    **exh_2_queries.csv** : receptor_2, receptor_7

Each file contains the receptor conformations that produce the largest EF at a FPF of 0.01 of the indicated size. For example, receptor_2 and receptor_7 make up the two-membered ensemble that produces the largest EF at a FPF of 0.01 when the training set is screened. 

#### Fast Heuristic[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=17> "Edit section: Fast Heuristic")]

To generate ensembles of size 1 through 2, optimized to produce the largest EF at a false positive fraction of 0.01, run the following command. 
    
    
    ensemblebuilder slowheuristic --input training_set.cv --outname fh --ensemble_size 2 --fpf 0.01

If the command above is run with the example training set found [here](<https://github.com/rvswift/EB/blob/master/data/training_set.csv>), which contains docking scores from 10 receptor conformations, 2 files (fh_1_queries.csv, and fh_2_queries.csv) should be produced. They should contain the following contents. 

    **exh_1_queries.csv** : receptor_2
    **exh_2_queries.csv** : receptor_2, receptor_6

Each file contains the receptor conformations that produce the largest EF at a FPF of 0.01 of the indicated size. For example, receptor_2 and receptor_6 make up the two-membered ensemble that produces the largest EF at a FPF of 0.01 when the training set is screened. 

### Evaluating VS Performance[edit](</mediawiki/index.php?title=Training_Ensembles&action=edit&section=18> "Edit section: Evaluating VS Performance")]

[Example 1](</mediawiki/index.php/Example_1> "Example 1"): Generate a table describing the performance of each ensemble 

[Example 2](</mediawiki/index.php/Example_2> "Example 2"): Compare the performance of two ensembles 

[Example 3](</mediawiki/index.php/Example_3> "Example 3"): Generate ROC plots of one or more input ensembles. 

[Example 4](</mediawiki/index.php/Example_4> "Example 4"): Generate ROC data of one or more input ensembles
