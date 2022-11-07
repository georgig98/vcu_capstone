import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def runAnalyzer():
############################################################################################
	# Import the data
	raw_data = pd.read_csv('rawdata.csv')
	back_data = pd.read_csv('backdata.csv')
############################################################################################
	# The following code sets up the bins used to lower the channel count from 
	# 4096 to 1024 and then adds the bins to the pandas data-frame
	upper = 4
	bins = []

	for i in range(1024):
		bins.append(upper)
		upper = upper+4
		
	raw_data['Channel Bin'] = pd.cut(raw_data['Channel'], bins = bins, labels = range(1023))
############################################################################################
	#The following code sets up the bins used range the time from beginning to end
	index = int(raw_data['Time'].iloc[-1]/1000)+1
	upper = 0
	bins = []

	for i in range(index):
		bins.append(upper)
		upper = upper + 1
	bins.append(upper)

	raw_data['Time(s)'] = raw_data['Time'] / 1000
	raw_data['Time Bins'] = pd.cut(raw_data['Time']/1000,
		 bins = bins, labels = np.array(range(index))+1 )
############################################################################################
	# The following code determines the energy level of each channel
	energy_range= np.array(range(1024))+1
	energy_range = 9.22+2.02*energy_range
############################################################################################
	# The following code determines the energy of each count
	count_energy = np.array(raw_data['Channel Bin'])
	count_energy = 9.22+2.02*count_energy
	raw_data['Energy (keV)'] = count_energy
############################################################################################
	# The following code determines the bin counts of each channel
	channel_count = []
	channels = (np.array(range(1024))+1)

	for i in range(1024):
	  channel_count.append(sum(raw_data['Channel Bin'] == i+1))
	channel_count = np.array(channel_count)  
############################################################################################
	# The following code determines the estimated background radiation
	back_est = np.array(back_data['Slope'])*raw_data['Time'].iloc[-1]

	back_sub = []
	for i in range(1024):
	  back_sub.append(max(channel_count[i]-back_est[i],0))

	back_sub = np.array(back_sub)
############################################################################################
	# The following code determines weather or not a given channel has peaked above the 
	# expected background radiation by a ratio of 5
	peaks = []
	for i in range(1024):
		if back_est[i] > 0:
			peaks.append(channel_count[i]/back_est[i])
		elif back_est[i] <= 0 :
			peaks.append(channel_count[i])
			
	peak_ratio = 9
	
	for i in range(1024):
		if peaks[i] >= peak_ratio:
			peaks[i] = 1
		elif peaks[i] < peak_ratio:
			peaks[i] = 0
	
	peaks = np.array(peaks)
	
	print('Total number of unexpected peaks:	' + str(sum(peaks)))
	
	
############################################################################################
	# The following code sets up some of the settings for plotting
	plot = False
	if plot == True:
		plt.rcParams['axes.facecolor'] = 'silver'
		plt.hot()
		plt.subplot(3,1,1)
		plotx = np.array(raw_data['Energy (keV)'])
		ploty = (np.array(raw_data['Time']))/1000
		scale =  0.000025**2*(plotx)**3
############################################################################################
		# The following code plots the data over time on a scatter plot
		plt.scatter(ploty,
					plotx,
					s = scale,
					c=plotx,
					alpha = 0.5)

		plt.xlabel('Time (s)')
		plt.ylabel('Energy (keV)')
		plt.title('Radiation Counts Over Time')
############################################################################################
		# The following forms the Line plot
		plt.subplot(3,1,2)
		plt.plot(energy_range,
				 channel_count,
				 color = 'black',
				 lw = 0.15,
				 alpha = 0.9)
		plt.scatter(energy_range,
					channel_count, 
					c = channel_count,
					s = 0.1,
					alpha = 0.6)
		plt.xlabel('Energy (keV)')
		plt.ylabel('Counts')
		plt.title('Accumulated Radiation Counts per Energy Level')
############################################################################################
		# Plot the background subtracted line plot
		plt.subplot(3,1,3)
		plt.plot(energy_range,
				 back_sub,
				 color = 'black',
				 lw = 0.15,
				 alpha = 0.9)
		plt.scatter(energy_range,
					back_sub, 
					c = back_sub,
					s = 0.1,
					alpha = 0.6)
		plt.xlabel('Energy (keV)')
		plt.ylabel('Counts')
		plt.title('Accumulated Radiation Counts per Energy Level (Background Subtracted)')
############################################################################################
		# The following code properly arranges the plots and saves the figure before
		# showing the plot
		plt.tight_layout()
		manager = plt.get_current_fig_manager()
		manager.resize(*manager.window.maxsize())
		
		manager.window.wm_geometry('-1+0')
		plt.savefig('Radiation Detection Run.png')
		plt.show(block = True)
		
############################################################################################
	
runAnalyzer()
