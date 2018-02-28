import os
import numpy as np
import xml.etree.ElementTree as ET


def max_update(master,new):
    '''
    Checks the individual number of atoms for
    a molecule and the current mak value for each atom.
    The purpose is to know the full dimenson necessary
    to handle every single molecule in the dataset.
    '''
    for key in new:
        if(key in master.keys()):
            if(master[key] < new[key]): 
                master[key] = new[key]
        else:
            master[key] = new[key]


def output2file(mol_dict):
    '''
    For each molecule in the dataset dictionary,
    this function writes the data to an individual 
    csv file in the data/ folder
    '''

    for mol in mol_dict:

        # Check for incomplete data
        try:
            temp = mol_dict[mol][2]
        except:
            continue

        filename = mol + '.csv'
        molfile = open('data/' + filename,'w')

        # Get Data from molecule dictionary
        empirical = ''
        for atom in mol_dict[mol][0]:
            empirical += atom + str(mol_dict[mol][0][atom])

        peakline = ''
        for peak in range(len(mol_dict[mol][2])):
            peakline += str(mol_dict[mol][2][peak][0]) + ' ' \
                      + str(mol_dict[mol][2][peak][1]) + ' ' \
                      + str(mol_dict[mol][2][peak][2]) + '\n'

        elemstr = mol_dict[mol][1][0]
        graph = mol_dict[mol][1][1]

        # Write to individual .csv file
        molfile.write('Empirical formula: ' + empirical + '\n')
        molfile.write('peakLocation peakArea peakMultiplicity' + '\n')
        molfile.write(peakline)
        molfile.write('Connectivity Matrix' + '\n')
        molfile.write(elemstr + '\n')
        for i in range(len(graph)):
            for j in range(len(graph)):
                molfile.write(str(graph[i,j]) + ' ')
            molfile.write('\n')
        molfile.close()



#------ Main Parsing Section ------

# Read in custom XML file
tree = ET.parse("nmrshiftdb2.xml")
root = tree.getroot()

# initialize max size testing dictionary
maxed = {}

# Parse Molecule object from XML file
molecules = {}
for mol in root.findall('{www.xml-cml.org/schema/schema24/schema.xsd}molecule'):
    ident = mol.attrib['id']
    atoms = mol.find('{www.xml-cml.org/schema/schema24/schema.xsd}atomArray')


    
    # Calculate empirical formula and num of atoms
    empirical = {}
    atomcount = 0
    elemstr = ''
    for i in atoms:
        elem = i.attrib['elementType']
        elemstr += elem + ' '
        atomcount += 1
        if(elem in empirical):
            empirical[elem] += 1
        else:
            empirical[elem]  = 1

    molecules[ident] = [empirical]

    # Make molecular graph
    bonds = mol.find('{www.xml-cml.org/schema/schema24/schema.xsd}bondArray')
    bondorder = {'S': 1, 'D': 2, 'T': 3, 'Q': 4}
    bondinfo = []
    graph = np.zeros((atomcount,atomcount),dtype=int)
    for i in bonds:
        bstr = i.attrib['atomRefs2'].split()
        indx1 = int(bstr[0][1:]) - 1
        indx2 = int(bstr[1][1:]) - 1
        order = bondorder[i.attrib['order']]

        # Make full, redundant graph matrix
        graph[indx1,indx2] = order
        graph[indx2,indx1] = order

    molecules[ident].append([elemstr,graph])

    # Remove fringe case compounds
    atoms_wanted = ['C', 'O', 'N', 'H', 'S', 'F', 'Cl', 'Br', 'P', 'B', 'I']
    for i in atoms:
        if(i.attrib['elementType'] not in atoms_wanted):
            molecules.pop(ident,0)
            break
        else:
            pass




# Parse Spectrum object from XML file
ppmMinMax = {'Max': 0., 'Min': 1000.}
for spec in root.findall('{www.xml-cml.org/schema/schema24/schema.xsd}spectrum'):
    molref = spec.attrib['moleculeRef']

    # Get NMR type
    nmrtype = []
    for n in spec.find('{www.xml-cml.org/schema/schema24/schema.xsd}metadataList'):
        nmrtype.append(n.attrib['content'])

    # Get peaks for 13C NMR
    nmrpeaks = []
    if('13C' in nmrtype and molref in molecules):

        for peak in spec.find('{www.xml-cml.org/schema/schema24/schema.xsd}peakList'):
            
            # Get max range of ppm's in dataset
            ppm = float(peak.attrib['xValue'])
            if(ppmMinMax['Max'] < ppm):
                ppmMinMax['Max'] = ppm
            if(ppmMinMax['Min'] > ppm):
                ppmMinMax['Min'] = ppm

            # Initialize variables
            intcount = None
            mult = None

            # Get number of atoms associated with peak
            try:
                integrate = peak.attrib['atomRefs']
                intcount = 1
                for i in integrate:
                    if(i == ' '): 
                        intcount += 1
            except:
                pass

            # Get multiplicity of peak
            try:
                mult = peak.attrib['peakMultiplicity']
            except:
                pass

            nmrpeaks.append([peak.attrib['xValue'],intcount,mult])

        max_update(maxed,molecules[molref][0])
        molecules[molref].append(nmrpeaks)
 
    else:
        molecules.pop(molref,0)



#print('MAX: ', maxed)
#print('SIZE: ', len(molecules))
#print('PPMRANGE: ', ppmMinMax)


# Write to data files
output2file(molecules)

    



