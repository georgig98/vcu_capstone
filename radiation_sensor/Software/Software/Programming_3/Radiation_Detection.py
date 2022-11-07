# This code is the property of Hubert E Coburn II

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

def runAnalyzer:
	# Import the data
	raw_data = pd.read_csv('rawdata.csv')
	back_data = pd.read_csv('backdata.csv')

	# The following code sets up the bins used to lower the channel count from 
	# 4096 to 1024 and then adds the bins to the pandas data-frame
	upper = 4
	bins = []

	for i in range(1024):
		bins.append(upper)
		upper = upper+4
		
	raw_data['Channel Bin'] = pd.cut(raw_data['Channel'], bins = bins, labels = range(1023))


	#The following code sets up the bins used range the time from beginning to end
	index = int(raw_data['Time'].iloc[-1]/1000)+1
	upper = 0
	bins = []

	raw_data['Energy (keV)'] = raw_data['Channel Bin']

	for i in range(index):
		bins.append(upper)
		upper = upper + 1
	bins.append(upper)


	raw_data['Time(s)'] = raw_data['Time'] / 1000
	raw_data['Time Bins'] = pd.cut(raw_data['Time']/1000,
		 bins = bins, labels = np.array(range(index))+1 )

	# The following code determines the energy level of each channel
	 
	raw_data['Energy (keV)'] = np.array(raw_data['Channel Bin'])*2  


	# The following code determines the bin counts of each channel
	channel_count = []
	energies = (np.array(range(1024))+1)*2


	for i in range(1024):
	  channel_count.append(sum(raw_data['Channel Bin'] == i))
	channel_count = np.array(channel_count)  

	# The following code determines the estimated background radiation
	back_est = np.array(back_data['Slope'])*raw_data['Time'].iloc[-1]

	back_sub = []
	for i in range(1024):
	  back_sub.append(max(channel_count[i]-back_est[i],0))

	back_sub = np.array(back_sub)



# This code is the property of Hubert E Coburn II
	# The following code plots the data over time on a scatter plot
	plt.rcParams['axes.facecolor'] = 'silver'
	plt.hot()
	# ~ plt.ino()
	plt.subplot(3,1,1)
	plotx = np.array(raw_data['Energy (keV)'])
	ploty = (np.array(raw_data['Time']))/1000
	scale =  0.000025**2*(plotx)**3


	plt.scatter(ploty,
				plotx,
				s = scale,
				c=plotx,
				alpha = 0.5)

	plt.xlabel('Time (s)')
	plt.ylabel('Energy (keV)')
	plt.title('Radiation Counts Over Time')
# This code is the property of Hubert E Coburn II

	# The following forms the Line plot
	plt.subplot(3,1,2)
	plt.plot(energies,
			 channel_count,
			 color = 'black',
			 lw = 0.15,
			 alpha = 0.9)
	plt.scatter(energies,
				channel_count, 
				c = channel_count,
				s = 0.1,
				alpha = 0.6)
	plt.xlabel('Energy (keV)')
	plt.ylabel('Counts')
	plt.title('Accumulated Radiation Counts per Energy Level')
# This code is the property of Hubert E Coburn II
	# Plot the background subtracted line plot
	plt.subplot(3,1,3)
	plt.plot(energies,
			 back_sub,
			 color = 'black',
			 lw = 0.15,
			 alpha = 0.9)
	plt.scatter(energies,
				back_sub, 
				c = channel_count,
				s = 0.1,
				alpha = 0.6)
	plt.xlabel('Energy (keV)')
	plt.ylabel('Counts')
	plt.title('Accumulated Radiation Counts per Energy Level (Background Subtracted)')

	plt.tight_layout()
	manager = plt.get_current_fig_manager()
	manager.resize(*manager.window.maxsize())

	plt.savefig('Radiation Detection Run.png')
	plt.show(block = True)

	# ~ count_weight = []
	# ~ index = (raw_data.index[-1])

	# ~ for i in range(index+1):
		# ~ count_weight.append(sum(raw_data['Channel Bin'].iloc[i-200:i+200] == raw_data['Channel Bin'].iloc[i]))
	# ~ count_weight = np.array(count_weight)
	# ~ raw_data['Count Weight'] = count_weight

# This code is the property of Hubert E Coburn II
	# ~ plotx = np.array(raw_data['Energy (keV)'])
	# ~ ploty = np.array(raw_data['Time'])/1000
	# ~ plotz = np.array(raw_data['Count Weight'])
# This code is the property of Hubert E Coburn II
	# ~ scale =  1/(plotx)
	# ~ plt.subplot(3,1,1)
	# ~ fig = plt.axes(projection='3d')
	# ~ fig.scatter(plotx, ploty, plotz,c = plotx,cmap = 'YlOrRd_r', s = 0.25, alpha = 0.3)
	# ~ fig.view_init(elev=0, azim=270)
	# ~ plt.show(block = True)
	# ~ plt.savefig('Radiation Detection Run Ground.png')

	# ~ plt.subplot(3,1,2)
	# ~ fig = plt.axes(projection='3d')
	# ~ fig.scatter(plotx, ploty, plotz,c = plotx,cmap = 'YlOrRd_r', s = 0.25, alpha = 0.3)
	# ~ fig.view_init(elev=90, azim=270)
	# ~ plt.savefig('Radiation Detection Run Air.png')

