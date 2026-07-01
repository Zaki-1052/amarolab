pbc set {box vectors from NPT simulation} -all

pbc wrap -center com -centersel "atomic selection near the center of the system" -compound residue -all

pbc wrap -center com -centersel "entire protein/membrane" -compound residue -all
