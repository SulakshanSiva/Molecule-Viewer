#include "mol.h"

/*
atomset: Sets the values of an atom struct using the passed in arguments
In: atom *atom, char element[3], double *x, double *y, double *z
Out: N/A
Post: Sets the values of a atom struct
*/
void atomset(atom *atom, char element[3], double *x, double *y, double *z){
    //copy values to struct atom
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
    strcpy(atom->element, element);
}//end atomset method

/*
atomget: Gets the values of an atom struct
In: atom *atom, char element[3], double *x, double *y, double *z
Out: N/A
Post: Gets the values of an atom struct and stores them in variables
*/
void atomget(atom *atom, char element[3], double *x, double *y, double *z){
    //save atom values to variables x,y,z
    *x = atom->x;
    *y = atom->y;
    *z = atom->z; 
    strcpy(element, atom->element);
}//end atomget method

/*
compute_coords: Calculates the z, x1, y1, x2, y2, len, dx, and dy values of the bond and sets them
In: bond *bond
Out: N/A
Post: Sets the z, x1, y1, x2, y2, len, dx, and dy values of the bond
*/
void compute_coords(bond *bond){
   //save x and y
    bond->x1 = bond->atoms[bond->a1].x;
    bond->y1 = bond->atoms[bond->a1].y;
    //save x and y
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y2 = bond->atoms[bond->a2].y;
    //calculate z
    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2;
    //calculate len
    double xTotal = bond->atoms[bond->a2].x - bond->atoms[bond->a1].x; 
    double yTotal = bond->atoms[bond->a2].y - bond->atoms[bond->a1].y;
    xTotal *= xTotal;
    yTotal *= yTotal;
    bond->len = sqrt(xTotal + yTotal);
    //calculate dx and dy
    bond->dx = (bond->atoms[bond->a2].x - bond->atoms[bond->a1].x) / bond->len;
    bond->dy = (bond->atoms[bond->a2].y - bond->atoms[bond->a1].y) / bond->len;
}//end computer_coords method

/*
bondset: Sets the values of a bond struct using the passed in arguments
In: bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs 
Out: N/A
Post: Sets the values of a bond struct
*/
void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs){
    //copy values to bond struct
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->epairs = *epairs;
    bond->atoms = *atoms;   
	compute_coords(bond);
}//end bondset method

/*
bondget: Gets the values of a bond struct
In: bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs
Out: N/A
Post: Gets the values of a bond struct and stores them in variables
*/
void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs){
    //save bond values to variables
    *a1 = bond->a1;
    *a2 = bond->a2;
    *epairs = bond->epairs;
    *atoms = bond->atoms;
}//end bondget method

/*
molmalloc: Creates a malloced area of memory that is large enough to hold a molecule, set struct data values and mallocs enough memory for their arrays
In: unsigned short atom_max, unsigned short bond_max
Out: molecule
Post: Returns a malloced area of memory, large enough to hold a molecule
*/
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max){
    //malloc space for one molecule
    molecule * moleculeTemp = malloc(sizeof(molecule) * 1);
    if(moleculeTemp == NULL){
        return NULL;
    }
    //set atom data
    moleculeTemp->atom_max = atom_max;
    moleculeTemp->atom_no = 0;
    //allocate memory to the atoms array
    moleculeTemp->atoms = malloc(sizeof( struct atom) * moleculeTemp->atom_max);
    moleculeTemp->atom_ptrs = malloc(sizeof(struct atom*) * moleculeTemp->atom_max);
    //check if malloc was successful
    if(moleculeTemp->atoms == NULL){
        return NULL;
    }
    if(moleculeTemp->atom_ptrs == NULL){
        return NULL;
    }
    //set bond data
    moleculeTemp->bond_max = bond_max;
    moleculeTemp->bond_no = 0;
    //allocate memory to the bonds array
    moleculeTemp->bonds =  malloc(sizeof(struct bond) *  moleculeTemp->bond_max);
    moleculeTemp->bond_ptrs = malloc(sizeof(struct bond*) *  moleculeTemp->bond_max);
    //check if malloc was successful
    if(moleculeTemp->bonds == NULL){
        return NULL;
    }
    if(moleculeTemp->bond_ptrs == NULL){
        return NULL;
    }
    //return address of molecule
    return moleculeTemp;
    
}//end molmalloc method

/*
molcopy: Creates a copy of a passed in molecule
In: molecule *src
Out: molecule *
Post: Returns the address of a malloced area of memory, large enough to hold a molecule
*/
molecule *molcopy(molecule *src){
    //malloc memory for copy of molecule
    molecule * newMol = molmalloc(src->atom_max, src->bond_max);
    if(newMol == NULL){
        return NULL;
    }
    //loop through number of atoms
    for(int i = 0; i < src->atom_no; i++){
         //set atom in array
        atomset(&newMol->atoms[i], src->atoms[i].element, &src->atoms[i].x, &src->atoms[i].y, &src->atoms[i].z);
        //append atom to molecule
        molappend_atom(newMol, &src->atoms[i]);
    }
    //loop through number of bonds
    for(int j = 0; j < src->bond_no; j++){
        //set bonds in array
        bondset(&newMol->bonds[j], &src->bonds[j].a1, &src->bonds[j].a1, &src->bonds[j].atoms, &src->bonds[j].epairs);
        //append bond in array
        molappend_bond(newMol, &src->bonds[j]);
    }
    //set copied molecule values
    newMol->atom_no = src->atom_no;
    newMol->bond_no = src->bond_no;
    return newMol;
}//end molcopy method

/*
molfree: Free all memory associated with the molecule
In: molecule *ptr
Out: N/A
Post: Frees malloced memory
*/
void molfree(molecule *ptr){
    //free memory allocated by struct molecule
    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);
    //free molecule
    free(ptr);
}// end molFree method

/*
molappend_atom: Adds an atom to the molecule
In: molecule *molecule, atom *atom
Out: N/A
Post: Saves an atom to the molecule atoms arrays, reallocates memory if needed
*/
void molappend_atom(molecule *molecule, atom *atom){
    //check if array is at full capacity
    if(molecule->atom_no >= molecule->atom_max){
        //update atom max value
        if(molecule->atom_max == 0){
            molecule->atom_max = molecule->atom_max + 1;
        } else {
            molecule->atom_max = molecule->atom_max * 2;
        }
        //reallocate memory
        molecule->atoms = (struct atom*)realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max );
        molecule->atom_ptrs = (struct atom**)realloc(molecule->atom_ptrs, sizeof(struct atom*) * molecule->atom_max);
        if(molecule->atoms == NULL){
            printf("Error. Exiting Program.\n");
            exit(0);
        }
        if(molecule->atom_ptrs == NULL){
            printf("Error. Exiting Program.\n");
            exit(0);
        }
        for(int i = 0; i < molecule->atom_no; i++){
            molecule->atom_ptrs[i] = &(molecule->atoms[i]);
        }
    }
    //add atom to molecule 
    molecule->atoms[molecule->atom_no] = *atom;
    molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];
    //increment atom count
    molecule->atom_no = molecule->atom_no + 1;
}//end molappend_atom method

/*
molappend_bond: Adds a bond to the molecule
In: molecule *molecule, bond *bond
Out: N/A
Post: Saves a bond to the molecule bond arrays, reallocates memory if needed
*/
void molappend_bond(molecule *molecule, bond *bond){
    //check if array is at full capacity
    if(molecule->bond_no >= molecule->bond_max){
        //update bond max
        if(molecule->bond_max == 0){
            molecule->bond_max = molecule->bond_max + 1;
        } else {
            molecule->bond_max = molecule->bond_max * 2;
        }
        //reallocate memory
        molecule->bonds = (struct bond *)realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);
        molecule->bond_ptrs = (struct bond **)realloc(molecule->bond_ptrs, sizeof(struct bond*) * molecule->bond_max);
        if(molecule->bonds == NULL){
            printf("Error. Exiting Program.\n");
            exit(0);
        }
        if(molecule->bond_ptrs == NULL){
            printf("Error. Exiting Program.\n");
            exit(0);
        }
        for(int i = 0; i < molecule->bond_no; i++){
            molecule->bond_ptrs[i] = &(molecule->bonds[i]);
        }
    }
    //add bond to molecule 
    molecule->bonds[molecule->bond_no] = *bond;
    molecule->bond_ptrs[molecule->bond_no] = &(molecule->bonds[molecule->bond_no]);
    //increment bond count
    molecule->bond_no = molecule->bond_no + 1;
}//end molappend_bond method

/*
compareAtom: Comparator to find the bigger value, helper function for q sort
In: const void * a, const void * b
Out: int
Post: Returns an int for qsort to read and use to sort values
*/
int compareAtom (const void * a, const void * b){
  struct atom * const * atom1 = a;
  struct atom * const * atom2 = b;

  if ((*atom1)->z == (*atom2)->z){
    return 0;
  } else if((*atom1)->z > (*atom2)->z){
    return 1;
  } else {
    return -1;
  }

}//end compareAtom method

/*
bond_comp: Comparator to find the bigger value, helper function for q sort
In: const void *a, const void *b
Out: int
Post: Returns an int for qsort to read and use to sort values
*/
int bond_comp(const void *a, const void *b){
    struct bond * const * bond1 = a;
    struct bond * const * bond2 = b;

    if((*bond1)->z == (*bond2)->z){
        return 0;
    } else if((*bond1)->z > (*bond2)->z){
        return 1;
    } else {
        return -1;
    }

}//end bond_comp method

/*
molsort: Sorts the bondbond_ptrs and atom_ptrs array of a molecule in ascending order of z values
In: molecule *molecule
Out: N/A
Post: Sorts both the bond_ptrs array and atom_ptrs array of a molecule
*/
void molsort(molecule *molecule){
    //sort arrays
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom*), compareAtom);
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond*), bond_comp);
    
}//end molsort method

/*
xrotation: Rotates matrix by deg degrees around the x-axis
In: xform_matrix xform_matrix, unsigned short deg
Out: N/A
Post: Rotates the matrix by deg degrees around the x-axis
*/

void xrotation(xform_matrix xform_matrix, unsigned short deg) {
	double rad = deg * M_PI / 180; 
    // create matrix
	xform_matrix[0][0] = 1.00;
	xform_matrix[0][1] = 0.00;
	xform_matrix[0][2] = 0.00;
	xform_matrix[1][0] = 0.00;
	xform_matrix[1][1] = cos(rad);
	xform_matrix[1][2] = sin(rad) * -1.00;
	xform_matrix[2][0] = 0.00;
	xform_matrix[2][1] = sin(rad);
	xform_matrix[2][2] = cos(rad);
}//end xrotation method

/*
yrotation: Rotates matrix by deg degrees around the y-axis
In: xform_matrix xform_matrix, unsigned short deg
Out: N/A
Post: Rotates the matrix by deg degrees around the y-axis
*/
void yrotation(xform_matrix xform_matrix, unsigned short deg) {
	double rad = deg * M_PI / 180; 

    // create matrix
	xform_matrix[0][0] = cos(rad);
	xform_matrix[0][1] = 0.00;
	xform_matrix[0][2] = sin(rad);
	xform_matrix[1][0] = 0.00;
	xform_matrix[1][1] = 1.00;
	xform_matrix[1][2] = 0.00;
	xform_matrix[2][0] = sin(rad) * -1.00;
	xform_matrix[2][1] = 0.00;
	xform_matrix[2][2] = cos(rad);
}//end yrotation method

/* 
zrotation: Rotates matrix by deg degrees around the z-axis
In: xform_matrix xform_matrix, unsigned short deg
Out: N/A
Post: Rotates the matrix by deg degrees around the z-axis
*/
void zrotation(xform_matrix xform_matrix, unsigned short deg) {
	double rad = deg * M_PI / 180; 
    // create matrix
	xform_matrix[0][0] = cos(rad);
	xform_matrix[0][1] = sin(rad) * -1.00;
	xform_matrix[0][2] = 0.00;
	xform_matrix[1][0] = sin(rad);
	xform_matrix[1][1] = cos(rad);
	xform_matrix[1][2] = 0.00;
	xform_matrix[2][0] = 0.00;
	xform_matrix[2][1] = 0.00;
	xform_matrix[2][2] = 1.00;
}//end zrotation method

/*
mol_xform: Applies the transformation matrix to all the atoms of the molecule through a vector matrix multiplication
In: molecule *molecule, xform_matrix matrix
Out: N/A
Post: Applies the transformation matrix to all the atoms of the molecule through a vector matrix multiplication
*/
void mol_xform(molecule* molecule, xform_matrix matrix) {
    //loop through atom array
	for (int i = 0; i < molecule->atom_no; i++) {
		double x = molecule->atoms[i].x; 
		double y = molecule->atoms[i].y; 
		double z = molecule->atoms[i].z; 

        //perform vector matrix multiplication
		for (int j = 0; j < 3; j++) {
			switch (j) {
			case 0:
				molecule->atoms[i].x = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z; //Calculate new x value
				break;
			case 1:
				molecule->atoms[i].y = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z; //Calculate new y value
				break;
			case 2:
				molecule->atoms[i].z = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z; //Calculate new z value
				break;
			}
		}//end inner for
	}//end outer for

    //calculate bond values
	for (int i = 0; i < molecule->bond_no; i++) {
		compute_coords(&molecule->bonds[i]);
	}//end for
}//end mol_xform

