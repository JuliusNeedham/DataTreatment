##A toolbox for plotting from VAMAS files. Works with ISS and XPS data.
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import *
from tkinter import filedialog

#Determine whether data is XPS or ISS and passes the appropriate loaded module and an indicative marker. This is used in other functions throughout the code.
def xps_or_iss(): 
    if filename[0].split('_')[3].split('-')[0] == 'XPS':
        import XPS as module
        marker = 0 
    elif filename[0].split('_')[3].split('-')[0] == 'ISS':
        import ISS as module
        marker = 1
    return module, marker
    
#Load data with a file prompt, change the working directory to it, and return the filename
def loaddata():
    root = Tk()
    cdir = os.getcwd()
    files = filedialog.askopenfilenames(initialdir = cdir, title = 'Select files to plot', filetypes = [('Vamas files', '*.vms')])
    filesread = root.tk.splitlist(files)
    filename= []
    root.destroy()
    for i in filesread:
        filename.append(i.split('/')[-1])

    # Change working directory to directory first chosen file is in.
    os.chdir(filesread[0].replace(filename[0],'')) 
    return filename

# Plotting function        
def plottingtool():
    module = xps_or_iss()[0]
    marker = xps_or_iss()[1]

    # Creating empty arrays for appending information later.
    sample = []
    comment = []
    region = []
    date = []
    current_regions= []
    
    # Loop that loads the data in from all the files. The module has already
    # been set so if the files are not all XPS or all ISS, this will fail.
    for index, k in enumerate(filename):
        # Information on file k. Specifically the type of scan,
        # regions, samples, comments and dates.
        fileinfo = k.split('_')
        type = fileinfo[3].split('-')[0]
        region.append(fileinfo[3].split('-')[2])
        current_region = int(region[index])-1
        current_regions.append(current_region)

        sample.append(fileinfo[1].split('-')[1])
        comment.append(fileinfo[1].split('-')[0])
        date.append(fileinfo[0].split('-')[0])    
        
        #Allow plotting of other than first scan - region not 1 (files with index 1)
        region_not_1 = False
        if not region[index] == '1': 
            k = fileinfo[0] + '_' + fileinfo[1] + '_' + fileinfo[2] + '_' + type + '-' + '-' + '1' + '_' + fileinfo[4] + '_' + fileinfo[5]
            region_not_1 = True
            
        # Load the data using either the XPS or ISS module for the
        # specific file k.
        exp = module.Experiment(k)
        
        # Create x,y arrays and append the data into them. Each scan enters as
        # an array that is appended. X-axis depends on the type identified
        # above.
        if index == 0:
            x, y = [], []
        if marker == 0: #xps
            x.append(exp.BE[current_region][::-1])
            y.append(exp.cps[current_region][::-1])
        elif marker == 1: #iss
            x.append(exp.energy[current_region])
            y.append(exp.cps[current_region])  
            
    # Create figure and assign y-axis label.
    fig = plt.figure(1)
    plt.ylabel('Counts')

    # Assign the appropriate label depending on data type and scale to the x-axis.
    if marker == 0: #xps
        plt.xlabel('Binding Energy [eV]')
        plt.xlim(x[0][-1],x[0][0])
        plt.xticks(np.arange(round(x[0][0]/100)*100,x[0][-1], step = 100))
    elif marker== 1: #iss
        plt.xlabel('Kinetic Energy [eV]')
        plt.xticks(np.arange(round(x[0][0]/100)*100,x[0][-1], step = 100))

    # The plotting of all the scans in the loaded files.
    for i in range(len(filename)):
        if type.upper() == 'XPS':
            yplot=[q+i*20000 for q in y[i]]
        elif type.upper() == 'ISS':
            yplot=[q+i*0 for q in y[i]]
            ysave = np.array(y[i])
            fname = 'plot'+str(i)+'.txt'
        plt.plot(x[i],yplot)



    # Create arrays for plot naming.
    # Comments are seperated by + and dates are seperated by + and are reformatted to yyyy-mm-dd format
    # (easier to sort in file explorer than dd-mm-yyyy)
    comments = ''
    dates = ''

    for i in range(len(comment)):
        comments += comment[i] + '+'
    comments = comments.rstrip('+')
    for i in range(len(date)):
            dates += date[i][:4] + '-' + date[i][4:6] + '-' + date[i][6:8] + '+'
    dates = dates.strip('+')        
      
    # Create figure with legend and title, which changes depending on amount of data chosen.
    if comment.count(comment[0]) == len(comment): #If all comments are same, set legend to sample and title to comment
        plt.legend(sample)
        plt.title(comment[0])
    else:
        plt.legend(comments.split('+'))
        plt.title(sample)
        
    #Change title depending on single plot or multiplot. Mostly for use during saving.    
    if len(comment)==1:
        fig.canvas.set_window_title(dates[0] + '_' + comment[0] + '_' + sample[0] + '_' + type + '_' + region[0])
    elif len(comment)>1:    
        fig.canvas.set_window_title('Multiplot_' + dates + '_' + comments + '_' + type)
    
    #Show the plot
    plt.show()

#Saving data as .txt (with Origin compatible header)
def savingtool():
    for i in range(len(filename)):
        #Remove any subfolder designation from file name.
        filename[i] = filename[i].lstrip('\b')
        
        #Check whether files are XPS or ISS, and loads appropriate module, sets marker and prints detected type.
        module = xps_or_iss()[0]
        marker = xps_or_iss()[1]
        #print('Detected type: ' + filename.split('_')[3].split('-')[0])
        
        #Import VAMAS and save as .txt with header in same folder.
        exp = module.Experiment(filename[i])
        for number in exp.cps.keys():
            #print('Writing region {}'.format(number))
            new_filename = filename[i].split('--')[0] + '_Region_{}.txt'.format(number+1)
            f = open(new_filename, 'w')
            f.writelines(['Energy,Counts/s\neV,A.U.\n'])
            if marker == 0: # xps
                x = exp.BE[number]
            elif marker == 1: # iss
                x = exp.energy[number]
            y = exp.cps[number]
            for j in range(len(y)):
                line = '{},{}\n'.format(x[j], y[j])
                f.write(line)
            print('File saved as: {}'.format(new_filename))
            f.close()


# ------------------------------------------------------------------------------------
# Actual script begins here
# ------------------------------------------------------------------------------------

#When script first runs, data is loaded and plotted
filename = loaddata()
plottingtool()

#Simple menu
ans=True
while ans:
    print("""
    -------------------------------
    Welcome to the XPS/ISS toolbox!
    -------------------------------
    
    Options:
    -------------------------------
    1. Load other data
    2. Plot data
    3. Save data as .txt
    4. Quit
    -------------------------------
    """)
    ans=input("Choose an option: ")
    if ans=="1":
      filename = loaddata() #overwrites current filename and changes working directory
    elif ans=="2":
      plottingtool() 
    elif ans=="3":
      savingtool()
    elif ans=="4":
      ans = None #Quits the script
    else:
       print("\n Not a valid choice, try again")

