"""Helper code to analyse survey data"""

import pickle
import datetime
import os
from textwrap import wrap
from matplotlib import style
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_folder(directory):
    """folder creation code to be called later"""
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: The folder wasn\'t able to be created:' + directory)

def data_analytics(file_name):
    """Analyse some data from a file"""
    style.use('ggplot')
    title_font = {'size':'8'}

    ##cleaning the current date time to be just a number to use as the file and folder names
    currentdatetime = str(datetime.datetime.now())
    currentdatetime = currentdatetime.replace("-", "")
    currentdatetime = currentdatetime.replace(":", "")
    currentdatetime = currentdatetime.replace(".", "")
    currentdt = currentdatetime.replace(" ", "")
    path = os.path.dirname(os.path.abspath(__file__)) + "/data/analytics/" + currentdt + '/'
    ##creating the uniquely named folder to save all data to
    create_folder(path)

    ##need to put code to recieve a file name instead of using the static sample data file
    df = pd.read_csv(file_name)


    ##saving the dataframe as a pickle for its current state
    pickle_out = open(path + currentdt + ".pickle","wb")
    pickle.dump(df, pickle_out)
    pickle_out.close()

    ##get numeric columns and save in a new DF to then loop through and get specific statistics
    typedf = df.select_dtypes(include='number')

    csv_data = "Question,Max,Min,Average,Median"
    for col in typedf:
        ##making the templist to write to the csv file for this columns stats
        csv_data += "\n"
        csv_data += str(col)+"," 
        csv_data += str(np.nanmax(typedf[col].values)) + ","
        csv_data += str(np.nanmin(typedf[col].values)) + ","
        csv_data += str(round(np.nanmean(typedf[col].values), 2)) + ","
        csv_data += str(np.nanmedian(typedf[col].values))
        ##writing to a csv file witht the col stats


        # creating graphs of the numerical columns after determining
		# a customer range for the values of the column
        # bins = []
        col_min = int(np.nanmin(typedf[col].values))
        col_max = int(np.nanmax(typedf[col].values) + 1)
        # for x in range(col_min, col_max+1):
        #     bins.append(x)


        plt.hist(typedf[col], np.arange(col_min, col_max+1)-0.5, histtype='bar', rwidth=0.8)

        plt.xlabel('Rating', **title_font)
        plt.ylabel('# of Responses', **title_font)
        plt.title(("\n".join(wrap(col, 60))), **title_font)
        # plt.legend()
        plt.savefig(path + col.replace("?", "") + '.svg')
        plt.clf()
        plt.close()

    with open(path + currentdt + '.csv', 'w+') as myfile:
        # wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=',')
        # wr.write(csv_data)
        myfile.write(csv_data)
    myfile.close()

    ##get the Dataframe of just the object columns
    objectdf = df.select_dtypes(exclude='number')
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    # check if any of the columns are days of the week columns,
	# then get averages for each day by numerical columns
    for obcol in objectdf:
        result = all(elem in days for elem in objectdf[obcol])
        if result:
            for col in typedf:
                anotherlist = df.groupby(obcol).mean()[[col]]
                with open(path + currentdt + '.csv', 'a') as myfile:
                    anotherlist.to_csv(myfile, header=True)
                    myfile.close()
