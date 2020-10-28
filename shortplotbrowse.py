##Up to date plotting directly from vamas files.
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import *
from tkinter import filedialog

root = Tk()
cdir = os.getcwd()
files = filedialog.askopenfilenames(initialdir = cdir, title = 'Select files to plot', filetypes = [('Vamas files', '*.vms')])
filesread = root.tk.splitlist(files)
filename= []
for i in filesread:
    filename.append(i.split('/')[-1])
    
# Change working directory to directory first chosen file is in.
os.chdir(filesread[0].replace(filename[0],'')) 

## If more than one filename is written then this if-statement is used.##

#filename = []
#for i in range(len(sys.argv)-1):
#    filename.append(sys.argv[i+1])

if filename[0].split('_')[3].split('-')[0] == 'XPS':
    import XPS as module
elif filename[0].split('_')[3].split('-')[0] == 'ISS':
    import ISS as module

    ## Creating empty arrays for appending information later.
sample = []
comment = []
region = []

    ##Loop that loads the data in from all the files. The module has already
    ## been set so if the files are not all XPS or all ISS, this will fail.
    ##

for index, k in enumerate(filename):

        ## Finds information on file k. Specifically the type of scan,
        ## regions, samples, comments and dates.
    fileinfo = k.split('_')
    type = fileinfo[3].split('-')[0]
    region.append(fileinfo[3].split('-')[2])
    sample.append(fileinfo[1].split('-')[1])
    comment.append(fileinfo[1].split('-')[0]+'-')
    date = fileinfo[0].split('-')[0]

        ##Load the data using either the XPS or ISS module for the
        ## specific file k.
    exp = module.Experiment(k)
        ##Create x,y arrays and append the data into them. Each scan enters as
        ## an array that is appended. X-axis depends on the type identified
        ## above.
    if index == 0:
        x, y = [], []
    if type.upper() == 'XPS':
        x.append(exp.BE[0][::-1])
        y.append(exp.cps[0][::-1])
        #y=[i+index*1000 for i in y]

    elif type.upper() == 'ISS':
        x.append(exp.energy[0])
        y.append(exp.cps[0])

    #Create figure and assign y-axis label.
fig = plt.figure(1)
plt.ylabel('Counts')

    ## Assign the appropriate label and scale to the x-axis.
if type.upper() == 'XPS':
    plt.xlabel('Binding Energy [eV]')
        #v=[-5, 1000, 0, np.amax(y)+200]
    plt.xlim(x[0][-1],x[0][0])
    plt.xticks(np.arange(round(x[0][0]/100)*100,x[0][-1], step = 100))
elif type.upper() == 'ISS':
    plt.xlabel('Kinetic Energy [eV]')
    #v=[x[0][0], x[0][-1], 0, np.amax(y)+100]
    plt.xticks(np.arange(round(x[0][0]/100)*100,x[0][-1], step = 100))
    #plt.axis(v)

    ## The plotting of all the scans in the loaded files.
for i in range(len(filename)):
    if type.upper() == 'XPS':
        yplot=[q+i*20000 for q in y[i]]
    elif type.upper() == 'ISS':
        yplot=[q+i*0 for q in y[i]]
        ysave = np.array(y[i])
        fname = 'plot'+str(i)+'.txt'
        #np.savetxt(fname,ysave)
    #np.savetxt('x.txt', x[i])
    plt.plot(x[i],yplot)



    #Fix comments and sample names for file and title.
samples = ''
samples2 = ''
comments = ''

for i in range(len(sample)):
    if sample[i] not in samples:
            ## for figure title.
        samples = (samples + sample[i]+ ' ')
        ## for saved file name.
        samples2 = (samples2 + sample[i])

for i in range(len(comment)):
    comments += comment[i] + ' '
    ## Create figure title and save figure to file.
plt.title(samples+ 'Scans: '+comments)
commentslist = comments.split('-')
plt.legend(commentslist)
plt.savefig(type + samples2 +'.png',dpi = 600)

plt.show()
#print(x)
