"""
Created on Fri Oct 30 10:42:56 2020
authors: rikplo & jlune

"""

""" Import relevant packages """
import numpy as np 
import os
import matplotlib.pyplot as plt 
import math
import datetime

""" Pre-defined values """
#Known materials and densities
known_materials = ['1','2'], \
                  ['Pt', 'Cu'], \
                  [21.45, 8.96]
# L1: number, L2: material names L3: densities

#Create string for printing of known materials
print_materials = ''
for i in range(len(known_materials[1])):
    print_materials += known_materials[0][i] + '. ' + known_materials[1][i] + '\t'


# Known patterns, effective diameters anr raster cycle time.
# L1: pattern disignations, L2: pattern names L3: d_eff for patterns L4: raster cycle time
pattern_table = ['1','2','3'], \
                ['5x5_stub','1x1_stub','local_TPD'], \
                [6.462,0.000,7.004], \
                [360.2,0,448.2]       

# Create string for printing
print_patterns = ''
for i in range(len(pattern_table[1])):
    print_patterns += pattern_table[0][i] + '. ' + pattern_table[1][i] + '\t'

""" Calculate mass from nanoparticle diameter """
def diameter2mass():  
    ######################################################## ENTER VALUES
    # Input variables - information about the metal and nanoparticles

    #Loop for material choice
    material_choice=True
    while material_choice:
        print('---------------------------------------------')
        print('Currently known materials:')
        print('0. Enter manually')
        print(print_materials) 
        print('---------------------------------------------')
        material_choice=input("Choose a material: ")
        if material_choice in known_materials[0]:
            density = known_materials[2][int(material_choice)-1]
            break
        elif material_choice == '0':
            material_choice= float(input('Input material bulk density (in g/cm^3): '))
            break
        else:
           print("\n Not a valid choice, input a valid number")

    # desired particle size (diameter)
    try:
        diameter = float(input('Desired nanoparticle diameter (in nm): '))
    except ValueError:
        diameter = float(input('Invalid value. Enter number: '))

    ######################################################## CALCULATE
    D = (density/1000)*(10**6) # density in kg/m3
    r = diameter/2 # nm
    V = ((4/3)*math.pi)*(r*10**(-9))**3 # m^3
    mass = D*V # kg
    amukg = 1.6603145*10**(-27) #kg
    Mass_amu = mass/amukg
    
    print('\nThe mass of a {} nanoparticle of size {} nm is {} amu'.format(known_materials[1][int(material_choice)-1], diameter, int(round(Mass_amu))))

""" Calculate diameter in nm from nanoparticle mass in amu"""
def mass2diameter():

    
    ######################################################## ENTER VALUES
    # Input variables - information about the metal and nanoparticles
    
    #Loop for material choice
    material_choice=True
    while material_choice:
        print('---------------------------------------------')
        print('Currently known materials:')
        print('0. Enter manually')
        print(print_materials) 
        print('---------------------------------------------')
        material_choice=input("Choose a material: ")
        if material_choice in known_materials[0]:
            density = known_materials[2][int(material_choice)-1]
            break
        elif material_choice == '0':
            material_choice= float(input('Input material bulk density (in g/cm^3): '))
            break
        else:
           print("\n Not a valid choice, input a valid number")
    
    # desired particle mass
    try:
        mass = float(input('Desired nanoparticle mass (in amu): '))
    except ValueError:
        mass = float(input('Invalid value. Enter number: '))
        
    ######################################################## CALCULATE
    D = (density/1000)*(10**6) # density in kg/m3
    amukg = 1.6603145*10**(-27) #kg
    Mass_kg = mass*amukg
    d = (((6*Mass_kg/math.pi)**(1/3))/D**(1/3))*10**(9)# nm
    
    print('\nThe diameter of a {} nanoparticle of mass {:.0f} amu is {:.2f} nm'.format(known_materials[1][int(material_choice)-1], mass, d))

"""Calculate time to get desired projected coverage on sample"""
def coverage_time():
    #Choose mode for calculation
    mode_choice=True
    while mode_choice:
        print("""
----------------------------------------------------------------
1. Sample area is larger than deposition area (A_sample > A_dep)
2. Deposition area is larger than sample area (A_sample < A_dep)
----------------------------------------------------------------
        """)
        mode_choice = input('Choose a mode: ')
        if mode_choice == '1':
            case = 1
            break
        elif mode_choice == '2':
            case = 2
            break
        else:
            print('\nNot a valid choice, enter a valid number')
            
    ######################################################## ENTER VALUES      
    
    # Loop for choosing pattern
    pattern_choice=True
    raster_cycle=None
    while pattern_choice:
        print("""
--------------------------------------------
Currently known raster patterns:
0. Enter manually""")
        print(print_patterns)
        print('---------------------------------------------')
        pattern_choice=input("Choose a raster pattern: ")
        if pattern_choice in pattern_table[0]:
            d_eff = pattern_table[2][int(pattern_choice)-1]
            raster_cycle = pattern_table[3][int(pattern_choice)-1]
            break
        elif pattern_choice == '0':
            d_eff = float(input('Effective diameter (in mm): '))
            break
        else:
           print("\nNot a valid choice, enter a valid number")
    
    #ask for inputs about sample etc.
    if case == 2:
        d_real = float(input('Sample diameter (in mm): '))   
    elif case == 1:
        d_aperture = float(input('Aperture diameter (in mm): '))
        
    d_np = (float(input('Nanoparticle diameter (in nm): ')))
    Goal_coverage= float(input('Goal coverage (in %): '))/100 # goal coverage - in %
    Current = float(input('Current (in pA): '))*10**(-12) # current measured in pA   
    
    ########################################################  CALCULATE
    # Total area covered by beam (including sample + mask and raster pattern effect).
    # This number must be determined experimentally. Aka "raster area".   
    Acover = (((d_eff/2)*10**(-3))**2)*math.pi           
    
    # Asample: Area of sample (only if A_dep smaller than A_sample) 
    # Rf: fraction of charge on sample (vs total charge on sample + surrounding plate). Aka "sample to spot ratio"
    # Adep = total area of the deposited NANOPARTICLES (including sample + mask)  
    # Coverage = (Adep*Rf)/Asample for case 2
    if case == 2:
        Asample = (((d_real/2)*10**(-3))**2)*math.pi 
        Rf = Asample/Acover
        Adep = (Goal_coverage*Asample)/Rf # Adep = N*r**2*math.pi 
    elif case == 1:
        Aaperture = (((d_aperture/2)*10**(-3))**2)*math.pi 
        Adep = (Goal_coverage*Aaperture)

    #==> Get number of particles deposited, N
    Anp = (((d_np/2)*10**(-9))**2)*math.pi
    N = Adep/Anp      
    
    e = 1.602*10**(-19) # Electron charge in C
    charges = Current/e # charges/s = NPs/s (Assume each nanoparticle has one elementary charge)
    
    #Calculate and format time
    time = N/charges 
    time_formatted = datetime.timedelta(seconds=round(time))
    
    #Print output
    print('---------------------------------------------')
    print('Deposition time: {}'.format(str(time_formatted)))
    if raster_cycle is not None:
        print('Corresponding to {:.2f} raster cycles'.format(raster_cycle))

"""Main menu""" 
ans=True
while ans:
    print("""
----------------------------------------------------------
--------- Welcome to the pre-deposition toolbox! ---------
----------------------------------------------------------
    
Options:
----------------------------------------------------------
1. Diameter to mass converter
2. Mass to diameter converter
3. Estimate deposition time
4. Quit
----------------------------------------------------------
    """)
    ans=input("Choose an option: ")
    if ans=="1":
      diameter2mass()
    elif ans=="2":
      mass2diameter()
    elif ans=="3":
      coverage_time()
    elif ans=="4":
      ans = None
    else:
       print("\n Not a valid choice, input a valid number")
