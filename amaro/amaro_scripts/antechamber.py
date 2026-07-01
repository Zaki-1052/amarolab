#By Andy Stokely

import os

def antechamber(path,name,charge):
	os.system('antechamber -i ' + path + name + '.cif -fi ccif -bk ' + name + ' -o '+ name + '.mol2 -fo mol2 -c bcc -nc ' + charge)
	os.system('find ' + path + ' -type f -not -name *py -not -name *cif -not -name *mol2 -delete')
	os.system('parmchk2 -i ' + name + '.mol2 -f mol2 -o ' + name + '.frcmod')
	with open(path + name + '.leap', 'w+') as leap:
		leap.write('source leaprc.gaff\n' + name + ' = loadmol2 ' + name + '.mol2\nsaveoff ' + name + ' ' + name + '.lib\nquit')
		leap.close()
	os.system('tleap -f ' + path + name + '.leap')
	return

# antechamber('/home/andy/leap/','BEN','0')
