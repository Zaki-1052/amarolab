# Side Chain Modeling

## Introduction[edit](</mediawiki/index.php?title=Side_Chain_Modeling&action=edit&section=1> "Edit section: Introduction")]

The process of building appropriately located sidechain atoms missing from a protein model is known as sidechain modelling. This is an important step in HomologyModelling, protein design, and several other modelling tasks. There is a considerable range of approaches that may be used to undertake sidechain modelling, and these are reviewed in this document. 

## Being Discrete[edit](</mediawiki/index.php?title=Side_Chain_Modeling&action=edit&section=2> "Edit section: Being Discrete")]

Any single, specific, sidechain conformation is called a rotamer. While a continous range of conformations can be observed in solved protein structures, it is usual to treat sidechains as exhibiting only certian, discrete, conformations. The primary reason for this is to reduce the computational effort required in sampling available conformations. 

Typically, the rotamers available for a given residue type will be defined by a rotamer library. Many rotamer libraries exist. Many roatmer libraries are designed for general purpose modelling while others are specialised. Links to some of the more trustworthy rotamer libraries are provided below. 

It is important to note that some residues have quite different distributions of conformations (and therefore rotamers) depending upon the environment (i.e. buried versus exposed to solvent). The backbone conformation also correlates very strongly with the sidechain conformation. It is for this reason that many published rotamer libraries are sorted according to the backbone phi and psi dihedral angles or (less commonly) according to the secondary structure assignment. For example, phenylalanine may be observed in three distinct conformational clusters formed through 60 degree rotations about the C-alpha-C-beta bond. In helical segments, however, only two of these conformational clusters are ever seen. (This is due to occurance of a sidechain-backbone steric overlap.) 

## The Search[edit](</mediawiki/index.php?title=Side_Chain_Modeling&action=edit&section=3> "Edit section: The Search")]

Numerous algorithms exist for selecting appropriate rotamers for the construction of sidechain coordinates. These rely on a variety of schemes for evaluating the suitability of each conformation, including geometric, energetic and statistical measures. 

## Sidechain Placement Software Available to Us[edit](</mediawiki/index.php?title=Side_Chain_Modeling&action=edit&section=4> "Edit section: Sidechain Placement Software Available to Us")]

This list will be replaced by descriptions and instructions... 

SCAP sccomp SCRWL3.0 scgen 

## One or All[edit](</mediawiki/index.php?title=Side_Chain_Modeling&action=edit&section=5> "Edit section: One or All")]

It should be noted that if you are interested in modelling a few sidechains (e.g., after mutating a single residue or to build in a few missing atoms) then SCAP, sccomp, scgen and SCRWL will all produce very similar results. In such cases you should just choose whichever program you feel most comfortable with. It is only the cases in which a large number of sidechains need to be modelled (e.g., during homology modelling or while building an all-atom model from a backbone only model) that issue such as overall prediction accuracy and speed become important. 

## Some random writings:[edit](</mediawiki/index.php?title=Side_Chain_Modeling&action=edit&section=6> "Edit section: Some random writings:")]
    
    
    Hi,
    
    Dunbrack's backbone-dependent rotamer library is generally considered to be by far the best general purpose rotamer 
    library, and it can be freely downloaded from the Dunbrack website.  The associated software, SCRWL3, is the side-chain 
    placement software against which all else is compared.
    
    Stewart.
    
    
    
    I second that opinion.  I'm only using the backbone-independent library
    right now, but I could make a switch pretty easily.  I've got it all
    implemented in my code, and one of our summer students is looking at ways
    to make the code work with BD-like algorithms to look at association
    constants.
    
    The other thing I might add is that SCWRL3.0 doesn't always produce good
    results, even though it is the apex of side-chain predictors.  For
    instance, if you give it a complex of two proteins that has beend docked
    by a van-der-Waals potential (i.e. the structures are complete, and do not
    clash), and then ask SCWRL to recompute the side-chain configurations of
    the complex, about 3% of the time you get a bad steric clash between the 
    two proteins in the result, and I suspect that much more of the time you
    get bad intra-molecular interactions.  If you're going to talk seriously
    about any output from SCWRL, I'd run it through a short gas-phase
    minimization first.
    
    Dave
    
    
    
    A better rotamer library is the one used by SCAP:
    Xiang, Z. and Honig, B. (2001) Extending the Accuracy Limits of Prediction for Side Chain Conformations. J. Mol. Biol. 311:421-430.
    According to my own test, SCAP is far better than SCRWL in terms of accuracy.  SCAP achieved its accuracy by 
    using a large rotamer library.  (see http://www.proteinscience.org/cgi/content/full/13/3/735 ). In predicting structure 
    every sidechain conformation matters.  Accuracy sometimes outweigh the importance of speed.
    
    David
    
    
    
    David,
    
    With respect, that rotamer library was so large that the whole point of having a rotamer library was nullified.  I disagree 
    that SCAP is any better (or any worse) than SCRWL3, the improved results were an artifact of the huge rotamer library - 
    and (afaik) there is nothing stopping one from using a different rotamer library with either of those codes.
    There are definitely cases when the Xiang2001 approach is applicable, but Wei wants to make the sampling of sidechain 
    conformations tractable.  For the record, the software that I typically chose to use for sidechain placements is SCCOMP 
    (Eran Eyal et al. - see http://www.weizmann.ac.il/cgi-bin/sgedg/sccomp1.cgi ) with Dunbrack's BB-dependant library.
    Did you compare SCAP with SCWRL or SCRWL3?  Which version of the Dunbrack library?  2002, 2000, 1997, 1993?
    I guess this stuff should all go on the McWiki...
    
    Stewart
    
    
    
    Hi Wei, Andy, and Stewart,
    
    Even though I have nowhere near the experience that Stewart has on this 
    subject, I would have to agree.  I've been reading several papers on 
    this subject recently.  The Mayo group also uses the backbone-dependent 
    rotamer library from Dunbrack and Karplus for all of their protein 
    engineering projects =
    Dunbrack, R.L. and Karplus, M.  J. Mol. Bio.  230:  543-574 (1993).
    
    I hope this helps,
    Alex
    
    
    
    Thanks a lot, Andy and Stewart.
    
    Steward, I'd like to build side chains on a peptide template that binds to
    SH3 doamin. I heard that Richardson's rotamer library is also quite
    good. What do you think? Which one you think is better for my purpose?
    
    Thanks.
    Wei
    
    
    
    Hi Wei,
    
    In practise, I don't think there is much difference between the Richardson and Dunbrack libraries.  They both used structures 
    at 1.7 A resolution or better, both used criteria to eliminate suspect rotamers and both considered the backbone conformation.  
    I'd choose Dunbrack's over Richardson's solely on the basis that that was compiled ca. 2002 rather than ca. 2000, and I believe 
    that the Dunbrack training set was larger (although I may be wrong on that point).  If one is in a format that is easier for 
    you to use than the other, then that should probably be the ultimate deciding factor.
    I haven't checked rigorously, but I think that the Dunbrack library is cited more in current papers (this might be an artifact 
    of SCRWL3's existence).  One issue, that may or may not be critical, is that these rotamer libraries are based on X-ray 
    protein structures.  There is no reason to believe that the distribution of rotamers in such structures correspond to the 
    distribution of rotamers on a short peptide.  Presumably, you are just planning to use the rotamer library to limit the 
    conformations that you sample?  In that case, I don't think this will be a problem.
    
    Stewart
    
    
    
    HI, Stewart:
    
    Thanks a lot. I'll try Dunbrack's library first. 
    You are right that I just use rotamer library to limit the sample size.
    I'll start from a SH3-peptide complex, mutate amino acids of the
    peptide, minimize the complex and then quickly estimate the binding free
    energy using MM/PBSA or MM/GBSA for the single snapshot. I need to perform
    such simulation on 10e6 peptide sequences. Hopefully it won't be too slow.
    
    Thanks.
    Wei
    
    
    
    While I was doing the google for SCRWL, I found there are a lot different flavors out there:
    Ponder and Richards: http://www.fccc.edu/research/labs/dunbrack/sidechain/ponder_richards.rot
    Dunbrack and Cohen: http://www.fccc.edu/research/labs/dunbrack/sidechain.html
    Tuffery et al: http://condor.urbb.jussieu.fr/Rotamer.php/
    DeMaeyer et al: http://www.fccc.edu/research/labs/dunbrack/sidechain/demaeyer.rot
    Lovell et al: http://kinemage.biochem.duke.edu/databases/rotamer.php
    I used SCRWL versions from 2.1 to 2.9. Is there any huge improvement in SCRWL3?  I have to disagree with the point of having 
    the rotamer library.  The library was abtracted from the PDB. Larger library means we are using more information from the PDB.
    
    David
    
    
    
    Hi David,
    
    David Zhang wrote:
    > While I was doing the google for SCRWL, I found there are a lot different flavors out there:
    >
    > Ponder and Richards: http://www.fccc.edu/research/labs/dunbrack/sidechain/ponder_richards.rot
    > Dunbrack and Cohen: http://www.fccc.edu/research/labs/dunbrack/sidechain.html
    > Tuffery et al:     http://condor.urbb.jussieu.fr/Rotamer.php/
    > DeMaeyer et al: http://www.fccc.edu/research/labs/dunbrack/sidechain/demaeyer.rot
    > Lovell et al:     http://kinemage.biochem.duke.edu/databases/rotamer.php
    
    These are flavours of rotamer library not flavours of SCRWL.  Don't confuse the data set with the search algorithm!
    
    > I used SCRWL versions from 2.1 to 2.9. Is there any huge improvement in SCRWL3? 
    
    Yes.  Look at the paper of Canutescu (2003) Prot. Sci., iirc.
    
    > I have to disagree with the point of having the rotamer library.  The library was abtracted from the PDB. 
    Larger library means we are using more information from the PDB.
    As I've pointed out, the goal in this case was to limit the amount of conformational sampling to the minimal reasonable amount!
    NB/ Honig et al. used the same proteins as Dunbrack's 2002 edition of his library, so no additional information 
    is used from the PDB.  The Honig library may be considered more complete because it isn't compressed into a smaller 
    number of rotamers.  However, in this case it is desirable to have a smaller number of rotamers.  My rotamer library
    has >16 000 rotamers.  Does that make it better still?
    
    Stewart.
