import sys
import numpy
import glob
import os
from tkinter import *
from tkinter import filedialog

"""
Convert VAMAS files to TXT files (Origin compatible header). 
Prompts user to pick a directory, and searches subdirectories and converts all found files. 
Auto-detects ISS or XPS data, and saves it appropriately.
Some useful print commands have been commented out.
"""

#Ask for input folder and chdir to it.
root = Tk()
cdir = os.getcwd()
files = filedialog.askdirectory(initialdir = cdir)
os.chdir(files)


for filename in glob.glob('**/*.vms',recursive=True):
    #Remove any subfolder disignation from file name.
    filename = filename.lstrip('\b')
    
    #Check whether files are XPS or ISS, and loads appropriate module, sets marker and prints detected type.
    if filename.split('_')[3].split('-')[0] == 'XPS':
        import XPS as module
        marker = 0
    elif filename.split('_')[3].split('-')[0] == 'ISS':
        import ISS as module
        marker = 1
    #print('Detected type: ' + filename.split('_')[3].split('-')[0])
    
    #Import VAMAS and save as .txt with header in same folder.
    exp = module.Experiment(filename)
    for number in exp.cps.keys():
        #print('Writing region {}'.format(number))
        new_filename = filename.split('--')[0] + '_Region_{}.txt'.format(number)
        f = open(new_filename, 'w+')
        f.writelines(['Energy,Counts/s\neV,A.U.\n'])
        if marker == 0: # xps
            x = exp.BE[number]
        elif marker == 1: # iss
            x = exp.energy[number]
        y = exp.cps[number]
        for i in range(len(y)):
            line = '{},{}\n'.format(x[i], y[i])
            f.write(line)
        f.close()
print('\nDone!')
