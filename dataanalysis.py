import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pickle
import datetime
import os
import csv
from textwrap import wrap
style.use('ggplot')
title_font = {'size':'8'}

##folder creation code to be called later
def createFolder(directory):
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
			
	except OSError:
		print('Error: The folder wasnt able to be created:' + directory)

##cleaning the current date time to be just a number to use as the file and folder names
currentdatetime = str(datetime.datetime.now())
currentdatetime = currentdatetime.replace("-","")
currentdatetime = currentdatetime.replace(":","")
currentdatetime = currentdatetime.replace(".","")
currentdt = currentdatetime.replace(" ","")
path = './' + currentdt + '/'
##creating the uniquely named folder to save all data to
createFolder(path)

##need to put code to recieve a file name instead of using the static sample data file
df = pd.read_csv('sampledata.csv')


##saving the dataframe as a pickle for its current state
pickle_out = open(path + currentdt + ".pickle","wb")
pickle.dump(df, pickle_out)
pickle_out.close()

##get numeric columns and save in a new DF to then loop through and get specific statistics
typedf = df.select_dtypes(include='number')

for col in typedf:
	##making the templist to write to the cvs file for this columns stats
	templist = [col,np.nanmax(typedf[col].values),np.nanmin(typedf[col].values),
				round(np.nanmean(typedf[col].values),2),np.nanmedian(typedf[col].values)]
		
	##writing to a csv file witht the col stats

	with open(path + currentdt + '.csv', 'a') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL,delimiter=',')
		wr.writerow(templist)
	myfile.close()	
	
	##clean up templist for reuse
	del templist[:]
	
	##creating graphs of the numerical columns after determining a customer range for the values of the column
	bins = []
	min = int(np.nanmin(typedf[col].values))
	max = int(np.nanmax(typedf[col].values) + 1)
	for x in range(min, max):
		bins.append(x)
		
		
	plt.hist(typedf[col], bins, histtype='bar', rwidth=0.8)
	
	plt.xlabel('Rating', **title_font)
	plt.ylabel('# of Responses', **title_font)
	plt.title(("\n".join(wrap(col,60))), **title_font)
	plt.legend()
	plt.savefig(path + col.replace("?","") + '.svg')
	plt.clf()

##get the Dataframe of just the object columns
objectdf = df.select_dtypes(exclude='number')
days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

#cheack if any of the columns are days of the week columns then get averages for each day by numerical columns
for obcol in objectdf:
	result = all(elem in days for elem in objectdf[obcol])
	if result:
	
		for col in typedf:
			anotherlist = df.groupby(obcol).mean()[[col]]
			with open(path + currentdt + '.csv', 'a') as myfile:
				anotherlist.to_csv(myfile, header=True)
				myfile.close()


