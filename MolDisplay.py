import molecule

#Define the following constants:

header = """<svg version="1.1" width="1000" height="1000"
xmlns="http://www.w3.org/2000/svg">"""

footer = """</svg>"""
offsetx = 500
offsety = 500

# Class for an Atom
class Atom:
    # Constructor for a atom
    def __init__(self, c_atom):
        # set atom and z value
        self.atom = c_atom
        self.z = c_atom.z

    # Method to return a string representation of an atom
    def __str__(self):
        return f"Element:{self.atom.element} X:{self.atom.x} Y:{self.atom.y} Z:{self.z}"

    # Method to return a svg string representation of an atom
    def svg(self):
        # Calculate coordinates
        xTemp = (self.atom.x * 100.0) + offsetx
        yTemp = (self.atom.y * 100.0) + offsety
        # Get radius and colour
        r = radius[self.atom.element]
        colour = element_name[self.atom.element]
        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (xTemp, yTemp, r, colour)

# Class for a Bond
class Bond:
    # Constructor for a bond
    def __init__(self, c_bond):
        # set bond and z value
        self.bond = c_bond
        self.z = c_bond.z

    # Method to return a string representation of a bond
    def __str__(self):
        return f"x1:{self.bond.x1} x2:{self.bond.x2} y1:{self.bond.y1} y2:{self.bond.y1} z:{self.bond.z} len:{self.bond.len} dx:{self.bond.dx} dy:{self.bond.dy}"

    # Method to return a svg string representation of a bond
    def svg(self):
        # calculate bond coordinates
        atomOnex = (self.bond.x1 * 100) + offsetx
        atomOney = (self.bond.y1 * 100) + offsety
        atomTwox = (self.bond.x2 * 100) + offsetx
        atomTwoy = (self.bond.y2 * 100) + offsety
        
        # calculate bond coordinates
        x1Pos = atomOnex + self.bond.dy * 10
        x1Neg = atomOnex - self.bond.dy * 10
        x2Pos = atomTwox + self.bond.dy * 10
        x2Neg = atomTwox - self.bond.dy * 10

        y1Pos = atomOney + self.bond.dx * 10
        y1Neg = atomOney - self.bond.dx * 10
        y2Pos = atomTwoy + self.bond.dx * 10
        y2Neg = atomTwoy - self.bond.dx * 10

        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (x1Neg, y1Pos, x1Pos, y1Neg, x2Pos, y2Neg, x2Neg, y2Pos)

# Subclass for a molecule
class Molecule(molecule.molecule):
    # Method to return a string representation of a molecule
    def __str__(self):
        text = ""
        # get string representations of atoms
        for i in range(self.atom_no):
            atom = self.get_atom(i)
            temp = Atom(atom)
            text += temp.__str__()
            text += "\n"
        # get string representations of bonds
        for i in range(self.bond_no):
            bond = self.get_bond(i)
            temp = Bond(bond)
            text += temp.__str__()
            text += "\n"

        return text

    # Method to return a svg string representation of a molecule   
    def svg(self):
        # add header to string
        text = header
        i = 0
        j = 0
        # loop through atoms and bonds
        while(i != self.atom_no and j != self.bond_no):
            # get atom and bond
            tempAtom = self.get_atom(i)
            a1 = Atom(tempAtom)
            tempBond = self.get_bond(j)
            b1 = Bond(tempBond)
            # get smallest z value
            if(a1.z < b1.z):
                # save to string
                text += a1.svg()
                i += 1
            else:
                # save to string
                text += b1.svg()
                j += 1
        # end while        

        # loop through remaining bonds or atoms
        if(i == self.atom_no):
            for k in range(j, self.bond_no):
                # save to string
                tempBond = self.get_bond(k)
                b1 = Bond(tempBond)
                text += b1.svg()
        else:
            for m in range(i, self.atom_no):
                # save to string
                tempAtom = self.get_atom(m)
                a1 = Atom(tempAtom)
                text += a1.svg()
        # add footer to string
        text += footer
        return text

    # Method to parse a file and create a molecule
    def parse(self, fileObj):
        # get file contents
        text = fileObj.read()
        lineCount = 0
        # loop through lines in file
        for line in text.split("\n"):
            # add 1 to file count
            lineCount += 1
            # if string is at the bond and atom count line
            if(lineCount == 4):
                # split line by whitespace
                result = line.split()
                # save num of atom and bond
                atomCount = int(result[0])
                bondCount = int(result[1])
            # if string is at the atom info
            elif(lineCount > 4 and atomCount != 0):
                # split line by whitespace
                result = line.split()
                # append atom to molecule
                self.append_atom(result[3], float(result[0]), float(result[1]), float(result[2]))
                atomCount = atomCount -  1
            # if string is at the bond info
            elif(lineCount > 4 and atomCount == 0 and bondCount != 0):
                # split line by whitespace
                result = line.split()
                # append bond to molecule
                self.append_bond((int(result[0])) - 1, (int(result[1])) - 1, int(result[2]))
                bondCount = bondCount - 1
