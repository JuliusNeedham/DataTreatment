"""
Created on Fri Oct 30 10:42:56 2020
authors: rikplo & jlune

"""

# Import relevant packages
import numpy as np 
import os
import matplotlib.pyplot as plt 
import math
import datetime

def diameter2mass():
    # Calculate mass in amu from nanoparticle diameter
    
    ######################################################## ENTER VALUES
    # Input variables - information about the metal and nanoparticles
    
    # bulk density of the metal
    known_materials = ['Pt', 'Cu']
    known_densitites = [21.45, 8.96]
    material = input('Currently known materials: {}\nEnter material: '.format(', '.join(known_materials))) #ask user for material input

    if str.capitalize(material) in known_materials:
        ind = known_materials.index(material.capitalize())
        density = known_densitites[ind]
    else:
        density = float(input('Material not found. Enter density (in g/cm^3): '))
    
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
    
    print('\nThe mass of a {} nanoparticle of size {} nm is {} amu'.format(material.capitalize(), diameter, int(round(Mass_amu))))

def mass2diameter():
    # Calculate diameter in nm from nanoparticle mass in amu
    
    ######################################################## ENTER VALUES
    # Input variables - information about the metal and nanoparticles
    
    # bulk density of the metal
    known_materials = ['Pt', 'Cu']
    known_densitites = [21.45, 8.96]
    material = input('Currently known materials: {}\nEnter material: '.format(', '.join(known_materials))) #ask user for material input

    if str.capitalize(material) in known_materials:
        ind = known_materials.index(material.capitalize())
        density = known_densitites[ind]
    else:
        density = float(input('Material not found. Enter density (in g/cm^3): '))
    
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
    
    print('\nThe diameter of a {} nanoparticle of mass {:.0f} amu is {:.2f} nm'.format(material.capitalize(), mass, d))


def coverage_time():
    # Calculate time to get desired projected coverage on sample
    # Case 1: Area deposited is greater than the area of the sample 
    
    ######################################################## ENTER VALUES
    r = (float(input('Nanoparticle diameter (in nm): ')))/2
    
    d_eff = float(input('Effective deposition diameter (in mm): '))
    Acover = (((d_eff/2)*10**(-3))**2)*math.pi # Total area covered by beam (including sample + mask and raster pattern effect).
                                     # This number must be determined experimentally. Aka "raster area".    
    d_real = float(input('Sample diameter (in mm): '))    
    Asample = (((d_real/2)*10**(-3))**2)*math.pi # Area of sample (smaller than Acover)
    
    Goal_coverage= float(input('Goal coverage (in %): '))/100 # goal coverage - in %
    Current = float(input('Current (in pA): '))*10**(-12) # current measured in nA. 
    
    ########################################################  CALCULATE
    
    Rf = Asample/Acover # fraction of charge on sample (vs total charge on sample + surrounding plate). Aka "sample to spot ratio".
    
    Adep = (Goal_coverage*Asample)/Rf  # Coverage = (Adep*Rf)/Asample, 
                                        # Adep = total area of the deposited NANOPARTICLES (including sample + mask)
    N = Adep/(math.pi*(r*10**(-9))**2) # Adep = N*r**2*math.pi    ==> Get number of particles deposited, N
                           
    e = 1.602*10**(-19)
    charges = Current/e # charges/s = NPs/s (Assume each nanoparticle has one elementary charge)
    
    time = N/charges 
    time_formatted = datetime.timedelta(seconds=round(time))
    
    print('Deposition time: {}'.format(str(time_formatted)))

#simple menu    
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
       print("\n Not a valid choice, try again")
