from stat import S_ISREG, ST_CTIME, ST_MODE, ST_MTIME
import os, sys, time, re
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
  
def plotLine(name, xData, yData, color, symbol, line='-', doPoints=True):
    if len(xData)!=len(yData):
        print("Len x and y do not match: %d vs %d" %(len(xData), len(yData)));
    #Sort data
    xData, yData = zip(*sorted(zip(xData, yData)))
    #Array of sampling vals for polyfit line
    xp = np.linspace(xData[0], xData[-1]*0.98, 100)
    #polyfit
    #default_z = np.polyfit(xData, yData, 6)
    #default_fit = np.poly1d(default_z)
    # plt.plot(
        # xp, 
        # default_fit(xp), 
        # str(color)+str(line),
        # label=str(name),
        # lw=1
    # );
    #points
    if(doPoints):
        default_h = plt.plot(
           xData,yData, 
           str(symbol),
           label=str(name),
           lw=1,
           color=color
        );
        
def loadCSV(path):
    return np.loadtxt(
         path,
         dtype=[('Radius','float'), ('Bin Width','float'), ('Radial Neighbours','int'), ('Agent Count','int'), ('Env Width','int'), ('PBM(ms)','float'), ('Kernel(ms)','float'), ('fails','int')],
         skiprows=1,
         delimiter=',',
         usecols=(0,1,2,3,4,5,6,7),
         unpack=True
     );
###        
### Locate the most recent file in the directory That begins collated
###
#pattern = re.compile("\[2D\][0-9]+.csv$");
# get all entries in the directory w/ stats
#entries = (os.path.join('.', fn) for fn in os.listdir('.'))
#entries = ((os.stat(path), path) for path in entries)

# leave only regular files, insert creation date
#entries = ((stat[ST_MTIME], path)
#           for stat, path in entries if (S_ISREG(stat[ST_MODE]) and bool (pattern.search(path))))
#NOTE: on Windows `ST_CTIME` is a creation date 
#  but on Unix it could be something else
#NOTE: use `ST_MTIME` to sort by a modification date

#cdate, path = sorted(entries)[-1]

###
### Config, labelling
###
models = ['Default', 'Strips'];
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', '#dc5939', '#e8b2d8' ,'#684204' ,'#d9ffa0' ,'#a293bf'];
symbols = ['*', 'o', '^', 'x', 's', '+', 'h','p'];
lines = ['-','--',':', '-.']
plt.rc('font', family='serif', serif='Times')
#plt.rc('text', usetex=True)
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["legend.fontsize"] = 8
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
fig = plt.figure()
fig.set_size_inches(3.5, 3.5/1.4)
#fig.set_size_inches(3.5*3, 3.5*3/1.4)
co = 6;#5: overall step time, #6: kernel time, #7: rebuild/texture time
#Label axis
plt.xlabel('Actor Population Size');
if co==6:
    plt.ylabel('Average FRNNs Search Time (ms)');
elif co==7:
    plt.ylabel('Average PBM Rebuild Time (ms)');
else:
    print('Unexpected column (5-6 required)');
    sys.exit(0);
###
### Load Data, Create tuples of matching columns from each file
###
csvDefault = loadCSV('[3D] Default, Circles Model, Scaling Pop.csv');
csvStrips = loadCSV('[3D] Strips, Circles Model, Scaling Pop.csv');
fails = (csvDefault.pop(-1), csvStrips.pop(-1));
kernelTime = (csvDefault.pop(-1), csvStrips.pop(-1));
pbmTime = (csvDefault.pop(-1), csvStrips.pop(-1));
envWidth = (csvDefault.pop(-1), csvStrips.pop(-1));
agentCount = (csvDefault.pop(-1), csvStrips.pop(-1));
radialNeighbour = (csvDefault.pop(-1), csvStrips.pop(-1));
binWidth = (csvDefault.pop(-1), csvStrips.pop(-1));
radius = (csvDefault.pop(-1), csvStrips.pop(-1));
###
### Filter data, Only publish bin width's that we want
###
desiredWidths = [1.0, 0.5];
minWidth = [-1,-1];
colorI = 0;
for j in range(len(binWidth)):
    while True:
        #Find which binWidth to plot next
        t_minWidth = 1000000;
        for i in range(len(binWidth[0])):
            if binWidth[j][i]>minWidth[j] and binWidth[j][i]<t_minWidth and (binWidth[j][i] in desiredWidths):
                t_minWidth = binWidth[j][i];
        minWidth[j] = t_minWidth;
        if minWidth[j] == 1000000:
            break;
    #Collect that bin width's data into a temporary array
        if (j==0 and minWidth[j]!=1.0) or (j==1 and minWidth[j]!=0.5):
            continue;
        x = [];
        y = [];
        for i in range(len(binWidth[j])):
            if binWidth[j][i]==minWidth[j]:# and fails[j][i]==0:# #Toggle full vs low density
                x.append(agentCount[j][i]);
                #if kernelTime[j][i]>16:
                #    x = [];
                #    break;
                if co==6:
                    y.append(kernelTime[j][i]);
                elif co==7:
                    y.append(pbmTime[j][i]);            
        #Send to plot
        if(len(x)>2):
            plotLine('%s %.2f' % (models[j], minWidth[j]), x, y, colors[colorI], '-');
            colorI+=1;
            if colorI>=len(colors):
                colorI = 0;
###
### Position Legend
###
#plt.legend(loc='lower right',numpoints=1);
plt.legend(loc='upper left',numpoints=1);
plt.tight_layout();

###
### Export/Show Plot
###
plt.savefig('[3D] Circles Pop.eps')
plt.savefig('[3D] Circles Pop.pdf')
plt.savefig('[3D] Circles Pop.png')
plt.close();
#plt.show();
