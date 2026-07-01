import os
import sys



protein_residues = ["ALA", "ARG", "ASN", "ASP", "ASPP", "CYS", "GLN", "GLU", "GLY", "HSD", "HSE", "HSP", "ILE", "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL", "CYX", "HIE", "HID", "HIP", "CTER", "CT3", "ACE", "GLUP", "DISU", "LSN"]

def assign_radius(resname, atomname):
  ''' given the residue name and atom name, will return the appropriate radius for the atom '''
  radii = "X.XXX" # should be 'radius' but whatever
  if resname == "ASPP": resname = "ASP" # makes it easier
  if resname in protein_residues:
    if atomname == "C": radii = "2.040"
    elif atomname == "O": radii = "1.520"
    elif atomname == "OXT": radii = "1.520"
    elif atomname == "N": radii = "2.230"
    elif atomname == "CA":
      if resname == "GLY": radii = "2.380"
      else: radii = "2.860"
    elif atomname == "CB":
      if resname == "PRO": radii = "1.980"
      else: radii = "2.670"
    elif atomname == "CH2":
      if resname == "TRP": radii = "1.780"
    elif atomname == "OH":
      if resname == "TYR": radii = "1.850"
    elif atomname == "NE":
      if resname in ["ARG", "LYS", "LSN"]: radii = "2.130"
    elif atomname == "NZ":
      if resname in ["ARG", "LYS", "LSN"]: radii = "2.130"
    elif atomname == "NE2":
      if resname in ["GLN", "ASN"]: radii = "2.150"
      if resname in ["HSD", "HSE", "HSP", "HIE", "HID", "HIP"]: radii = "2.310"
    elif atomname == "ND2":
      if resname in ["GLN", "ASN"]: radii = "2.150"
    elif atomname == "ND1":
      if resname in ["HSD", "HSE", "HSP" , "HIE", "HID", "HIP"]: radii = "2.310"
    elif atomname == "NE1":
      if resname == "TRP": radii = "2.400"
    elif atomname[:1] == "S":
      if resname in ["MET", "CYS", "CYX"]: radii = "2.000"
    elif atomname in ["1SG", "2SG"]:
      if resname in ["DISU"]: radii = "2.000"
    elif atomname in ["1CB", "2CB"]:
      if resname in ["DISU"]: radii = "2.670"
    elif atomname[:2] == "OE":
      if resname in ["GLU", "GLUP", "ASP", "ASN", "GLN"]: radii = "1.420"
    elif atomname[:2] == "OD":
      if resname in ["GLU", "GLUP", "ASP", "ASN", "GLN"]: radii = "1.420"
    elif atomname[:2] == "OG":
      if resname in ["SER", "THR"]: radii = "1.640"
    elif atomname[:2] == "NH":
      if resname in ["ARG", "LYS", "LSN"]: radii = "2.130"
    elif atomname[:1] == "H": radii = "0.0000"
    elif atomname[:2] == "CG":
      if resname in ["VAL", "ILE", "ARG", "LYS", "LSN", "MET", "PHE", "THR", "TRP", "GLN", "GLU", "GLUP"]: radii = "2.460"
      elif resname in ["ASP", "GLU", "GLUP", "ASN", "GLN"]: radii = "1.980"
      elif resname == "PRO": radii = "1.980"
      elif resname in ["HSE", "HSD", "HSP", "HIE", "HID", "HIP"]: radii = "2.460" # THIS IS JUST A GUESS. NOT EXPLICITLY STATED IN PAPER. MOST CGS HAVE THIS.
      elif resname in ["LEU", "TYR"]: radii = "2.460" # THIS IS JUST A GUESS. NOT EXPLICITLY STATED IN PAPER. MOST CGS HAVE THIS.
    elif atomname[:2] == "CD":
      if resname in ["ILE", "LEU", "ARG", "LYS", "LSN"]: radii = "2.440"
      elif resname in ["ASP", "GLU", "GLUP", "ASN", "GLN"]: radii = "1.980"
      elif resname == "PRO": radii = "1.980"
      elif resname in ["TYR", "PHE"]: radii = "2.000"
      elif resname == "TRP": radii = "1.780"
      elif resname in ["HSE", "HSD", "HSP", "HIE", "HID", "HIP"]: radii = "2.000" # THIS IS JUST A GUESS. NOT EXPLICITLY STATED IN PAPER. ANALOGOUS TO TYR.
    elif atomname[:2] == "CE":
      if resname in ["TYR", "PHE"]: radii = "2.000"
      elif resname == "TRP": radii = "1.780"
      elif resname == "MET": radii = "2.100"
      elif resname in ["ARG", "LYS", "LSN"]: radii = "2.800"
      elif resname in ["HSE", "HSD", "HIE", "HID", "HIP"]: radii = "1.780" # THIS IS JUST A GUESS. NOT EXPLICITLY STATED IN PAPER. ANALOGOUS TO TRP.
      elif resname == "HSP": radii = "2.000"
    #elif atomname == "CE1":
      #if resname == "HSP": radii = "2.000"
    elif atomname[:2] == "CZ":
      if resname in ["TYR", "PHE"]: radii = "2.000"
      elif resname == "TRP": radii = "1.780"
      elif resname in ["ARG", "LYS", "LSN"]: radii = "2.800"
    elif atomname[:2] == "OT": radii = "1.420"  # THIS IS JUST A GUESS. NOT EXPLICITLY STATED IN PAPER. ANALOGOUS TO ASP.
    elif atomname == "CAT": radii = "2.06"  # CAY: 2.06. CY: 2.04. OY: 1.52. NT: 2.23
    elif atomname == "CAY": radii = "2.06"
    elif atomname[:2] == "CY": radii = "2.04"
    elif atomname[:2] == "OY": radii = "1.52"
    elif atomname[:2] == "NT": radii = "2.23"
    elif atomname in ["OT1", "OT2"]: radii = "1.420"
      
  else: # so it's a lipid (or something else)
    if atomname[:1] == "H": radii = "0.000"
    if atomname[:1].isdigit(): 
      if atomname [1] == "H": radii = "0.000"
    elif resname == "POPG":
      if atomname in ["C211", "C28", "C29", "C210", "C23", "C24", "C25", "C26", "C27", "C212", "C213", "C214", "C215", "C216", "C217", "C33", "C34", "C35", "C36", "C37", "C38", "C39", "C310", "C311", "C312", "C313", "C314", "C315"]: radii = "2.450" # SP3_c -- SP3_C -- SP3_c: Ex: CG/CD from LYS (2.46/2.44). Also, alkene carbons in chain, because couldn't find amino-acid analogue. Also carbon adjacent to alkene carbon.
      elif atomname in ["O11", "O12", "O13", "O14"]: radii = "1.420" # phosphate oxygens are like carbonyl oxygens (ASP OD1/OD2 and GLU OE1/OE2 (1.420))
      elif atomname == "P": radii = "1.980" # Phosphate themselves. Let's just consider like CG from ASP or CD from GLU. (1.98) THIS IS A BIG ASSUMPTION!!!
      elif atomname in ["O22", "O32"]: radii = "1.520" # Carbonyl oxygen atoms: O from backbone (1.52)
      elif atomname in ["C218", "C316"]: radii = "2.460" # Terminal sp3 C: ILE CG2/CG1 (2.46), LEU CD1/CD2 (2.44), THR CG2 (2.46), VAL CG1/CG2 (2.46)
      elif atomname in ["C22", "C32"]: radii = "2.460" # sp3 carbon adjacent to CO==O, with sp3 carbon on other side too. GLU CG (2.46)
      elif atomname in ["C11", "C1"]: radii = "2.670" # Carbon near phosphate oxygen. Like carbon adjacent to alcohol oxygen? Best I can do. SER CB (2.67), THR CB (2.67)
      #elif atomname in ["C12", "C15", "C14", "C13"]: radii = "2.800" # carbon next to nitrogen, carbon LYS CE (2.80)
      elif atomname in ["C21", "C31"]: radii = "2.040" # carbonyl carbon (ester). Let's use backbone C. (2.04)
      elif atomname in ["O21", "O31", "OC2", "OC3"]: radii = "1.420" # ester oxygen (not carbonyl). Let's use carboxylate oxygens. ASP OD1/OD2, GLU OE1/OE2 (1.42)
      elif atomname in ["C2", "C3", "C12", "C13"]: radii = "2.670" # carbon adjacent to ester oxygen. SER CB, THR CB. SER CB (2.67), THR CB (2.67)
    elif resname == "POPE":
      if atomname in ["C211", "C28", "C210", "C29", "C23", "C24", "C25", "C26", "C27", "C212", "C213", "C214", "C215", "C216", "C217", "C33", "C34", "C35", "C36", "C37", "C38", "C39", "C310", "C311", "C312", "C313", "C314", "C315"]: radii = "2.450" # SP3_c -- SP3_C -- SP3_c: Ex: CG/CD from LYS (2.46/2.44). Also alkene carbon. Also, carbon adjacent to alkene carbon.
      elif atomname == "N": radii = "2.130" # SP3_c -- SP3_N: Ex: NZ from LYS (2.13)
      elif atomname == "C12": radii = "2.800" # SP3_c -- SP3_C -- SP3_n: Ex: CE from LYS (2.80)
      elif atomname in ["O11", "O12", "O13", "O14"]: radii = "1.420" # phosphate oxygens are like carbonyl oxygens (ASP OD1/OD2 and GLU OE1/OE2 (1.420))
      elif atomname == "P": radii = "1.980" # Phosphate themselves. Let's just consider like CG from ASP or CD from GLU. (1.98) THIS IS A BIG ASSUMPTION!!!
      elif atomname in ["O22", "O32"]: radii = "1.520" # Carbonyl oxygen atoms: O from backbone (1.52)
      elif atomname in ["C218", "C316"]: radii = "2.460" # Terminal sp3 C: ILE CG2/CG1 (2.46), LEU CD1/CD2 (2.44), THR CG2 (2.46), VAL CG1/CG2 (2.46)
      elif atomname in ["C22", "C32"]: radii = "2.460" # sp3 carbon adjacent to CO==O, with sp3 carbon on other side too. GLU CG (2.46)
      elif atomname in ["C11", "C1"]: radii = "2.670" # Carbon near phosphate oxygen. Like carbon adjacent to alcohol oxygen? Best I can do. SER CB (2.67), THR CB (2.67)
      elif atomname == "C12": radii = "2.800" # carbon next to nitrogen, carbon LYS CE (2.80)
      elif atomname in ["C21", "C31"]: radii = "2.040" # carbonyl carbon (ester). Let's use backbone C. (2.04)
      elif atomname in ["C2", "C3"]: radii = "2.670" # carbon adjacent to ester oxygen. SER CB, THR CB. SER CB (2.67), THR CB (2.67)
      elif atomname in ["O21", "O31"]: radii = "1.420" # ester oxygen (not carbonyl). Let's use carboxylate oxygens. ASP OD1/OD2, GLU OE1/OE2 (1.42)
    elif resname == "POPC":
      if atomname == "N": radii = "2.130" # SP3_c -- SP3_N: Ex: NZ from LYS (2.13). Note, though, that this is quartinary N (attached to carbons)
      elif atomname in ["C211", "C28", "C29", "C210", "C23", "C24", "C25", "C26", "C27", "C212", "C213", "C214", "C215", "C216", "C217", "C33", "C34", "C35", "C36", "C37", "C38", "C39", "C310", "C311", "C312", "C313", "C314", "C315"]: radii = "2.450" # SP3_c -- SP3_C -- SP3_c: Ex: CG/CD from LYS (2.46/2.44). Also, alkene carbons in chain, because couldn't find amino-acid analogue. Also carbon adjacent to alkene carbon.
      elif atomname in ["O11", "O12", "O13", "O14"]: radii = "1.420" # phosphate oxygens are like carbonyl oxygens (ASP OD1/OD2 and GLU OE1/OE2 (1.420))
      elif atomname == "P": radii = "1.980" # Phosphate themselves. Let's just consider like CG from ASP or CD from GLU. (1.98) THIS IS A BIG ASSUMPTION!!!
      elif atomname in ["O22", "O32"]: radii = "1.520" # Carbonyl oxygen atoms: O from backbone (1.52)
      elif atomname in ["C218", "C316"]: radii = "2.460" # Terminal sp3 C: ILE CG2/CG1 (2.46), LEU CD1/CD2 (2.44), THR CG2 (2.46), VAL CG1/CG2 (2.46)
      elif atomname in ["C22", "C32"]: radii = "2.460" # sp3 carbon adjacent to CO==O, with sp3 carbon on other side too. GLU CG (2.46)
      elif atomname in ["C11", "C1"]: radii = "2.670" # Carbon near phosphate oxygen. Like carbon adjacent to alcohol oxygen? Best I can do. SER CB (2.67), THR CB (2.67)
      elif atomname in ["C12", "C15", "C14", "C13"]: radii = "2.800" # carbon next to nitrogen, carbon LYS CE (2.80)
      elif atomname in ["C21", "C31"]: radii = "2.040" # carbonyl carbon (ester). Let's use backbone C. (2.04)
      elif atomname in ["O21", "O31"]: radii = "1.420" # ester oxygen (not carbonyl). Let's use carboxylate oxygens. ASP OD1/OD2, GLU OE1/OE2 (1.42)
      elif atomname in ["C2", "C3"]: radii = "2.670" # carbon adjacent to ester oxygen. SER CB, THR CB. SER CB (2.67), THR CB (2.67)
    elif resname == "DSPS":
      if atomname in ["C23", "C24", "C25", "C26", "C27", "C28", "C29", "C210", "C211", "C212", "C213", "C214", "C215", "C216", "C217", "C33", "C34", "C35", "C36", "C37", "C38", "C39", "C310", "C311", "C312", "C313", "C314", "C315", "C316", "C317"]: radii = "2.450" # SP3_c -- SP3_C -- SP3_c: Ex: CG/CD from LYS (2.46/2.44)
      elif atomname == "N": radii = "2.130" # SP3_c -- SP3_N: Ex: NZ from LYS (2.13)
      elif atomname == "C12": radii = "2.800" # SP3_c -- SP3_C -- SP3_n: Ex: CE from LYS (2.80)
      elif atomname in ["O11", "O12", "O13", "O14"]: radii = "1.420" # phosphate oxygens are like carbonyl oxygens (ASP OD1/OD2 and GLU OE1/OE2 (1.420))
      elif atomname == "P": radii = "1.980" # Phosphate themselves. Let's just consider like CG from ASP or CD from GLU. (1.98) THIS IS A BIG ASSUMPTION!!!
      elif atomname in ["O22", "O32"]: radii = "1.520" # Carbonyl oxygen atoms: O from backbone (1.52)
      elif atomname in ["C218", "C318"]: radii = "2.460" # Terminal sp3 C: ILE CG2/CG1 (2.46), LEU CD1/CD2 (2.44), THR CG2 (2.46), VAL CG1/CG2 (2.46)
      elif atomname in ["C22", "C32"]: radii = "2.460" # sp3 carbon adjacent to CO==O, with sp3 carbon on other side too. GLU CG (2.46)
      elif atomname in ["C11", "C1"]: radii = "2.670" # Carbon near phosphate oxygen. Like carbon adjacent to alcohol oxygen? Best I can do. SER CB (2.67), THR CB (2.67)
      elif atomname == "C12": radii = "2.800" # carbon next to nitrogen, carbon LYS CE (2.80)
      elif atomname == "C13": radii = "1.980" # carboxylate carbon. ASP CG (1.98), GLU CD (1.98)
      elif atomname in ["O13A", "O13B"]: radii = "1.420" # carboxylate oxygen. ASP OD1/OD2, GLU OE1/OE2 (1.42)
      elif atomname in ["C21", "C31"]: radii = "2.040" # carbonyl carbon (ester). Let's use backbone C. (2.04)
      elif atomname in ["O21", "O31"]: radii = "1.420" # ester oxygen (not carbonyl). Let's use carboxylate oxygens. ASP OD1/OD2, GLU OE1/OE2 (1.42)
      elif atomname in ["C2", "C3"]: radii = "2.670" # carbon adjacent to ester oxygen. SER CB, THR CB. SER CB (2.67), THR CB (2.67)
    elif resname == "CHL1":
      # the CHL1 tail looks a lot like LEU. Let's use that as analogy
      if atomname in ["C27", "C26", "C21", "C22"]: radii = "2.440" # CD1/CD2 from LEU is analogous
      elif atomname in ["C25", "C20"]: radii = "2.670" # VAL CB (2.67) (mostly because couldn't find on LEU)
      elif atomname == "C24": radii = "2.670" # LEU CB (2.67)
      elif atomname[:1] == "C": radii = "2.450" # SP3_c -- SP3_C -- SP3_c: Ex: CG/CD from LYS (2.46/2.44). Also, alkene carbons in chain, because couldn't find amino-acid analogue. Also carbon adjacent to alkene carbon.
      elif atomname == "O3": radii = "1.640" # SER OG, THR OG1,
    elif resname == "CAL": radii = "1.370"
    
    elif resname == "SIA": # its a sialic acid
      if atomname == "C11": radii = "2.670" # like the beta carbon of an alanine
      if atomname == "C10": radii = "2.860" # like the alpha carbon of an alanine
      if atomname == "O10": radii = "1.520" # like the amide oxygen ?
      if atomname == "N5": radii = "2.130" # like the epsilon nitrogen of arginine
      if atomname == "C5": radii = "1.980" # like the delta carbon of a proline
      if atomname == "C4": radii = "2.670" # like a threonine beta carbon
      if atomname == "O4": radii = "1.64" # like a ser or thr beta oxygen
      if atomname == "C3": radii = "2.460" # like the gamma carbon of thr
      if atomname == "C2": radii = "1.980" # like the last carbon in asp or glu
      if atomname == "C1": radii = "1.980" # like the last carbon in asp or glu
      if atomname == "O1A": radii = "1.420" # like the oxygens in asp or glu
      if atomname == "O1B": radii = "1.420" # like the oxygens in asp or glu
      if atomname == "O2": radii = "1.640" # like a ser or thr beta oxygen
      if atomname == "O6": radii = "1.640" # even though this is ether: best I can do is a ser or thr beta oxygen
      if atomname == "C6": radii = "2.040" # sorta like a backbone carbon
      if atomname == "C7": radii = "2.460" # like the gamma carbon of thr
      if atomname == "O7": radii = "1.640" # like a ser or thr beta oxygen
      if atomname == "C8": radii = "2.460" # like the gamma carbon of thr
      if atomname == "O8": radii = "1.640" # like a ser or thr beta oxygen
      if atomname == "C9": radii = "2.460" # like the gamma carbon of thr
      if atomname == "O9": radii = "1.640" # like a ser or thr beta oxygen
      
    elif resname == "G39": # its a sialic acid
      if atomname == "C82": radii = "2.440" # like the delta carbon of an isoleucine
      if atomname == "C81": radii = "2.460" # like the gamma carbon of an isoleucine
      if atomname == "C8": radii = "2.670" # like the beta carbon of an isoleucine
      if atomname == "C9": radii = "2.460" # like the gamma carbon of an isoleucine
      if atomname == "C91": radii = "2.440" # like the gamma carbon of an isoleucine
      if atomname == "O7": radii = "1.64" # even though this is ether: best I can do is a ser or thr beta oxygen
      if atomname == "C6": radii = "2.04" # sorta like a backbone carbon
      if atomname == "C7": radii = "2.670" # like the beta carbon of an iso/leu
      if atomname == "C2": radii = "2.460" # like the 2nd to last carbon in asp or glu
      if atomname == "C1": radii = "1.980" # like the last carbon in asp or glu
      if atomname == "O1A": radii = "1.420" # like the oxygens in asp or glu
      if atomname == "O1B": radii = "1.420" # like the oxygens in asp or glu
      if atomname == "C3": radii = "2.670" # like the beta carbon of an iso/leu
      if atomname == "C4": radii = "2.800" # like the last carbon of lys
      if atomname == "N4": radii = "2.130" # like the last nitrogen of lys
      if atomname == "C5": radii = "2.440" # like the last delta carbon of arg
      if atomname == "N5": radii = "2.130" # like the epsilon nitrogen of arg
      if atomname == "C10": radii = "2.040" # sorta like a backbone carbon
      if atomname == "O10": radii = "1.520" # like the amide oxygen ?
      if atomname == "C11": radii = "2.670" # like the beta carbon of an alanine
      
  try:
    if radii != "0.0000":
      if radii == "1.370": # it's a CA
        R = "1.3700" # from CHARMM
      else: # not a calcium
        R = "%0.3f0" % (0.952 * (float(radii) + 0.3))
    else:
      R = "0.0000" # so hydrogens stay 0.000, per the relevant paper
  except:
    R = "X.XXXX"
  return radii

def parse_line(line, t):
  ''' parses a pdb line into various parts for assignment of the atom radius '''
  first_part = line[:t+1]
  radii = line[t+1:]
  
  line2 = line
  while "  " in line2: line2 = line2.replace("  "," ")
  line2 = line2.split(" ")
  atomname = line2[2]
  resname = line2[3]
  
  radii = assign_radius(resname, atomname)
  newline = first_part + radii
  return newline

if __name__ == "__main__":
  f = open(sys.argv[1], 'r')
  while True:
    line = f.readline().strip()
    if len(line) == 0: break
    if line[:4] == "ATOM":
      for t in range(len(line), -1, -1):
        if line[t:t+1] == " ": break
      print parse_line(line, t) # actually parse the line and print it with the new correct radius
  f.close()

'''
while True:
    line = f.readline().strip()
    if len(line) == 0: break
    if line[:4] == "ATOM":
        for t in range(len(line), -1, -1):
            if line[t:t+1] == " ": break
        #print line[:t+1] + line[t+1:]
        #print line
        #print ""
        #print line[t+1:]
        first_part = line[:t+1]
        radii = line[t+1:]
        
        line2 = line
        while "  " in line2: line2 = line2.replace("  "," ")
        line2 = line2.split(" ")
        atomname = line2[2]
        resname = line2[3]
        
        radii = "X.XXX"
        
        if resname in protein_residues:
            if atomname == "C": radii = "2.040"
            elif atomname == "O": radii = "1.520"
            elif atomname == "OXT": radii = "1.520"
            elif atomname == "N": radii = "2.230"
            elif atomname == "CA":
                if resname == "GLY": radii = "2.380"
                else: radii = "2.860"
            elif atomname == "CB":
                if resname == "PRO": radii = "1.980"
                else: radii = "2.670"
            elif atomname == "CH2":
                if resname == "TRP": radii = "1.780"
            elif atomname == "OH":
                if resname == "TYR": radii = "1.850"
            elif atomname == "NE":
                if resname in ["ARG", "LYS"]: radii = "2.130"
            elif atomname == "NZ":
                if resname in ["ARG", "LYS"]: radii = "2.130"
            elif atomname == "NE2":
                if resname in ["GLN", "ASN"]: radii = "2.150"
                if resname in ["HSD", "HSE", "HSP", "HIE", "HID", "HIP"]: radii = "2.310"
            elif atomname == "ND2":
                if resname in ["GLN", "ASN"]: radii = "2.150"
            elif atomname == "ND1":
                if resname in ["HSD", "HSE", "HSP" , "HIE", "HID", "HIP"]: radii = "2.310"
            elif atomname == "NE1":
                if resname == "TRP": radii = "2.400"
            elif atomname[:1] == "S":
                if resname in ["MET", "CYS", "CYX"]: radii = "2.000"
            elif atomname[:2] == "OE":
                if resname in ["GLU", "ASP", "ASN", "GLN"]: radii = "1.420"
            elif atomname[:2] == "OD":
                if resname in ["GLU", "ASP", "ASN", "GLN"]: radii = "1.420"
            elif atomname[:2] == "OG":
                if resname in ["SER", "THR"]: radii = "1.640"
            elif atomname[:2] == "NH":
                if resname in ["ARG", "LYS"]: radii = "2.130"
            elif atomname[:1] == "H": radii = "0.0000"
            elif atomname[:2] == "CG":
                if resname in ["VAL", "ILE", "ARG", "LYS", "MET", "PHE", "THR", "TRP", "GLN", "GLU"]: radii = "2.460"
                elif resname in ["ASP", "GLU", "ASN", "GLN"]: radii = "1.980"
                elif resname == "PRO": radii = "1.980"
                elif resname in ["HSE", "HSD", "HIE", "HID", "HIP"]: radii = "2.460" # THIS IS JUST A GUESS. NOT EXPLICITLY STATED IN PAPER. MOST CGS HAVE THIS.
                elif resname in ["LEU", "TYR"]: radii = "2.460" # THIS IS JUST A GUESS. NOT EXPLICITLY STATED IN PAPER. MOST CGS HAVE THIS.
            elif atomname[:2] == "CD":
                if resname in ["ILE", "LEU", "ARG", "LYS"]: radii = "2.440"
                elif resname in ["ASP", "GLU", "ASN", "GLN"]: radii = "1.980"
                elif resname == "PRO": radii = "1.980"
                elif resname in ["TYR", "PHE"]: radii = "2.000"
                elif resname == "TRP": radii = "1.780"
                elif resname in ["HSE", "HSD", "HIE", "HID", "HIP"]: radii = "2.000" # THIS IS JUST A GUESS. NOT EXPLICITLY STATED IN PAPER. ANALOGOUS TO TYR.
            elif atomname[:2] == "CE":
                if resname in ["TYR", "PHE"]: radii = "2.000"
                elif resname == "TRP": radii = "1.780"
                elif resname == "MET": radii = "2.100"
                elif resname in ["ARG", "LYS"]: radii = "2.800"
                elif resname in ["HSE", "HSD", "HIE", "HID", "HIP"]: radii = "1.780" # THIS IS JUST A GUESS. NOT EXPLICITLY STATED IN PAPER. ANALOGOUS TO TRP.
            elif atomname[:2] == "CZ":
                if resname in ["TYR", "PHE"]: radii = "2.000"
                elif resname == "TRP": radii = "1.780"
                elif resname in ["ARG", "LYS"]: radii = "2.800"
            elif atomname[:2] == "OT": radii = "1.420"  # THIS IS JUST A GUESS. NOT EXPLICITLY STATED IN PAPER. ANALOGOUS TO ASP.
        else: # so it's a lipid
            if atomname[:1] == "H": radii = "0.000"
            elif resname == "POPE":
                if atomname in ["C211", "C28", "C210", "C29", "C23", "C24", "C25", "C26", "C27", "C212", "C213", "C214", "C215", "C216", "C217", "C33", "C34", "C35", "C36", "C37", "C38", "C39", "C310", "C311", "C312", "C313", "C314", "C315"]: radii = "2.450" # SP3_c -- SP3_C -- SP3_c: Ex: CG/CD from LYS (2.46/2.44). Also alkene carbon. Also, carbon adjacent to alkene carbon.
                elif atomname == "N": radii = "2.130" # SP3_c -- SP3_N: Ex: NZ from LYS (2.13)
                elif atomname == "C12": radii = "2.800" # SP3_c -- SP3_C -- SP3_n: Ex: CE from LYS (2.80)
                elif atomname in ["O11", "O12", "O13", "O14"]: radii = "1.420" # phosphate oxygens are like carbonyl oxygens (ASP OD1/OD2 and GLU OE1/OE2 (1.420))
                elif atomname == "P": radii = "1.980" # Phosphate themselves. Let's just consider like CG from ASP or CD from GLU. (1.98) THIS IS A BIG ASSUMPTION!!!
                elif atomname in ["O22", "O32"]: radii = "1.520" # Carbonyl oxygen atoms: O from backbone (1.52)
                elif atomname in ["C218", "C316"]: radii = "2.460" # Terminal sp3 C: ILE CG2/CG1 (2.46), LEU CD1/CD2 (2.44), THR CG2 (2.46), VAL CG1/CG2 (2.46)
                elif atomname in ["C22", "C32"]: radii = "2.460" # sp3 carbon adjacent to CO==O, with sp3 carbon on other side too. GLU CG (2.46)
                elif atomname in ["C11", "C1"]: radii = "2.670" # Carbon near phosphate oxygen. Like carbon adjacent to alcohol oxygen? Best I can do. SER CB (2.67), THR CB (2.67)
                elif atomname == "C12": radii = "2.800" # carbon next to nitrogen, carbon LYS CE (2.80)
                elif atomname in ["C21", "C31"]: radii = "2.040" # carbonyl carbon (ester). Let's use backbone C. (2.04)
                elif atomname in ["C2", "C3"]: radii = "2.670" # carbon adjacent to ester oxygen. SER CB, THR CB. SER CB (2.67), THR CB (2.67)
                elif atomname in ["O21", "O31"]: radii = "1.420" # ester oxygen (not carbonyl). Let's use carboxylate oxygens. ASP OD1/OD2, GLU OE1/OE2 (1.42)
            elif resname == "POPC":
                if atomname == "N": radii = "2.130" # SP3_c -- SP3_N: Ex: NZ from LYS (2.13). Note, though, that this is quartinary N (attached to carbons)
                elif atomname in ["C211", "C28", "C29", "C210", "C23", "C24", "C25", "C26", "C27", "C212", "C213", "C214", "C215", "C216", "C217", "C33", "C34", "C35", "C36", "C37", "C38", "C39", "C310", "C311", "C312", "C313", "C314", "C315"]: radii = "2.450" # SP3_c -- SP3_C -- SP3_c: Ex: CG/CD from LYS (2.46/2.44). Also, alkene carbons in chain, because couldn't find amino-acid analogue. Also carbon adjacent to alkene carbon.
                elif atomname in ["O11", "O12", "O13", "O14"]: radii = "1.420" # phosphate oxygens are like carbonyl oxygens (ASP OD1/OD2 and GLU OE1/OE2 (1.420))
                elif atomname == "P": radii = "1.980" # Phosphate themselves. Let's just consider like CG from ASP or CD from GLU. (1.98) THIS IS A BIG ASSUMPTION!!!
                elif atomname in ["O22", "O32"]: radii = "1.520" # Carbonyl oxygen atoms: O from backbone (1.52)
                elif atomname in ["C218", "C316"]: radii = "2.460" # Terminal sp3 C: ILE CG2/CG1 (2.46), LEU CD1/CD2 (2.44), THR CG2 (2.46), VAL CG1/CG2 (2.46)
                elif atomname in ["C22", "C32"]: radii = "2.460" # sp3 carbon adjacent to CO==O, with sp3 carbon on other side too. GLU CG (2.46)
                elif atomname in ["C11", "C1"]: radii = "2.670" # Carbon near phosphate oxygen. Like carbon adjacent to alcohol oxygen? Best I can do. SER CB (2.67), THR CB (2.67)
                elif atomname in ["C12", "C15", "C14", "C13"]: radii = "2.800" # carbon next to nitrogen, carbon LYS CE (2.80)
                elif atomname in ["C21", "C31"]: radii = "2.040" # carbonyl carbon (ester). Let's use backbone C. (2.04)
                elif atomname in ["O21", "O31"]: radii = "1.420" # ester oxygen (not carbonyl). Let's use carboxylate oxygens. ASP OD1/OD2, GLU OE1/OE2 (1.42)
                elif atomname in ["C2", "C3"]: radii = "2.670" # carbon adjacent to ester oxygen. SER CB, THR CB. SER CB (2.67), THR CB (2.67)
            elif resname == "DSPS":
                if atomname in ["C23", "C24", "C25", "C26", "C27", "C28", "C29", "C210", "C211", "C212", "C213", "C214", "C215", "C216", "C217", "C33", "C34", "C35", "C36", "C37", "C38", "C39", "C310", "C311", "C312", "C313", "C314", "C315", "C316", "C317"]: radii = "2.450" # SP3_c -- SP3_C -- SP3_c: Ex: CG/CD from LYS (2.46/2.44)
                elif atomname == "N": radii = "2.130" # SP3_c -- SP3_N: Ex: NZ from LYS (2.13)
                elif atomname == "C12": radii = "2.800" # SP3_c -- SP3_C -- SP3_n: Ex: CE from LYS (2.80)
                elif atomname in ["O11", "O12", "O13", "O14"]: radii = "1.420" # phosphate oxygens are like carbonyl oxygens (ASP OD1/OD2 and GLU OE1/OE2 (1.420))
                elif atomname == "P": radii = "1.980" # Phosphate themselves. Let's just consider like CG from ASP or CD from GLU. (1.98) THIS IS A BIG ASSUMPTION!!!
                elif atomname in ["O22", "O32"]: radii = "1.520" # Carbonyl oxygen atoms: O from backbone (1.52)
                elif atomname in ["C218", "C318"]: radii = "2.460" # Terminal sp3 C: ILE CG2/CG1 (2.46), LEU CD1/CD2 (2.44), THR CG2 (2.46), VAL CG1/CG2 (2.46)
                elif atomname in ["C22", "C32"]: radii = "2.460" # sp3 carbon adjacent to CO==O, with sp3 carbon on other side too. GLU CG (2.46)
                elif atomname in ["C11", "C1"]: radii = "2.670" # Carbon near phosphate oxygen. Like carbon adjacent to alcohol oxygen? Best I can do. SER CB (2.67), THR CB (2.67)
                elif atomname == "C12": radii = "2.800" # carbon next to nitrogen, carbon LYS CE (2.80)
                elif atomname == "C13": radii = "1.980" # carboxylate carbon. ASP CG (1.98), GLU CD (1.98)
                elif atomname in ["O13A", "O13B"]: radii = "1.420" # carboxylate oxygen. ASP OD1/OD2, GLU OE1/OE2 (1.42)
                elif atomname in ["C21", "C31"]: radii = "2.040" # carbonyl carbon (ester). Let's use backbone C. (2.04)
                elif atomname in ["O21", "O31"]: radii = "1.420" # ester oxygen (not carbonyl). Let's use carboxylate oxygens. ASP OD1/OD2, GLU OE1/OE2 (1.42)
                elif atomname in ["C2", "C3"]: radii = "2.670" # carbon adjacent to ester oxygen. SER CB, THR CB. SER CB (2.67), THR CB (2.67)
            elif resname == "CHL1":
                # the CHL1 tail looks a lot like LEU. Let's use that as analogy
                if atomname in ["C27", "C26", "C21", "C22"]: radii = "2.440" # CD1/CD2 from LEU is analogous
                elif atomname in ["C25", "C20"]: radii = "2.670" # VAL CB (2.67) (mostly because couldn't find on LEU)
                elif atomname == "C24": radii = "2.670" # LEU CB (2.67)
                elif atomname[:1] == "C": radii = "2.450" # SP3_c -- SP3_C -- SP3_c: Ex: CG/CD from LYS (2.46/2.44). Also, alkene carbons in chain, because couldn't find amino-acid analogue. Also carbon adjacent to alkene carbon.
                elif atomname == "O3": radii = "1.640" # SER OG, THR OG1,
            elif resname == "CAL": radii = "1.370"

        try:
            if radii != "0.0000":
                if radii == "1.370": # it's a CA
                    R = "1.3700" # from CHARMM
                else: # not a calcium
                    R = "%0.3f0" % (0.952 * (float(radii) + 0.3))
            else:
                R = "0.0000" # so hydrogens stay 0.000, per the relevant paper
        except:
            R = "X.XXXX"
        
        print first_part + R
 CHL1 residue

C1
C10
C11
C12
C13
C14
C15
C16
C17
C18
C19
C2
C20
C21
C22
C23
C24
C25
C26
C27
C3
C4
C5
C6
C7
C8
C9
O3




# these ones not defined:

CD2	HSD: CD1 and CD2 from PHE TYR good analogue (2.000)
CD2	HSE
CE1	HSD: CE1 and CE2 from PHE TYR good analogue (2.000)
CE1	HSE
CG	HSD: CG from PHE good analogue (2.460)
CG	HSE

CG	LEU: CG from ARG GLN (2.460)
CG	TYR: CG from PHE good analogue (2.460)

OT1	GLY: ASP OD1/OD2 and GLU OE1/OE2 (1.420)
OT1	ILE: ASP OD1/OD2 and GLU OE1/OE2 (1.420)
OT1	LYS: ASP OD1/OD2 and GLU OE1/OE2 (1.420)
OT2	GLY: ASP OD1/OD2 and GLU OE1/OE2 (1.420)
OT2	ILE: ASP OD1/OD2 and GLU OE1/OE2 (1.420)
OT2	LYS: ASP OD1/OD2 and GLU OE1/OE2 (1.420)


# Patches N-term and C-term CAT, CAY: 2.06. CY: 2.04. OY: 1.52. NT: 2.23

f.close()
'''
