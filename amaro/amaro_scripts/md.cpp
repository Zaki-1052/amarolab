/*
Lane's MD engine

This MD engine uses a given symplectic method to integrate Newton's equations of motion for a molecular system
Potential Energy and Forces built according to the Amber potential

Thermostats implemented:
- Andersen
- Gaussian
- Berendsen
- Langevin


*/

#include <iomanip>
#include <cmath>
#include <cassert>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
//#include <istream>
//#include <ostream>
#include <cstring>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <cstdio>
#include <climits>
#include <cstdlib>


const int MAX_ATOMS = 1000; // the maximum number of atoms to allocate for
const int MAX_BONDS = 1000;
const int MAX_ANGLES = 1000;
const int MAX_DIHEDRALS = 1000;
const int MAX_ATOM_TYPES = 10;
const int MAX_BOND_TYPES = 20;
const int MAX_ANGLE_TYPES = 40;
const int MAX_DIHEDRAL_TYPES = 80;
const double k = 8.3144621454689521e-07; // Boltzmann's const in A^2 * amu / fs^2 * K
const double PI = atan(1)*4;
const double AVO = 6.022e23; // Avogadro's number
const double FARADAY_CONST = 1.6021766e-19; // Faraday constant in C
const double PERMITTIVITY = 0.572779161; // permittivity of a vacuum in e^2 * fs^2 / amu * A^3

// Parameters for simulation
const double dt = 1.0; // size of timestep in fs
const double NUMSTEPS = 1000; // max number of steps in simulation
const int TRAJ_FREQ = 1; // trajectory update frequency
const int ENERGY_FREQ = 1; // print energy information frequency
const double BOXDIMS[6] = { -800.0, -800.0, -800.0, 780.1 , 780.1, 780.1 }; //{ 0.0, 0.0, 0.0, 34.7786, 34.7786, 34.7786 };
const double BOXAREA = 2.0 * ((BOXDIMS[3]-BOXDIMS[0])*(BOXDIMS[4]-BOXDIMS[1]) + (BOXDIMS[3]-BOXDIMS[0])*(BOXDIMS[5]-BOXDIMS[2]) + (BOXDIMS[5]-BOXDIMS[2])*(BOXDIMS[4]-BOXDIMS[1])); // total box surface area
const double BOXVOLUME = (BOXDIMS[3]-BOXDIMS[0]) * (BOXDIMS[4]-BOXDIMS[1]) * (BOXDIMS[5]-BOXDIMS[2]); // total box volume
const bool VEL_TRAJ = true; // whether the velocity trajectory is calculated



const bool VDW_FORCES = true; // whether VDW forces are evaluated
const bool COULOMB_FORCES = true; // whether Coulombic interactions are counted
const bool BOND_FORCES = true; // whether bonded interactions are counted
const bool ANGLE_FORCES = false; // whether angular interactions are counted
const bool DIHEDRAL_FORCES = false; // whether dihedral interactions are counted

const bool ANDERSEN_THERMOSTAT = false; // whether the Andersen thermostat is activated
const double ANDERSEN_NU = 0.01; // factor that determines the frequency of random kicks
const bool ANDERSEN_BORDER = false; // random velocities initiated from
const bool GAUSSIAN_THERMOSTAT = false;
const bool BERENDSEN_THERMOSTAT = false;
const double BERENDSEN_TAU = 0.01; // relaxation factor; fraction of timestep to decay
const bool LANGEVIN_THERMOSTAT = false;
const double LANGEVIN_DAMPING = 0.1; // the damping coefficient for Langevin Thermostat

const char ATOM_TYPE_FILENAME[] = "atom.ff"; // the filename that contains the atom ff params
const char BOND_TYPE_FILENAME[] = "bond.ff"; // the filename that contains the bond ff params
const char ANGLE_TYPE_FILENAME[] = "angle.ff"; // the filename that contains the angle ff params
const char DIHEDRAL_TYPE_FILENAME[] = "dihedral.ff"; // the filename that contains the angle ff params

using namespace std;

// Atom
struct Atom {
  int index; // index of the atom
  int serial; // serial of the atom
  string name; // name of the atom for forcefield purposes
  string resname;
  string ffname;
  double charge;
  double vdw_radius; // for VDW
  double vdw_epsilon; 
  double mass;
  double rx0; double ry0; double rz0;  // current atomic position
  double vx0; double vy0; double vz0;  // current atomic velocities
  double ax0; double ay0; double az0;  // current atomic acceleration
  
  double rx1; double ry1; double rz1;  // next atomic position
  double vx1; double vy1; double vz1;  // next atomic velocities
  double ax1; double ay1; double az1;  // next atomic acceleration
  
  Atom *next; // the next atom in the list
  //struct Atom *bondlist
};

struct Atom_type { // a holder for information pertaining to each atom type
  string atom1_name;
  double mass;
  double charge;
  double vdw_radius; // for VDW
  double vdw_epsilon; 
};

struct Bond { // a bond data structure
  Atom *atom1; // the atoms that are connected by the bond
  Atom *atom2;
  double k; // bond spring constant
  double eq; // bond equilibrium distance
};

struct Bond_type { // contains all possible types of bonds
  string atom1_name;
  string atom2_name;
  double k; // bond spring constant
  double eq; // bond equilibrium distance
};

struct Angle { // an angle data structure
  Atom *atom1; // the atoms that are connected by the bond angle
  Atom *atom2;
  Atom *atom3;
  double k; // angle spring constant
  double eq; // angle equilibrium distance
};

struct Angle_type { // contains all possible types of Angles
  string atom1_name;
  string atom2_name;
  string atom3_name;
  double k; // angle spring constant
  double eq; // equilibrium angle
};

struct Dihedral { // an dihedral data structure
  Atom *atom1; // the atoms that are connected by the dihedral
  Atom *atom2;
  Atom *atom3;
  Atom *atom4;
  double Vn; // 
  double n; // number of peaks
  double gamma; // torsion offset
};

struct Dihedral_type { // contains all possible types of dihedrals
  string atom1_name;
  string atom2_name;
  string atom3_name;
  string atom4_name;
  double Vn; // 
  double n; // number of peaks
  double gamma; // torsion offset
};

//static Atom nil = {0, "", "", 0.0, 0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,0.0, 0};
//Atom *NIL = &nil;

bool string2int(const string& str, int& result) {
  // Converts a string into an integer by ref
  istringstream ss(str);
  ss.imbue(locale::classic());
  ss >> result;
  return !ss.fail() && ss.eof();
}

double energy_convert(double kJ_mol) { // given a number in kJ/mol, will convert to A^2 * amu / fs^2
  // (1e20A^2/m^2) * (Avo's * 1e3 kg/amu) * 1e3 J/kJ / Avo's * (1e30fs^2/s^2)
  return kJ_mol * ( 1.0e20 * 1.0e6 / 1.0e30);
}

double assign_mass(Atom *atom) {
  // assign the mass based 
  string name, one_char, two_char;
  name = atom[0].name; // get the atom's name to get element
  name.erase( remove(name.begin(), name.end(), ' '), name.end()); // strip the spaces
  one_char = name.substr(0,1); two_char = name.substr(0,2);
  //cout << "one_char: " << one_char << " two_char: " << two_char << endl;
  if (two_char.compare("Ar") == 0) atom[0].mass = 39.948; // assign the molecular weight of argon
}

int read_pdb(ifstream &pdb_file, Atom *atom_list, int n_atom_types, Atom_type *atom_type_list) {
  /* parses a pdb file for atom positions, names, etc.
  returns a number of atoms, and creates an atom list by ref */
  string line, str, atom_name, type_name;
  string record, name, resname, chain; // PDB variables
  int index, serial, resid;
  double x, y, z, occ, beta; 
  int n=0; // number of lines in the file
  int i;
  Atom *cur_atom = &atom_list[0]; // the first atom
  Atom *prev_atom; // the previous atom in the list
  if (pdb_file.is_open()) {
    while (!pdb_file.eof()) { // read each line of the file
      getline(pdb_file,line); // takes a line from the file
      record = line.substr(0,6); 
      
      if (record.compare("ATOM  ") == 0) { // then we can continue
        
        string2int(line.substr(6,5),serial); name = line.substr(12,4); resname = line.substr(17,3);
        chain = line.substr(21,1); string2int(line.substr(22,4),resid); 
        x = atof(line.substr(30,8).c_str()); y = atof(line.substr(38,8).c_str()); z = atof(line.substr(46,8).c_str());
        //occ = atof(line.substr(54,6).c_str()); beta = atof(line.substr(60,6).c_str());
        cur_atom->serial = serial; cur_atom->name = name; cur_atom->resname = resname;
        cur_atom->index = n;
        cur_atom->rx0 = x; cur_atom->ry0 = y; cur_atom->rz0 = z; 
        assign_mass(cur_atom); // assign the mass of each atom
        for(i=0;i<n_atom_types;i++) {
          atom_name = cur_atom->name.substr(1,3);
          type_name = atom_type_list[i].atom1_name;
          if (atom_name.compare(type_name) == 0) {
            //cout << "found atom type for atom: " << atom_type_list[i].atom1_name << endl;
            cur_atom->mass = atom_type_list[i].mass;
            cur_atom->charge = atom_type_list[i].charge;
            cur_atom->vdw_radius = atom_type_list[i].vdw_radius;
            cur_atom->vdw_epsilon = energy_convert(atom_type_list[i].vdw_epsilon);
            break;
          }
        }
        //cur_atom->charge = double((n % 2)*2-1)*50.0; //0.0;
        //cout << name << " " << index << " " << resid << " " << x << "," <<  y << "," <<  z << ", charge: " << cur_atom->charge << endl;
        
        
        
        if (n > 0) prev_atom->next = cur_atom;
        prev_atom = cur_atom;
        n++;
        cur_atom = &atom_list[n]; // move to the next atom in the list
        
      } else {
        cout << "not including line: " << line << endl;
      }
      //atom_list[n]->next = nil;
      
      //cout << line; // put to standard output
    
    }
  } else {
    cout << "ERROR: could not open pdb file\n";
  }
  pdb_file.close();
  //cout << "\nNumber of lines in file: " << n << endl;
  return n;
}

int read_psf(ifstream &psf_file, int n, Atom *atom_list, Bond *bond_list, int *n_bonds, Bond_type *bond_type_list, int n_bond_types, Angle *angle_list, int *n_angles, Angle_type *angle_type_list, int n_angle_types, Dihedral *dihedral_list, int *n_dihedrals, Dihedral_type *dihedral_type_list, int n_dihedral_types) {
  /* Reads and parses a PSF in order to obtain Atom, bond, angle, and dihedral information. Constructs the lists of such bonded interactions */
  string line, title, ffname;
  double charge, mass;
  int i, j, k, mode=0; // 0=title, 1=atom, 2=bond, 3=atom, 4=dihedral, 5=end
  Atom atom1, atom2, atom3, atom4;
  int pt[4]; // declare 9 data points to store numbers in the psf file
  if (psf_file.is_open()) {
    while (!psf_file.eof()) { // read each line of the file
      getline(psf_file,line); // takes a line from the file
      if (line.length() < 15) continue;
      title = line.substr(9,6); 
      if (title.compare("!NATOM") == 0) {
        mode = 1; // atom read mode
        i = 0;
      } else if (title.compare("!NBOND") == 0) {
        mode = 2; // bond read mode
        i = 0;
      } else if (title.compare("!NTHET") == 0) {
        mode = 3; // angle read mode
        i = 0;
      } else if (title.compare("!NPHI:") == 0) {
        mode = 4; // dihedral read mode
        i = 0;
      } else {
        if (mode == 1) {
          //cout << "ATOM LINE: " << line << endl;
          ffname = line.substr(29,2);
          charge = atof(line.substr(35,9).c_str());  
          mass = atof(line.substr(51,7).c_str()); 
          atom_list[i].mass = mass; atom_list[i].charge = charge; atom_list[i].ffname = ffname; 
          i++; 
        } else if (mode == 2) {
          //cout << "BOND LINE: " << line << endl;
          for (j=0;j<4;j++) {
            if (line.length() <= 16*j+8) break;
            string2int(line.substr(16*j,8),pt[0]); string2int(line.substr(16*j + 8,8),pt[1]);
            bond_list[*n_bonds].atom1 = &atom_list[pt[0]-1]; // assign the two atoms for the bond
            bond_list[*n_bonds].atom2 = &atom_list[pt[1]-1];
            //cout << "atom ffnames:" << bond_list[*n_bonds].atom1->ffname << "," << bond_list[*n_bonds].atom2->ffname << endl;
            for (k=0;k<n_bond_types;k++) { // search thru all bond types to assign the force constants
              if (bond_type_list[k].atom1_name == bond_list[*n_bonds].atom1->ffname && bond_type_list[k].atom2_name == bond_list[*n_bonds].atom2->ffname ) { // if we found the ff entry
                bond_list[*n_bonds].k = bond_type_list[k].k; // then assign the relevant values:
                bond_list[*n_bonds].eq = bond_type_list[k].eq;
                break;
              }
            }
            *n_bonds = *n_bonds + 1;
          } 
        } else if (mode == 3) {
          //cout << "ANGLE LINE: " << line << endl;
          for (j=0;j<3;j++) {
            if (line.length() <= 24*j+8) break;
            string2int(line.substr(24*j,8),pt[0]); string2int(line.substr(24*j + 8,8),pt[1]); string2int(line.substr(24*j + 16,8),pt[2]);
            angle_list[*n_angles].atom1 = &atom_list[pt[0]-1]; // assign the atoms
            angle_list[*n_angles].atom2 = &atom_list[pt[1]-1];
            angle_list[*n_angles].atom3 = &atom_list[pt[2]-1];
            //cout << "atom ffnames:" << angle_list[*n_angles].atom1->ffname << "," << angle_list[*n_angles].atom2->ffname << "," << angle_list[*n_angles].atom3->ffname << endl;
            for (k=0;k<n_angle_types;k++) { // search thru all angle types to assign the force constants
              if (angle_type_list[k].atom1_name == angle_list[*n_angles].atom1->ffname && angle_type_list[k].atom2_name == angle_list[*n_angles].atom2->ffname && angle_type_list[k].atom3_name == angle_list[*n_angles].atom3->ffname) { // if we found the ff entry
                angle_list[*n_angles].k = angle_type_list[k].k; // then assign the relevant values:
                angle_list[*n_angles].eq = angle_type_list[k].eq;
                break;
              }
            }
            *n_angles = *n_angles + 1;
          } 
            
        } else if (mode == 4) {
          //cout << "DIHED LINE: " << line << endl;
          for (j=0;j<2;j++) {
            if (line.length() <= 32*j+8) break;
            string2int(line.substr(32*j,8),pt[0]); string2int(line.substr(32*j + 8,8),pt[1]); string2int(line.substr(32*j + 16,8),pt[2]); string2int(line.substr(32*j + 24,8),pt[3]);
            dihedral_list[*n_dihedrals].atom1 = &atom_list[pt[0]-1]; // assign the atoms
            dihedral_list[*n_dihedrals].atom2 = &atom_list[pt[1]-1];
            dihedral_list[*n_dihedrals].atom3 = &atom_list[pt[2]-1];
            dihedral_list[*n_dihedrals].atom4 = &atom_list[pt[3]-1];
            //cout << "atom ffnames:" << dihedral_list[*n_dihedrals].atom1->ffname << "," << dihedral_list[*n_dihedrals].atom2->ffname << "," << dihedral_list[*n_dihedrals].atom3->ffname << "," << dihedral_list[*n_dihedrals].atom4->ffname << endl;
            for (k=0;k<n_dihedral_types;k++) { // search thru all dihedral types to assign the force constants
              if (dihedral_type_list[k].atom1_name == dihedral_list[*n_dihedrals].atom1->ffname && dihedral_type_list[k].atom2_name == dihedral_list[*n_dihedrals].atom2->ffname && dihedral_type_list[k].atom3_name == dihedral_list[*n_dihedrals].atom3->ffname && dihedral_type_list[k].atom4_name == dihedral_list[*n_dihedrals].atom4->ffname) { // if we found the ff entry
                dihedral_list[*n_dihedrals].Vn = dihedral_type_list[k].Vn; // then assign the relevant values:
                dihedral_list[*n_dihedrals].n = dihedral_type_list[k].n;
                dihedral_list[*n_dihedrals].gamma = dihedral_type_list[k].gamma;
                break;
              }
            }
            *n_dihedrals = *n_dihedrals + 1;
          }
        }
      }
      
      
    }
  }
  //cout << "nbonds: " << *n_bonds << endl;
  /*for (i=0;i<*n_bonds;i++) {
    cout << "bond atom1: " << bond_list[i].atom1->ffname << " bond atom2: " << bond_list[i].atom2->ffname <<" bond k: " << bond_list[i].k << " bond eq: " << bond_list[i].eq << endl;
  }
  cout << "nangles: " << *n_angles << endl;
  for (i=0;i<*n_angles;i++) {
    cout << "angle atom1: " << angle_list[i].atom1->ffname << " angle atom2: " << angle_list[i].atom2->ffname << " angle atom3: " << angle_list[i].atom3->ffname <<" bond k: " << angle_list[i].k << " bond eq: " << angle_list[i].eq << endl;
  }*/
  psf_file.close(); 
  return 0;
}

int read_ff_atom(ifstream &ff_atom, Atom_type *atom_type_list) {
  /* parses a ff file for atom terms. */
  string line, str, firstchar;
  int n_atom_types=0; // number of atomtypes
  Atom_type *cur_atom_type = &atom_type_list[0];
  if (ff_atom.is_open()) {
    while (!ff_atom.eof()) { // read each line of the file
      getline(ff_atom,line); // takes a line from the file
      if(ff_atom.eof()) break;
      firstchar = line.substr(0,1); 
      if (firstchar.compare("#") != 0) { // then this is not a comment
        cur_atom_type->atom1_name = line.substr(0,3);
        cur_atom_type->mass = atof(line.substr(3,5).c_str());
        cur_atom_type->charge = atof(line.substr(10,5).c_str());
        cur_atom_type->vdw_radius = atof(line.substr(17,6).c_str());
        cur_atom_type->vdw_epsilon = atof(line.substr(25,6).c_str());
        n_atom_types++;
        //cout << "name: " << cur_atom_type->atom1_name << " vdw_epsilon:" << cur_atom_type->vdw_epsilon << endl;
        cur_atom_type = &atom_type_list[n_atom_types];
      } else { // then don't include this line, it is a comment
        cout << "Skipping line: " << line << endl;
      }
    }
  }
  ff_atom.close();
  return n_atom_types;
}

int read_ff_bond(ifstream &ff_bond, Bond_type *bond_type_list) {
  /* parses a ff file for bond terms */
  string line, str, firstchar;
  int n_bond_types=0; // number of bond types
  Bond_type *cur_bond_type = &bond_type_list[0];
  if (ff_bond.is_open()) {
    while (!ff_bond.eof()) { // read each line of the file
      getline(ff_bond,line); // takes a line from the file
      if(ff_bond.eof()) break;
      firstchar = line.substr(0,1); 
      if (firstchar.compare("#") != 0) { // then this is not a comment
        cur_bond_type->atom1_name = line.substr(0,2);
        cur_bond_type->atom2_name = line.substr(3,2);
        cur_bond_type->k = atof(line.substr(7,5).c_str());
        cur_bond_type->eq = atof(line.substr(16,6).c_str());
        
        n_bond_types++;
        cout << "name1: " << cur_bond_type->atom1_name << " name2: " << cur_bond_type->atom2_name << " k:" << cur_bond_type->k << " eq:" << cur_bond_type->eq << endl;
        cur_bond_type = &bond_type_list[n_bond_types];
      } else { // then don't include this line, it is a comment
        cout << "Skipping line: " << line << endl;
      }
    }
  }
  ff_bond.close();
  return n_bond_types;
}

int read_ff_angle(ifstream &ff_angle, Angle_type *angle_type_list) {
  /* parses a ff file for angle terms */
  string line, str, firstchar;
  int n_angle_types=0; // number of angle types
  Angle_type *cur_angle_type = &angle_type_list[0];
  if (ff_angle.is_open()) {
    while (!ff_angle.eof()) { // read each line of the file
      getline(ff_angle,line); // takes a line from the file
      if(ff_angle.eof()) break;
      firstchar = line.substr(0,1); 
      if (firstchar.compare("#") != 0) { // then this is not a comment
        cur_angle_type->atom1_name = line.substr(0,2);
        cur_angle_type->atom2_name = line.substr(3,2);
        cur_angle_type->atom3_name = line.substr(6,2);
        cur_angle_type->k = atof(line.substr(11,6).c_str());
        cur_angle_type->eq = atof(line.substr(22,6).c_str()) * PI/180; // need to convert from degrees to radians
        
        n_angle_types++;
        cout << "name1: " << cur_angle_type->atom1_name << " name2: " << cur_angle_type->atom2_name << " name3: " << cur_angle_type->atom3_name << " k:" << cur_angle_type->k << " eq:" << cur_angle_type->eq << endl;
        cur_angle_type = &angle_type_list[n_angle_types];
      } else { // then don't include this line, it is a comment
        cout << "Skipping line: " << line << endl;
      }
    }
  }
  ff_angle.close();
  return n_angle_types;
}

int read_ff_dihedral(ifstream &ff_dihedral, Dihedral_type *dihedral_type_list) {
  /* parses a ff file for dihedral terms */
  string line, str, firstchar;
  int n_dihedral_types=0; // number of dihedral types
  Dihedral_type *cur_dihedral_type = &dihedral_type_list[0];
  if (ff_dihedral.is_open()) {
    while (!ff_dihedral.eof()) { // read each line of the file
      getline(ff_dihedral,line); // takes a line from the file
      if(ff_dihedral.eof()) break;
      firstchar = line.substr(0,1); 
      if (firstchar.compare("#") != 0) { // then this is not a comment
        cur_dihedral_type->atom1_name = line.substr(0,2);
        cur_dihedral_type->atom2_name = line.substr(3,2);
        cur_dihedral_type->atom3_name = line.substr(6,2);
        cur_dihedral_type->atom4_name = line.substr(9,2);
        cur_dihedral_type->Vn = atof(line.substr(17,7).c_str()) / atof(line.substr(13,2).c_str());
        cur_dihedral_type->n = atof(line.substr(32,7).c_str());
        cur_dihedral_type->gamma = atof(line.substr(48,6).c_str());
        
        n_dihedral_types++;
        cout << "name1: " << cur_dihedral_type->atom1_name << " name2: " << cur_dihedral_type->atom2_name << " name3: " << cur_dihedral_type->atom3_name << " name4: " << cur_dihedral_type->atom4_name << " Vn:" << cur_dihedral_type->Vn << " n:" << cur_dihedral_type->n << " gamma:" << cur_dihedral_type->gamma << endl;
        cur_dihedral_type = &dihedral_type_list[n_dihedral_types];
      } else { // then don't include this line, it is a comment
        cout << "Skipping line: " << line << endl;
      }
    }
  }
  ff_dihedral.close();
  return n_dihedral_types;
}


double uniform(double lower, double upper) { // samples a random number from a uniform distribution between lower and upper
  return (lower + ((upper - lower)*(double) rand() / RAND_MAX));
}

double box_muller_transform() {
  double u, v, z0, z1, s=0.0; 
  // randomly samples from a normal distribution
  while (s >= 1.0 || s == 0.0) { // make sure we get between 0 and 1.0
    u = uniform(-1.0, 1.0); // random double between -1 and 1
    v = uniform(-1.0, 1.0); // random double between -1 and 1
    s = u*u + v*v;
    //cout << "s: " << s << " u: " << u << " v: " << v << endl;
  }
  z0 = u * sqrt((-2 * log(s))/s); // generates two normally distributed variables,
  z1 = v * sqrt((-2 * log(s))/s); //  but we only need one :(
  //cout << "z0: " << z0 << endl;
  return z0;
}
/*
double rand_maxwell_dist(double m, double T) {
  double rand_var;
  double vel; // momentum squared
  //srand(seed); // assign seed to random number generator
  
  vel = sqrt(-((2*k*T) / m) * log ( abs(rand_var) * sqrt((2*PI*k*T)/m)));
  if (rand_var < 0.0) vel *= -1.0; // make the velocity negative if the random variable is negative
  return vel;
  
}
*/
int random_velocity(Atom *curatom, double T) {
  double m;
  m = curatom->mass; // mass of the atom
  curatom->vx0 = sqrt(k*T/m)*box_muller_transform();
  curatom->vy0 = sqrt(k*T/m)*box_muller_transform(); // assign random velocities in x,y,z
  curatom->vz0 = sqrt(k*T/m)*box_muller_transform();
}

int assign_random_velocities(int n, Atom *atom_list, double T) {
  /*  Given n: a number of atoms, an atom list, and a temperature, will assign each atom a velocity from a maxwell-Boltzmann dist.*/
  int i; 
  cout << "Assigning Random Velocities\n";
  Atom *curatom; // modify the object by reference
  double m, v;
  for(i=0; i<n; i++) { // run thru each atom
    curatom = &atom_list[i]; // get the current atom
    random_velocity(curatom, T); 
     //cout << " vx0: " << curatom.vx0 << " vy0: " << curatom.vy0 << " vz0: " << curatom.vz0 << endl;
  }
  return 0;
}

int make_interaction_matrix(int n, Atom *atom_list, Bond *bond_list, int n_bonds, Angle *angle_list, int n_angles, Dihedral *dihedral_list, int n_dihedrals, int **interaction_matrix) {
  /* populates in interaction matrix based on a topology file
  0 = self, 1 = bonded, 2 = nonbonded */
  int i, j;
  for (i=0; i<n; i++) {
    for (j=0; j<n; j++) {
      if (j==i) interaction_matrix[i][j] = 0; // then this is just ourself
      // there needs to eventually be a case for bonded
      else interaction_matrix[i][j] = 2; // nonbonded
    }
  }
  // now go thru and fill out all the bonded interactions
  for(i=0;i<n_bonds;i++) {
    interaction_matrix[bond_list[i].atom1->index][bond_list[i].atom2->index] = 1; // 1 means that its a bonded interaction
    interaction_matrix[bond_list[i].atom2->index][bond_list[i].atom1->index] = 1; // set both sides of the matrix
  }
  for(i=0;i<n_angles;i++) {
    interaction_matrix[angle_list[i].atom1->index][angle_list[i].atom3->index] = 1; // 1 means that its a bonded interaction
    interaction_matrix[angle_list[i].atom3->index][angle_list[i].atom1->index] = 1; // set both sides of the matrix
  }
  for(i=0;i<n_dihedrals;i++) {
    interaction_matrix[dihedral_list[i].atom1->index][dihedral_list[i].atom4->index] = 1; // 1 means that its a bonded interaction
    interaction_matrix[dihedral_list[i].atom4->index][dihedral_list[i].atom1->index] = 1; // set both sides of the matrix
  }
  return 0;
}

int calc_dist_matrix(int n, Atom *atom_list, double **dist_matrix) {
  /* populates distance matrix by calculating all atom pairwise distances */
  int i, j;
  double x0, y0, z0, x1, y1, z1, dist;
  for (i=0; i<n; i++) {
    x0 = atom_list[i].rx0; y0 = atom_list[i].ry0; z0 = atom_list[i].rz0; // location of atom i
    for (j=0; j<n; j++) {
      x1 = atom_list[j].rx0; y1 = atom_list[j].ry0; z1 = atom_list[j].rz0; // location of atom j
      dist = sqrt(((x1-x0)*(x1-x0))+((y1-y0)*(y1-y0))+((z1-z0)*(z1-z0))); // get the distance between the atoms
      dist_matrix[i][j] = dist; // add the value to the matrix
    }
  }
  return 0;
}


double pressure_convert(double P) { // convert amu / fs^2 * A to Pascals (kg / m * s^2)
  return  P * 1.0e10 * 1.0e30 / (AVO * 1.0e30);
}


int make_vdw_matrices(int n, Atom *atom_list, double **epsilon_matrix, double **sigma_matrix) {
  /* populates the epsilon and sigma vdw matrices */
  int i, j;
  for (i=0; i<n; i++) {
    for (j=0; j<n; j++) {
      epsilon_matrix[i][j] = atom_list[i].vdw_epsilon + atom_list[j].vdw_epsilon; // kJ per mol -> A^2 * amu / fs^2
      sigma_matrix[i][j] = atom_list[i].vdw_radius + atom_list[j].vdw_radius; // in angstroms
    }
  }
  return 0;
}

double potential_energy(int n, Atom *atom_list, int index, double **epsilon_matrix, double **sigma_matrix, int **interaction_matrix) {
  // gets the potential energy of a particle's next timestep
  int i, j;
  double rx, ry, rz, r_2, sigma, sigma_6, sigma_12, epsilon, U=0.0;
  i = index;
  if (VDW_FORCES == true) {
    for (j=i+1;j<n;j++) { // run thru all other atoms
      if (interaction_matrix[i][j] != 2) continue; // don't evaluate distance to ourself
      rx = atom_list[i].rx1 - atom_list[j].rx1;
      ry = atom_list[i].ry1 - atom_list[j].ry1; // get difference vector
      rz = atom_list[i].rz1 - atom_list[j].rz1;
      epsilon = epsilon_matrix[i][j];
      sigma = sigma_matrix[i][j]; sigma_6 = pow(sigma,6.0); sigma_12 = pow(sigma,12.0);
      r_2 = rx*rx + ry*ry + rz*rz; // r^2: distance between the two points squared
      U += 4.0 * epsilon * ((sigma_12/pow(r_2,6.0)) - (sigma_6/pow(r_2,3.0))); // update potential energy
    } 
  }
  return U;
}

double kinetic_energy(int n, Atom *atom_list, int index) {
  // gets the kinetic energy of a particle's next timestep
  double vx, vy, vz;
  vx = atom_list[index].vx1; vy = atom_list[index].vy1; vz = atom_list[index].vz1;
  return 0.5 * atom_list[index].mass * (vx*vx + vy*vy + vz*vz); // K = 1/2 * m * |v|^2 
}

double vecs2angle(Atom *atoms) {
  double ax, ay, az, bx, by, bz;
  ax = atoms[0].rx1 - atoms[1].rx1;
  ay = atoms[0].ry1 - atoms[1].ry1;
  az = atoms[0].rz1 - atoms[1].rz1;
  bx = atoms[2].rx1 - atoms[1].rx1;
  by = atoms[2].ry1 - atoms[1].ry1;
  bz = atoms[2].rz1 - atoms[1].rz1;
  return acos( (ax*bx + ay*by + az*bz) / sqrt((ax*ax + ay*ay + az*az)*(bx*bx + by*by + bz*bz)) );
} 

double get_next_accel(int n, Atom *atom_list, Bond *bond_list, int n_bonds, Angle *angle_list, int n_angles, Dihedral *dihedral_list, int n_dihedrals, int **interaction_matrix, double **dist_matrix, double **epsilon_matrix, double **sigma_matrix) {
  int i, j;
  double rx, ry, rz, r, r_2, r_2_4, r_2_7; // distance metrics between the points
  double epsilon, sigma, sigma_6, sigma_12, fx=0.0, fy=0.0, fz=0.0, f_holder;
  double fx1=0.0, fy1=0.0, fz1=0.0, fx2=0.0, fy2=0.0, fz2=0.0;
  double U = 0.0; // potential energy
  double dot, angle, eq_angle, mag1, mag2;
  double ax, ay, az, bx, by, bz, len_A_sq, len_B_sq, len_A, len_B, A_dot_B, interior, dU_dTheta, dAcos_dinterior;
  double dinterior_dAx, dinterior_dAy, dinterior_dAz, dinterior_dBx, dinterior_dBy, dinterior_dBz;
  Atom *atom[4]; // a placeholder for atoms
  for (i=0;i<n;i++) {
    atom_list[i].ax1 = 0.0;
    atom_list[i].ay1 = 0.0; // first initialize no forces, so its easy to run a no-force simulatino
    atom_list[i].az1 = 0.0;
  }
  for (i=0;i<n;i++) {
    //fx=0.0; fy=0.0; fz=0.0;
    if (VDW_FORCES == true) {
      for (j=i+1;j<n;j++) { // run thru all other atoms
        if (interaction_matrix[i][j] != 2) continue; // don't evaluate distance to ourself
        rx = atom_list[i].rx1 - atom_list[j].rx1;
        ry = atom_list[i].ry1 - atom_list[j].ry1; // get difference vector
        rz = atom_list[i].rz1 - atom_list[j].rz1;
        epsilon = epsilon_matrix[i][j];
        sigma = sigma_matrix[i][j]; sigma_6 = pow(sigma,6.0); sigma_12 = pow(sigma,12.0);
        r_2 = rx*rx + ry*ry + rz*rz; // r^2: distance between the two points squared
        r_2_4 = pow(r_2, -4.0); r_2_7 = pow(r_2, -7.0);
        f_holder = 24 * epsilon * (2*sigma_12*r_2_7 - sigma_6*r_2_4); // just a holder term for this expression to save computation
        fx = rx * f_holder;
        fy = ry * f_holder;
        fz = rz * f_holder;
        U += 4.0 * epsilon * ((sigma_12/pow(r_2,6.0)) - (sigma_6/pow(r_2,3.0))); // update potential energy
        //cout << "vdw forces: " << fx << " " << fy << " " << fz << endl;
        //U += 4 * epsilon * ((sigma_12/(r_2*r_2*r_2*r_2*r_2*r_2)) - (sigma_6/(r_2*r_2*r_2*r_2*r_2*r_2*r_2*r_2*r_2*r_2*r_2*r_2))); // update potential energy
        atom_list[j].ax1 -= fx / atom_list[j].mass; 
        atom_list[j].ay1 -= fy / atom_list[j].mass; // get acceleration from forces
        atom_list[j].az1 -= fz / atom_list[j].mass; 
        atom_list[i].ax1 += fx / atom_list[i].mass; 
        atom_list[i].ay1 += fy / atom_list[i].mass; // get acceleration from forces
        atom_list[i].az1 += fz / atom_list[i].mass; 
      }
    }
    
    if (COULOMB_FORCES == true) {
      for (j=i+1;j<n;j++) { // run thru all other atoms
        if (interaction_matrix[i][j] != 2) continue; // don't evaluate distance to ourself
        rx = atom_list[i].rx1 - atom_list[j].rx1;
        ry = atom_list[i].ry1 - atom_list[j].ry1; // get difference vector
        rz = atom_list[i].rz1 - atom_list[j].rz1;
        r_2 = rx*rx + ry*ry + rz*rz; // r^2: distance between the two points squared
        
        f_holder = (atom_list[i].charge * atom_list[j].charge) / (4 * PI * PERMITTIVITY * pow(r_2, 1.5)); // just a holder term for this expression to save computation
        fx = rx * f_holder;
        fy = ry * f_holder;
        fz = rz * f_holder;
        U += (atom_list[i].charge * atom_list[j].charge) / (4 * PI * PERMITTIVITY * sqrt(r_2)); // update potential energy
        //cout << "elec forces: " << fx << " " << fy << " " << fz << endl;
        //U += 4 * epsilon * ((sigma_12/(r_2*r_2*r_2*r_2*r_2*r_2)) - (sigma_6/(r_2*r_2*r_2*r_2*r_2*r_2*r_2*r_2*r_2*r_2*r_2*r_2))); // update potential energy
        atom_list[j].ax1 -= fx / atom_list[j].mass; 
        atom_list[j].ay1 -= fy / atom_list[j].mass; // get acceleration from forces
        atom_list[j].az1 -= fz / atom_list[j].mass; 
        atom_list[i].ax1 += fx / atom_list[i].mass; 
        atom_list[i].ay1 += fy / atom_list[i].mass; // get acceleration from forces
        atom_list[i].az1 += fz / atom_list[i].mass; 
      }
    }
  }
  if (BOND_FORCES == true) {
    //cout << "Evaluating Bonds: " << n_bonds << endl;
    for(i=0;i<n_bonds;i++) {
      atom[0] = bond_list[i].atom1;
      atom[1] = bond_list[i].atom2;
      rx = atom[1]->rx1 - atom[0]->rx1;
      ry = atom[1]->ry1 - atom[0]->ry1;
      rz = atom[1]->rz1 - atom[0]->rz1;
      r = sqrt(rx*rx + ry*ry + rz*rz);
      fx = -2*bond_list[i].k*(1.0 - bond_list[i].eq/r)*rx;
      fy = -2*bond_list[i].k*(1.0 - bond_list[i].eq/r)*ry;
      fz = -2*bond_list[i].k*(1.0 - bond_list[i].eq/r)*rz;
      //cout << "bond forces: " << fx << " " << fy << " " << fz << endl;
      atom[1]->ax1 += fx / atom[1]->mass;
      atom[1]->ay1 += fy / atom[1]->mass;
      atom[1]->az1 += fz / atom[1]->mass;
      atom[0]->ax1 -= fx / atom[0]->mass;
      atom[0]->ay1 -= fy / atom[0]->mass;
      atom[0]->az1 -= fz / atom[0]->mass;
    }
  }
    
  if (ANGLE_FORCES == true) {
    for(i=0;i<n_angles;i++) {
      atom[0] = angle_list[i].atom1;
      atom[1] = angle_list[i].atom2;
      atom[2] = angle_list[i].atom3;
      ax = atom[0]->rx1 - atom[1]->rx1;
      ay = atom[0]->ry1 - atom[1]->ry1;
      az = atom[0]->rz1 - atom[1]->rz1;
      bx = atom[2]->rx1 - atom[1]->rx1;
      by = atom[2]->ry1 - atom[1]->ry1;
      bz = atom[2]->rz1 - atom[1]->rz1;
      len_A_sq = ax*ax + ay*ay + az*az;
      len_B_sq = bx*bx + by*by + bz*bz;
      len_A = sqrt(len_A_sq);
      len_B = sqrt(len_B_sq);
      A_dot_B = ax*bx + ay*by + az*bz;
      interior = A_dot_B / (len_A*len_B);
      angle = acos(interior);
      eq_angle = angle_list[i].eq;
      //cout << "atom[0].name" << atom[0]->name << "atom[1].name" << atom[1]->name << "atom[2].name" << atom[2]->name << endl;
      cout << "atom 0 vector: x:" << ax << " y: " << ay << " z: " << az << endl;
      cout << "atom 2 vector: x:" << bx << " y: " << by << " z: " << bz << endl;  
      cout << "angle: " << angle << " eq_angle: " << eq_angle << endl;
      dU_dTheta = 2*angle_list[i].k*(angle - eq_angle);
      dAcos_dinterior = 1.0/sqrt(1.0 - interior*interior);
      dinterior_dAx = (1.0/len_B)*(( len_A*bx - A_dot_B*ax/len_A) / len_A_sq);
      dinterior_dAy = (1.0/len_B)*(( len_A*by - A_dot_B*ay/len_A) / len_A_sq);
      dinterior_dAz = (1.0/len_B)*(( len_A*bz - A_dot_B*az/len_A) / len_A_sq);
      dinterior_dBx = (1.0/len_A)*(( len_B*ax - A_dot_B*bx/len_B) / len_B_sq);
      dinterior_dBy = (1.0/len_A)*(( len_B*ay - A_dot_B*by/len_B) / len_B_sq);
      dinterior_dBz = (1.0/len_A)*(( len_B*az - A_dot_B*bz/len_B) / len_B_sq);
      
      fx1 = dU_dTheta*dAcos_dinterior*dinterior_dAx;
      fy1 = dU_dTheta*dAcos_dinterior*dinterior_dAy;
      fz1 = dU_dTheta*dAcos_dinterior*dinterior_dAz;
      fx2 = dU_dTheta*dAcos_dinterior*dinterior_dBx;
      fy2 = dU_dTheta*dAcos_dinterior*dinterior_dBy;
      fz2 = dU_dTheta*dAcos_dinterior*dinterior_dBz;
      cout << "atom 0 forces: x:" << fx1 << " y: " << fy1 << " z: " << fz1 << endl;
      cout << "atom 2 forces: x:" << fx2 << " y: " << fy2 << " z: " << fz2 << endl;      
      
      // NOTE: to be continued
      atom[2]->ax1 += fx1 / atom[2]->mass;
      atom[2]->ay1 += fy1 / atom[2]->mass;
      atom[2]->az1 += fz1 / atom[2]->mass;
      atom[0]->ax1 += fx2 / atom[0]->mass;
      atom[0]->ay1 += fy2 / atom[0]->mass;
      atom[0]->az1 += fz2 / atom[0]->mass;
    }
  }
  
  if (DIHEDRAL_FORCES == true) {
  
  }
  return U;
}

double gaussian_thermostat(int n, Atom *atom_list, double T_goal) {
  // returns the gaussian thermostat factor with which to rescale all particle velocities
  int g = 3*n - 1, i;
  double const_K = (double) g*k*T_goal;
  double numerator_sum = 0.0, m, alpha;
  for (i=0;i<n;i++) {
    m = atom_list[i].mass;
    numerator_sum += m * ((atom_list[i].vx0 * atom_list[i].ax0) + (atom_list[i].vy0 * atom_list[i].ay0) + (atom_list[i].vz0 * atom_list[i].az0)); // sum of dot between momentum and force / mass
  }
  alpha = numerator_sum / const_K;
  //cout << "Gaussian Thermostat alpha: " << alpha << endl;
  return alpha;
}

double berendsen_thermostat(double T_goal, double T_current) {
  // generates the factor by which the momenta of the atoms will be adjusted
  return sqrt(1 + (BERENDSEN_TAU)*((T_goal/T_current)-1));
}

int langevin_thermostat(int n, Atom *atom_list, double T_goal) {
  // adjusts the momenta of all atoms by imposing a drag force, as well as random kicks according to a Langevin Eq.
  int i, j;
  double sigma; // the stdev of the random kick distribution
  for (i=0;i<n;i++) {
    sigma = sqrt(2.0*LANGEVIN_DAMPING*k*T_goal/atom_list[i].mass);
    //cout << "sigma: " << sigma << endl;
    //cout << "velocity before: " << atom_list[i].vx1;
    atom_list[i].vx1 = atom_list[i].vx1 + (-atom_list[i].vx1*LANGEVIN_DAMPING + sigma*box_muller_transform())*dt;
    atom_list[i].vy1 = atom_list[i].vy1 + (-atom_list[i].vy1*LANGEVIN_DAMPING + sigma*box_muller_transform())*dt;
    atom_list[i].vz1 = atom_list[i].vz1 + (-atom_list[i].vz1*LANGEVIN_DAMPING + sigma*box_muller_transform())*dt;
    //cout << " random kick: " << (sigma*box_muller_transform())*dt << " friction:" << -atom_list[i].vx1*LANGEVIN_DAMPING << " velocity after: " << atom_list[i].vx1 << endl;
  }
  return 0;
}

double atom_speed(Atom atom) {
  return sqrt((atom.vx0*atom.vx0) + (atom.vy0*atom.vy0) + (atom.vz0*atom.vz0));
}

double calculate_kinetic_energy(int n, Atom *atom_list){
  int i;
  // Calculates the total kinetic energy of a system
  double K = 0.0; // total velocity squared
  for (i=0;i<n;i++) {
    K += ((atom_list[i].vx0 * atom_list[i].vx0) + (atom_list[i].vy0 * atom_list[i].vy0) + (atom_list[i].vz0 * atom_list[i].vz0)) * atom_list[i].mass * 0.5; // square speed
  }
  return K;
}

double calculate_temperature(int n, Atom *atom_list){
  double K, T;
  K = calculate_kinetic_energy(n, atom_list);
  T = (2.0*K/ (double) (3.0*k*n));
  return T;
}

double velocity_verlet(int n, Atom *atom_list, Bond *bond_list, int n_bonds, Angle *angle_list, int n_angles, Dihedral *dihedral_list, int n_dihedrals, int **interaction_matrix, double **dist_matrix, double **epsilon_matrix, double **sigma_matrix, double T_goal) {
  int i;
  double U, T_current; // potential energy
  double thermo_factor = 1.0; // alpha: constrained force term
  // get next positions
  for (i=0;i<n;i++) {
    atom_list[i].rx1 = atom_list[i].rx0 + atom_list[i].vx0*dt + 0.5*atom_list[i].ax0*dt*dt;
    atom_list[i].ry1 = atom_list[i].ry0 + atom_list[i].vy0*dt + 0.5*atom_list[i].ay0*dt*dt;
    atom_list[i].rz1 = atom_list[i].rz0 + atom_list[i].vz0*dt + 0.5*atom_list[i].az0*dt*dt;
    //cout << "pos: " << atom_list[i].rx1 << endl;
  }
  // get next accelerations
  U = get_next_accel(n, atom_list, bond_list, n_bonds, angle_list, n_angles, dihedral_list, n_dihedrals, interaction_matrix, dist_matrix, epsilon_matrix, sigma_matrix);
  T_current = calculate_temperature(n, atom_list);
  //cout << "Goal Temperature: " << T_goal << " Current T: " << T_current << endl;
  // gaussian thermostat
  if (GAUSSIAN_THERMOSTAT == true) thermo_factor = 1-gaussian_thermostat(n, atom_list, T_goal);
  if (BERENDSEN_THERMOSTAT == true) thermo_factor = berendsen_thermostat(T_goal, T_current);
  
  //cout << "thermo factor: " << thermo_factor << endl; 
  // get next velocities
  for (i=0;i<n;i++) {
    //cout << "accel: " << atom_list[i].ax0 << "," << atom_list[i].ax1 << endl;
    atom_list[i].vx1 = atom_list[i].vx0*thermo_factor + 0.5*(atom_list[i].ax0 + atom_list[i].ax1)*dt; 
    atom_list[i].vy1 = atom_list[i].vy0*thermo_factor + 0.5*(atom_list[i].ay0 + atom_list[i].ay1)*dt; // this last factor is for the case of when using the Gaussian thermostat
    atom_list[i].vz1 = atom_list[i].vz0*thermo_factor + 0.5*(atom_list[i].az0 + atom_list[i].az1)*dt; 
    //cout << "vel: " << atom_list[i].vx1 << endl;
  }
  if (LANGEVIN_THERMOSTAT == true) langevin_thermostat(n, atom_list, T_goal); // then impose the Langevin Thermostat
  // test for barrier crossings
  
  return U;
}



int print_sys_info(int n, Atom *atom_list, double U, double momentum_change, double step, double temperature) {
  int i, j;
  double K, H, P, T; // kinetic energy, Total energy, Pressure, Temperature, added_square_speed
  // calculate total kinetic energy
  K = calculate_kinetic_energy(n, atom_list);
  H = U + K;
  T = (2.0*K/ (double) (3.0*k*n));
  P = (momentum_change) /  (step * dt * BOXAREA);
  cout << "STEP: " << step << ", ENERGY: Total: " << H << ", Kinetic: " << K << ", Potential: " << U << ", PRESSURE: " << P << ", NkT/V: " << n*k*T/BOXVOLUME << ", TEMPERATURE: " << T << endl;
  // estimate temperature/pressure
  
  return 0;
}

int print_pdb_trajectory(int n, Atom *atom_list, ofstream &pdbfile) {
  int i, j;
  char pdbline [100];
  //cout << "Writing frame to trajectory\n";
  for (i=0;i<n;i++) { // print every atom in the atom_list
    sprintf(pdbline, "ATOM  %5d %s %s  %4d    %8.3f%8.3f%8.3f  0.00  0.00  \n", i, atom_list[i].name.c_str(), atom_list[i].resname.c_str(), i, atom_list[i].rx0, atom_list[i].ry0, atom_list[i].rz0 ); 
    pdbfile << pdbline;
  }
  pdbfile << "ENDMDL\n";
  return 0;
}

int print_pdb_velocity_trajectory(int n, Atom *atom_list, ofstream &pdbfile) {
  int i, j;
  char pdbline [100];
  //cout << "Writing frame to trajectory\n";
  for (i=0;i<n;i++) { // print every atom in the atom_list
    sprintf(pdbline, "ATOM  %5d %s %s  %4d    %8.4f%8.4f%8.4f  0.00  0.00  \n", i, atom_list[i].name.c_str(), atom_list[i].resname.c_str(), i, atom_list[i].vx0, atom_list[i].vy0, atom_list[i].vz0 ); 
    pdbfile << pdbline;
  }
  pdbfile << "ENDMDL\n";
  return 0;
}

int advance_timestep(int n, Atom *atom_list) {
  int i, j;
  for (i=0;i<n;i++) {
    atom_list[i].rx0 = atom_list[i].rx1; atom_list[i].ry0 = atom_list[i].ry1; atom_list[i].rz0 = atom_list[i].rz1;
    atom_list[i].vx0 = atom_list[i].vx1; atom_list[i].vy0 = atom_list[i].vy1; atom_list[i].vz0 = atom_list[i].vz1;
    atom_list[i].ax0 = atom_list[i].ax1; atom_list[i].ay0 = atom_list[i].ay1; atom_list[i].az0 = atom_list[i].az1;
  }
  return 0;
}

double reflecting_boundary(int n, Atom *atom_list, double **epsilon_matrix, double **sigma_matrix, int **interaction_matrix, double T) {
  // reflects any atoms that have collided with the boundary, and also returns the momentum change
  int i, j;
  double delta_x; // the distance the atom has gone over the boundary
  double U_star; // the potential energy that it would have been
  double U1, U_diff; // the potential energy that it is going to be
  double K_star, K1;
  double v_star_mag, v1_mag, v_ratio; // the magnitude of the new v vector
  double momentum_change = 0.0;
  bool collision;
  for (i=0;i<n;i++) {
    U_diff = 0.0;
    collision = false;
    if (atom_list[i].rx1 < BOXDIMS[0]) {
      U_star = potential_energy(n, atom_list, i, epsilon_matrix, sigma_matrix, interaction_matrix);
      atom_list[i].vx1 = -1.0 * atom_list[i].vx1; // reverse the velocity
      delta_x = BOXDIMS[0] - atom_list[i].rx1;
      atom_list[i].rx1 = BOXDIMS[0] + delta_x; // place atom in correct position
      momentum_change += abs(atom_list[i].vx1 * atom_list[i].mass * 2.0);
      collision = true;
      if (ANDERSEN_BORDER == true) {
        random_velocity(&atom_list[i], T);
        atom_list[i].vx1 = abs(atom_list[i].vx1);
      }
    }
    if (atom_list[i].ry1 < BOXDIMS[1]) {
      U_star = potential_energy(n, atom_list, i, epsilon_matrix, sigma_matrix, interaction_matrix);
      atom_list[i].vy1 = -1.0 * atom_list[i].vy1; // reverse the velocity
      delta_x = BOXDIMS[1] - atom_list[i].ry1;
      atom_list[i].ry1 = BOXDIMS[1] + delta_x; // place atom in correct position
      momentum_change += abs(atom_list[i].vy1 * atom_list[i].mass * 2.0);
      collision = true;
      if (ANDERSEN_BORDER == true) {
        random_velocity(&atom_list[i], T);
        atom_list[i].vy1 = abs(atom_list[i].vy1);
      }
    }
    if (atom_list[i].rz1 < BOXDIMS[2]) {
      U_star = potential_energy(n, atom_list, i, epsilon_matrix, sigma_matrix, interaction_matrix);
      atom_list[i].vz1 = -1.0 * atom_list[i].vz1; // reverse the velocity
      delta_x = BOXDIMS[2] - atom_list[i].rz1;
      atom_list[i].rz1 = BOXDIMS[2] + delta_x; // place atom in correct position
      momentum_change += abs(atom_list[i].vz1 * atom_list[i].mass * 2.0);
      collision = true;
      if (ANDERSEN_BORDER == true) {
        random_velocity(&atom_list[i], T);
        atom_list[i].vz1 = abs(atom_list[i].vz1);
      }
    }
    if (atom_list[i].rx1 > BOXDIMS[3]) {
      U_star = potential_energy(n, atom_list, i, epsilon_matrix, sigma_matrix, interaction_matrix);
      atom_list[i].vx1 = -1.0 * atom_list[i].vx1; // reverse the velocity
      delta_x = BOXDIMS[3] - atom_list[i].rx1;
      atom_list[i].rx1 = BOXDIMS[3] + delta_x; // place atom in correct position
      momentum_change += abs(atom_list[i].vx1 * atom_list[i].mass * 2.0);
      collision = true;
      if (ANDERSEN_BORDER == true) {
        random_velocity(&atom_list[i], T);
        atom_list[i].vx1 = -abs(atom_list[i].vx1);
      }
    }
    if (atom_list[i].ry1 > BOXDIMS[4]) {
      U_star = potential_energy(n, atom_list, i, epsilon_matrix, sigma_matrix, interaction_matrix);
      atom_list[i].vy1 = -1.0 * atom_list[i].vy1; // reverse the velocity
      delta_x = BOXDIMS[4] - atom_list[i].ry1;
      atom_list[i].ry1 = BOXDIMS[4] + delta_x; // place atom in correct position
      momentum_change += abs(atom_list[i].vy1 * atom_list[i].mass * 2.0);
      collision = true;
      if (ANDERSEN_BORDER == true) {
        random_velocity(&atom_list[i], T);
        atom_list[i].vy1 = -abs(atom_list[i].vy1);
      }
    }
    if (atom_list[i].rz1 > BOXDIMS[5]) {
      U_star = potential_energy(n, atom_list, i, epsilon_matrix, sigma_matrix, interaction_matrix);
      atom_list[i].vz1 = -1.0 * atom_list[i].vz1; // reverse the velocity
      delta_x = BOXDIMS[5] - atom_list[i].rz1;
      atom_list[i].rz1 = BOXDIMS[5] + delta_x; // place atom in correct position
      momentum_change += abs(atom_list[i].vz1 * atom_list[i].mass * 2.0);
      collision = true;
      if (ANDERSEN_BORDER == true) {
        random_velocity(&atom_list[i], T);
        atom_list[i].vz1 = -abs(atom_list[i].vz1);
      }
    }
    if (collision == true) { // then get the new potential energy
      U1 = potential_energy(n, atom_list, i, epsilon_matrix, sigma_matrix, interaction_matrix);
      U_diff = U_star - U1;
    }
    // the velocity needs to be adjusted since the potential energy on different sides of the barrier are different
    // the total energy is conserved, so we only need to adjust the kinetic energy by the difference in potential nergy
    if (U_diff != 0.0 ) {
      cout << "Collision detected! Energy difference: " << U_diff << ". Adjusting particle velocity"<< endl;
      K_star = kinetic_energy(n, atom_list, i);
      v_star_mag = sqrt((atom_list[i].vx1 * atom_list[i].vx1) + (atom_list[i].vy1 * atom_list[i].vy1) + (atom_list[i].vz1 * atom_list[i].vz1));
      K1 = K_star + U_diff;
      //cout << "Old kinetic energy: " << K_star << " New kinetic E: " << K1 << "\n";
      v1_mag = sqrt(K1 * 2.0 / atom_list[i].mass);
      //cout << "Old velocity magnitude: " << v_star_mag << " New velocity mag: " << v1_mag << "\n";
      
      atom_list[i].vx1 = atom_list[i].vx1*(v1_mag / v_star_mag);
      atom_list[i].vy1 = atom_list[i].vy1*(v1_mag / v_star_mag);
      atom_list[i].vz1 = atom_list[i].vz1*(v1_mag / v_star_mag);
      //cout << "Adjusting velocity by: " << (v1_mag / v_star_mag) << " A/fs\n";
    }
  }
  return momentum_change;
}

int andersen_step() {
  // samples a random point from a poisson distribution to determine how long until the next Andersen kick
  return int(-ANDERSEN_NU * log(uniform(0.0,1.0)));
}

int andersen_kick(int n, Atom *atom_list, double T) {
  // chooses a random atom, then reassigns its velocity vector by the temperature according to a Maxwell Boltzmann distribution
  int random_i;
  random_i = int(uniform(0.0,n)); // choose a random atom
  random_velocity(&atom_list[random_i], T); // reassign the velocity vector randomly
}

int main(int argc, char *argv[]) {
  int n, n_atom_types, n_bond_types, n_angle_types, n_dihedral_types; // number of atoms
  int n_atoms=0, n_bonds=0, n_angles=0, n_dihedrals=0;
  int i, j;
  double t = 0.0, U;
  double momentum_change = 0.0;
  int step;
  double temperature = atof(argv[2]); // starting temperature
  int begin_time;
  bool andersen = false; // whether Andersen thermostat is being evaluated on this step
  int andersen_countdown = 0; // the number of timesteps until the next kick 
  Atom *cur_atom, *next_atom;
  srand(time(0)); // assign seed to random number generator
  //string test1 = "3.1415";
  //int test2;
  begin_time = time(0); // get time at beginning of simulation
  cout << "Initiating MD Engine...\n" << "Starting Temperature: " << temperature << endl;
  cout << "Parsing Forcefield files." << endl;
  ifstream atom_type_file; atom_type_file.open(ATOM_TYPE_FILENAME); ifstream bond_type_file; bond_type_file.open(BOND_TYPE_FILENAME); ifstream angle_type_file; angle_type_file.open(ANGLE_TYPE_FILENAME); ifstream dihedral_type_file; dihedral_type_file.open(DIHEDRAL_TYPE_FILENAME);
  Atom_type *atom_type_list = new Atom_type[MAX_ATOM_TYPES];
  Bond_type *bond_type_list = new Bond_type[MAX_BOND_TYPES];
  Angle_type *angle_type_list = new Angle_type[MAX_ANGLE_TYPES];
  Dihedral_type *dihedral_type_list = new Dihedral_type[MAX_DIHEDRAL_TYPES];
  n_atom_types = read_ff_atom(atom_type_file, atom_type_list);
  n_bond_types = read_ff_bond(bond_type_file, bond_type_list);
  n_angle_types = read_ff_angle(angle_type_file, angle_type_list);
  n_dihedral_types = read_ff_dihedral(dihedral_type_file, dihedral_type_list);
  cout << "Reading PDB file: " << argv[1] << "\n";
  ifstream pdb_file; // open the PDB file
  pdb_file.open(argv[1]); // first argument of program is PDB file name
  Atom *atom_list = new Atom[MAX_ATOMS]; // create a list of atoms
  n=read_pdb(pdb_file, atom_list, n_atom_types, atom_type_list); // read the pdb file and assign number of atoms
  pdb_file.close();
  cout << n << " atoms found.\n";
  Bond *bond_list = new Bond[MAX_BONDS];
  Angle *angle_list = new Angle[MAX_ANGLES];
  Dihedral *dihedral_list = new Dihedral[MAX_DIHEDRALS];
  cout << "Reading PSF file: " << endl;
  ifstream psf_file; // open the PSF file
  psf_file.open(argv[3]);
  read_psf(psf_file, n, atom_list, bond_list, &n_bonds, bond_type_list, n_bond_types, angle_list, &n_angles, angle_type_list, n_angle_types, dihedral_list, &n_dihedrals, dihedral_type_list, n_dihedral_types); // read the psf file
  psf_file.close();
  
  assign_random_velocities(n, atom_list, temperature); // assign random velocities
  
  
  //return 0;
  
  cout << "Constructing interaction tables\n" ;
  int **interaction_matrix; // make an nxn matrix for bonded, nonbonded interactions
  double **dist_matrix; // distance matrix between all atom pairs
  double **vdw_epsilon_matrix; // nxn matrix for VDW epsilon factor
  double **vdw_sigma_matrix; // nxn matrix for VDW sigma factor
  interaction_matrix = new int *[n]; // make the array of pointers
  dist_matrix = new double *[n];
  vdw_epsilon_matrix = new double *[n];
  vdw_sigma_matrix = new double *[n];
  // for more matrices
  for (i=0;i<n;i++) { // allocate memory for all the matrices
    interaction_matrix[i] = new int[n]; // make the array of pointers
    dist_matrix[i] = new double[n];
    vdw_epsilon_matrix[i] = new double[n];
    vdw_sigma_matrix[i] = new double[n];
    // for more matrices
  }  
  make_interaction_matrix(n, atom_list, bond_list, n_bonds, angle_list, n_angles, dihedral_list, n_dihedrals, interaction_matrix); // populate interaction matrix
  /*cout << "interaction matrix: \n";
  for(i=0;i<n;i++) {
    for(j=0;j<n;j++) {
      cout << interaction_matrix[i][j] << ", ";
    }
    cout << endl;
  }*/
  calc_dist_matrix(n, atom_list, dist_matrix); // populate distance matrix
  make_vdw_matrices(n, atom_list, vdw_epsilon_matrix, vdw_sigma_matrix); // populate vdw matrices
  
  string traj_filename = string("traj_") + argv[1]; // create the output trajectory
  string vel_traj_filename = string("veltraj_") + argv[1]; // create the output trajectory
  cout << "Opening file for trajectory: " << traj_filename << endl;
  ofstream traj_file; // declare the file
  ofstream vel_traj_file; // declare the file
  traj_file.open (traj_filename.c_str());
  if (VEL_TRAJ == true) vel_traj_file.open (vel_traj_filename.c_str()); // if we are writing a velocity trajectory
  cout << "Starting MD simulation\n";
  /*
  cout << "vdw epsilon: " << vdw_epsilon_matrix[3][9] << endl;
  cout << "vdw sigma: " << vdw_sigma_matrix[3][9] << endl;
  return 0;
  //atom_list[0].vy0 = -0.01;
  
  atom_list[0].rx0 = 45.0; atom_list[0].ry0 = 50.0; atom_list[0].rz0 = 50.0;
  atom_list[0].vx0 = 0.01; atom_list[0].vy0 = 0.0; atom_list[0].vz0 = 0.0;
  atom_list[1].rx0 = 55.0; atom_list[1].ry0 = 50.0; atom_list[1].rz0 = 50.0; 
  atom_list[1].vx0 = -0.01; atom_list[1].vy0 = 0.0; atom_list[1].vz0 = 0.0;
  */
  
  
  
  
  for (step=0;step<NUMSTEPS;step++) {
    // advance the timestep
    U = velocity_verlet(n, atom_list, bond_list, n_bonds, angle_list, n_angles, dihedral_list, n_dihedrals, interaction_matrix, dist_matrix, vdw_epsilon_matrix, vdw_sigma_matrix, temperature);
    cout << "on timestep: " << step << endl;
    momentum_change += reflecting_boundary(n, atom_list, vdw_epsilon_matrix, vdw_sigma_matrix, interaction_matrix, temperature);
    // write trajectory information
    if (step%ENERGY_FREQ == 0) print_sys_info(n, atom_list, U, momentum_change, double(step), temperature); // print energy, temp, pressure info
    //  print pdb trajectory
    if (step%TRAJ_FREQ == 0) {
      print_pdb_trajectory(n, atom_list, traj_file);
      if (VEL_TRAJ == true) print_pdb_velocity_trajectory(n, atom_list, vel_traj_file);
    }
    // Thermostat stuff
    if (ANDERSEN_THERMOSTAT == true) { // 
      if (andersen_countdown == 0) { // if this is the step to do an andersen kick
        andersen_kick(n, atom_list, temperature); // kick a random atom
        andersen_countdown = andersen_step(); // restart the countdown
        //cout << "andersen_countdown: " << andersen_countdown << endl;
      } else { andersen_countdown -= 1; } // otherwise, decrement the countdown      
    }
    // reset variables
    advance_timestep(n, atom_list);
  }
  //cout << "Epsilon: " << vdw_epsilon_matrix[2][3] << endl;
  cout << "Closing trajectory file\n";
  //cout << "Box area: " << BOXAREA << endl; 
  traj_file.close();
  cout << "Execution Time: " << time(0) - begin_time << " s" << endl;
  return 0;
}
