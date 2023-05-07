import os
import sqlite3
import MolDisplay

#Class for a SQL Database
class Database:
    #Method to create and start a database
    def __init__( self, reset=False ):
        #if database needs to be reset
        if(reset == True):
            #check if it exists
            if (os.path.isfile('molecules.db')):
                #delete database
                os.remove('molecules.db')
        #create database
        self.conn = sqlite3.connect("molecules.db")

    #Method to create tables in database
    def create_tables( self ):
        #Create Elements Table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Elements
        (   ELEMENT_NO INTEGER NOT NULL,
            ELEMENT_CODE VARCHAR(3) PRIMARY KEY NOT NULL,
            ELEMENT_NAME VARCHAR(32) NOT NULL,
            COLOUR1 CHAR(6) NOT NULL,
            COLOUR2 CHAR(6) NOT NULL,
            COLOUR3 CHAR(6) NOT NULL,
            RADIUS DECIMAL(3) NOT NULL
        )""")
        #Create Atoms Table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Atoms(   
            ATOM_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,  
            ELEMENT_CODE VARCHAR(3) NOT NULL REFERENCES Elements(ELEMENT_CODE),
            X DECIMAL(7,4) NOT NULL,
            Y DECIMAL(7,4) NOT NULL,
            Z DECIMAL(7,4) NOT NULL
            )""")
        #Create Bonds Table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Bonds
        (   BOND_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,  
            A1 INTEGER NOT NULL,
            A2 INTEGER NOT NULL,
            EPAIRS INTEGER NOT NULL
        )""")
        #Create Molecules Table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Molecules
        (   MOLECULE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            NAME TEXT UNIQUE NOT NULL
        )""")
        #Create MoleculeAtom Table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeAtom
        (   MOLECULE_ID INTEGER NOT NULL,
            ATOM_ID INTEGER NOT NULL,
            PRIMARY KEY (MOLECULE_ID, ATOM_ID),
            FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
            FOREIGN KEY (ATOM_ID) REFERENCES Atoms
        )""")
        #Create MoleculeBond Table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeBond
        (   MOLECULE_ID INTEGER NOT NULL,
            BOND_ID INTEGER NOT NULL,
            PRIMARY KEY (MOLECULE_ID, BOND_ID),
            FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
            FOREIGN KEY (BOND_ID) REFERENCES Bonds
        )""")
    
    #Method to set Table values
    def __setitem__( self, table, values ):
        # If table is Elements table
        if table == "Elements":
            # store values
            self.conn.execute(f"""INSERT INTO ELEMENTS
                                VALUES ('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}', '{values[4]}', '{values[5]}', '{values[6]}')""")
            self.conn.commit()
        # If table is Atoms table
        if table == "Atoms":
            # store values
            self.conn.execute(f"""INSERT INTO Atoms 
                                VALUES ('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}', '{values[4]}'""")
            self.conn.commit()
        # If table is Bonds table
        if table == "Bonds":
            # store values
            self.conn.execute(f"""INSERT INTO Bonds 
                                VALUES ('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}'""")
            self.conn.commit()
        # If table is Molecules table
        if table == "Molecules":
            # store values
            self.conn.execute(f"""INSERT INTO Molecules 
                                VALUES ('{values[0]}', '{values[1]}')""")
            self.conn.commit()
        # If table is MoleculeAtom table
        if table == "MoleculeAtom":
            # store values
            self.conn.execute(f"""INSERT INTO MoleculeAtom VALUES
                                VALUES ('{values[0]}', '{values[1]}')""")
            self.conn.commit()
        # If table is MoleculeBond table
        if table == "MoleculeBond":
            # store values
            self.conn.execute(f"""INSERT INTO MoleculeBond VALUES
                                VALUES ('{values[0]}', "{values[1]}")""")
            self.conn.commit()

    # Method to add a atom
    def add_atom( self, molname, atom ):
        # Insert Atoms values
        self.conn.execute("""INSERT INTO Atoms VALUES 
                        (null, '%s', %f, %f, %f) """ %(atom.atom.element, atom.atom.x, atom.atom.y, atom.atom.z))
        # Commit the change
        self.conn.commit()

        # Get molecule and Atom Id
        moleculeID = self.conn.execute(f"""SELECT Molecules.MOLECULE_ID FROM Molecules WHERE Molecules.NAME = '{molname}'""")
        atomID = self.conn.execute("""SELECT * FROM Atoms WHERE ATOM_ID = (SELECT MAX(ATOM_ID) FROM Atoms)""")
        row= atomID
        atomID = row.fetchone()[0]
        molIndex = moleculeID
        moleculeID =  molIndex.fetchone()[0]

        # Insert ID's into Table
        self.conn.execute("""INSERT INTO MoleculeAtom VALUES (%d, %d) """ %(moleculeID, atomID))

        # Commit the change
        self.conn.commit()

    # Method to add a bond
    def add_bond( self, molname, bond ):
        # Insert Bond values
        self.conn.execute("""INSERT INTO Bonds VALUES 
                        (null, %f, %f, %f) """ %(bond.bond.a1, bond.bond.a2, bond.bond.epairs))
        # Commit the change
        self.conn.commit()

        # Get molecule and bond ID
        moleculeID = self.conn.execute(f"""SELECT Molecules.MOLECULE_ID FROM Molecules WHERE Molecules.NAME = '{molname}'""")
        bondID = self.conn.execute("""SELECT * FROM Bonds WHERE BOND_ID = (SELECT MAX(BOND_ID) FROM Bonds)""")
        row = bondID
        bondID = row.fetchone()[0]
        molIndex = moleculeID
        moleculeID =  molIndex.fetchone()[0]

        # Insert ID's into Table
        self.conn.execute("""INSERT INTO MoleculeBond VALUES (%d, %d) """ %(moleculeID, bondID))

        # Commit the change
        self.conn.commit()

    # Method to add a molecule
    def add_molecule( self, name, fp ):
        # create molecule object
        mol = MolDisplay.Molecule()
        mol.parse(fp)

        # Insert Molecule value into table
        self.conn.execute("""INSERT INTO Molecules VALUES (null, '%s')""" %(name))
        # Commit the change
        self.conn.commit()

        # loop through the bonds
        for i in range(mol.bond_no):
            # add bond
            self.add_bond(name, MolDisplay.Bond(mol.get_bond(i)))

        # loop through the atoms
        for i in range(mol.atom_no):
            # add atom
            self.add_atom(name, MolDisplay.Atom(mol.get_atom(i)))

    # Method to create a molecule
    def load_mol( self, name ):
        # create molecule object
        mol = MolDisplay.Molecule()
        
        # Get atoms
        cursor = self.conn.cursor()
        cursor.execute("""SELECT *
                            FROM Atoms, MoleculeAtom, Molecules
                            WHERE Atoms.ATOM_ID = MoleculeAtom.ATOM_ID AND Molecules.NAME = ? AND Molecules.MOLECULE_ID = MoleculeAtom.MOLECULE_ID
                            ORDER BY ATOM_ID ASC""", (name,))
        atomsArr = cursor.fetchall()

        # loop through atoms
        for atom in atomsArr:
            # add atoms to molecule
            mol.append_atom(atom[1], atom[2], atom[3], atom[4])

        # Get bonds
        cursor.execute("""SELECT *
                            FROM Bonds, MoleculeBond, Molecules
                            WHERE Bonds.BOND_ID = MoleculeBond.BOND_ID AND Molecules.NAME = ? AND Molecules.MOLECULE_ID = MoleculeBond.MOLECULE_ID
                            ORDER BY BOND_ID ASC""", (name,))
        bondsArr = cursor.fetchall()

        # loop through bonds
        for bond in bondsArr:
            # add bonds to molecule
            mol.append_bond(bond[1], bond[2], bond[3])

        # return molecule
        return mol

    # Method to create a dictionary
    def radius( self ):
        # Get ELEMENT_CODE and RADIUS values
        r = self.conn.execute("""SELECT ELEMENT_CODE, RADIUS FROM ELEMENTS""").fetchall()
        # create dictionary
        radiusDict = dict(r)
        # return dictionary
        return radiusDict

    # Method to create a dictionary
    def element_name( self ):
        # Get ELEMENT_CODE and ELEMENT_NAME values
        e = self.conn.execute("""SELECT ELEMENT_CODE, ELEMENT_NAME FROM ELEMENTS""").fetchall()
        # create dictionary
        elementDict = dict(e)
        # return dictionary
        return elementDict

    # Method to create svg's
    def radial_gradients( self ):
        # declare and initialize variable
        svg = ""

        # Get values from Elements Table
        cursor = self.conn.cursor()
        cursor.execute("SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements")
        elements = cursor.fetchall()

        # loop through elements
        for element in elements:
            # concatenate string with values
            svg = svg + """
<radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
  <stop offset="0%%" stop-color="#%s"/>
  <stop offset="50%%" stop-color="#%s"/>
  <stop offset="100%%" stop-color="#%s"/>
</radialGradient>""" % (element[0], element[1], element[2], element[3])
        
        # return string representation of svg
        return svg

    def getMolTableData(self):
        cursor = self.conn.cursor()
        # retrieve molecule name and its respective atom and bond count
        cursor.execute("""SELECT Molecules.MOLECULE_ID, Molecules.NAME, COUNT(DISTINCT Bonds.BOND_ID), COUNT(DISTINCT Atoms.ATOM_ID)
                    FROM Molecules
                    JOIN MoleculeBond ON Molecules.MOLECULE_ID = MoleculeBond.MOLECULE_ID
                    JOIN Bonds ON MoleculeBond.BOND_ID = Bonds.BOND_ID
                    JOIN MoleculeAtom ON Molecules.MOLECULE_ID = MoleculeAtom.MOLECULE_ID
                    JOIN Atoms ON MoleculeAtom.ATOM_ID = Atoms.ATOM_ID
                    GROUP BY Molecules.MOLECULE_ID""")
        table = cursor.fetchall()

        molData = []

        for mol in table:
            # create dictionary
            dict = {
                "name": mol[1],
                "bondNum": mol[2],
                "atomNum": mol[3]
            }
            # save dictionary in array
            molData.append(dict)

        return molData

        


