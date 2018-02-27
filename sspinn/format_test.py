import os
import xml.etree.ElementTree as ET

# FORMAT OUTPUT AS:
'''

empirical formula: <xxx>
Peak Location, Peak area, Peak Multiplicity
<xxx>,<xxx>,<xxx>
...
...
Connectivity matrix
x_11,...,x_1n
...
x_n1,....,x_nn

'''



def output2file(mol_dict):
    for mol in mol_dict:
        filename = mol + '.mol'
        molfile = open('data/' + filename,'w')

        # Get Data from molecule dictionary
        empirical = ''
        for atom in mol_dict[mol][0]:
            empirical += atom + str(mol_dict[mol][0][atom])

        peakline = ''
        for peak in range(len(mol_dict[mol][1])):
            peakline += str(mol_dict[mol][1][peak][0]) + ',' \
                      + str(mol_dict[mol][1][peak][1]) + ',' \
                      + str(mol_dict[mol][1][peak][2]) + '\n'


        # Write to individual file
        molfile.write('Empirical formula: ' + empirical + '\n')
        molfile.write('Peak Location, Peak area, Peak Multiplicity' + '\n')
        molfile.write(peakline)
        molfile.write('Connectivity Matrix' + '\n')
        molfile.close()


# Read in custom XML file
tree = ET.parse("nmrshiftdb2.xml")
root = tree.getroot()


count = 0
molecules = {}
for mol in root.findall('{www.xml-cml.org/schema/schema24/schema.xsd}molecule'):
    count += 1
    ident = mol.attrib['id']
    atoms = mol.find('{www.xml-cml.org/schema/schema24/schema.xsd}atomArray')
    
    # Calculate empirical formula
    empirical = {}
    for i in atoms:
        elem = i.attrib['elementType']
        
        if(elem in empirical):
            empirical[elem] += 1
        else:
            empirical[elem]  = 1
    #print(empirical)

    molecules[ident] = [empirical]



    if(count > 10): break

#print(molecules)


count2 = 0
for spec in root.findall('{www.xml-cml.org/schema/schema24/schema.xsd}spectrum'):
    count2 += 1
    molref = spec.attrib['moleculeRef']
     
    # Get NMR type
    nmrtype = []
    for n in spec.find('{www.xml-cml.org/schema/schema24/schema.xsd}metadataList'):
        nmrtype.append(n.attrib['content'])

    # Get peaks for 13C NMR
    nmrpeaks = []
    if('13C' in nmrtype):
        for peak in spec.find('{www.xml-cml.org/schema/schema24/schema.xsd}peakList'):

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


    # FIXME?: do this later once sure there is no 13C NMR spectra
    if('13C' not in nmrtype):
        molecules.pop(molref,0)
    else:
        molecules[molref].append(nmrpeaks)


    if(count2 > 10): break

#print('MOLECULES: ',molecules)

output2file(molecules)





'''
count2 = 0
for spec in root.findall('{www.xml-cml.org/schema/schema24/schema.xsd}spectrum'):
    count2 += 1
    molref = spec.attrib['moleculeRef']
     
    # Get NMR type
    nmrtype = []
    for n in spec.find('{www.xml-cml.org/schema/schema24/schema.xsd}metadataList'):
        nmrtype.append(n.attrib['content'])

    # Get peak for 1H NMR
    nmrpeaks = []
    if('1H' in nmrtype):
        for peak in spec.find('{www.xml-cml.org/schema/schema24/schema.xsd}peakList'):
            #integrate = peak.attrib['atomRefs']
            integrate = peak.find('{www.xml-cml.org/schema/schema24/schema.xsd}atomRefs')
            intcount = 1
            if(integrate != None):
                for i in integrate:
                    if(i == ' '): 
                        intcount += 1
            mult = peak.find('{www.xml-cml.org/schema/schema24/schema.xsd}peakMultiplicity')
            if(mult != None): print(mult)
            #if(peak.attrib['peakMultiplicity'] != None):
            #    print(peak.attrib['peakMultiplicity'])
            #else:
            #    pass
            nmrpeaks.append([peak.attrib['xValue'],intcount,],peak.attrib['xValue'])



    # FIXME?: do this later once sure there is no 1H NMR spectra
    if('1H' not in nmrtype):
        molecules.pop(molref,0)
    else:
        molecules[molref].append(nmrpeaks)


    if(count2 > 60): break

print(molecules)


'''


'''
count = 0
confirm = False
for branch in root:
    count += 1
    #print('Branch: ',branch.tag)
    switch = False
    try:
        if(branch.attrib['title'] == 'Tetrafluoroborate'):
            print(branch.attrib['title'])
            switch = True
            
    except:
        continue

    if(switch):
        for child in branch:
            #for i in child:            
            print('Child: ',child)
            for i in child:
                print(i.tag,i.attrib)

            if("bondArray" in child.tag):
                for k in child:
                    print(k.tag,k.attrib)
            
            if("peakList" in child.tag):
                for i in child:
                    print(i.tag,i.attrib)
            if("atomArray" in child.tag):
                for i in child:
                    print(i.attrib,i.attrib['elementType'])
'''



'''
count = 0
confirm = False

for i, branch in enumerate(root):

    count += 1
    print(i, branch)
    for obj in branch:
        if('moleculeRef' in obj):
            print(branch['moleculeRef'])
        print(obj)
    #if molecule():
        #find spectrum id

    #else


    if(count > 10):
        break
'''

'''
for i, mol in enumerate(root):
    count += 1
    print('Molecule: ',mol.attrib)

    for prop in mol:
        print('Property: ',prop)
        #for i in prop:
        #    print(i.tag,i.attrib)

        if("atomArray" in prop.tag):
            empirical = {}
            for k in prop:
                print('ATOMS: ',k.attrib['elementType'])
                elem = k.attrib['elementType']
                
                if(elem in empirical):
                    empirical[elem] += 1
                else:
                    empirical[elem]  = 1
                


            print('COUNT: ',empirical)
            
        
        if("peakList" in prop.tag):
            for i in prop:
                print(i.tag,i.attrib)
        if("atomArray" in prop.tag):
            for i in prop:
                print(i.attrib,i.attrib['elementType'])
        

    if(count > 3):
        break

'''

