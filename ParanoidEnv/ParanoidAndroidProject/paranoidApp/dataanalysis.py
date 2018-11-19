"""Helper code to analyse survey data"""

# import pickle
import os
import json
import re
# from textwrap import wrap
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
        print('Error: The folder wasn\'t able to be created: ' + directory)

def data_analytics(survey_csv_file, survey_json_file, survey_id):
    """Analyse some data from a file"""
    style.use('ggplot')
    # title_font = {'size':'8'}

    # Get the structure of the survey we're analysing
    survey_stucture = json.loads(open(survey_json_file, "r").read())

    ##cleaning the current date time to be just a number to use as the file and folder names
    # currentdatetime = str(datetime.datetime.now())
    # currentdatetime = currentdatetime.replace("-", "")
    # currentdatetime = currentdatetime.replace(":", "")
    # currentdatetime = currentdatetime.replace(".", "")
    # currentdt = currentdatetime.replace(" ", "")
    static_path = "paranoidApp/analytics/survey_" + str(survey_id) + "_data" + '/'
    path = (os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            + "/static/" + static_path)
    ##creating the uniquely named folder to save all data to
    create_folder(path)

    ##need to put code to recieve a file name instead of using the static sample data file
    data_frame = pd.read_csv(survey_csv_file)


    ##saving the dataframe as a pickle for its current state
    # pickle_out = open(path + currentdt + ".pickle", "wb")
    # pickle.dump(df, pickle_out)
    # pickle_out.close()

    numerical_columns = []
    for question in survey_stucture["questions"]:
        if question["type"] in ["numerical", "number_rating"]:
            numerical_columns.append(question["column-name"])
        if "on" in question.keys():
            for subquestion in question["subquestions"]:
                if subquestion["type"] in ["numerical", "number_rating"]:
                    numerical_columns.append(subquestion["column-name"])

    ##get numeric columns and save in a new DF to then loop through and get specific statistics
    typedf = data_frame[numerical_columns]   #.select_dtypes(include='number')
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

        # plt.xlabel('Rating', **title_font)
        # plt.ylabel('# of Responses', **title_font)
        # plt.title(("\n".join(wrap(col, 60))), **title_font)
        # plt.legend()
        plt.savefig(path + col + '.svg')
        plt.clf()
        plt.close()

    with open(path + 'analytics.csv', 'w+') as myfile:
        # wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=',')
        # wr.write(csv_data)
        myfile.write(csv_data)
    myfile.close()

    ##get the Dataframe of just the object columns
    # objectdf = data_frame.select_dtypes(exclude='number')
    # days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    # # check if any of the columns are days of the week columns,
	# # then get averages for each day by numerical columns
    # for obcol in objectdf:
    #     result = all(elem in days for elem in objectdf[obcol])
    #     if result:
    #         for col in typedf:
    #             anotherlist = data_frame.groupby(obcol).mean()[[col]]
    #             with open(path + currentdt + '_per_dow.csv', 'a') as myfile:
    #                 anotherlist.to_csv(myfile, header=True)
    #                 myfile.close()

    # Oisín notes: Added charts for Multiple choice questions and booleans
    for question in survey_stucture["questions"]:
        graph_multiple_choice(question["type"], question, data_frame, path)
        try:
            for subquestion in question["subquestions"]:
                graph_multiple_choice(subquestion["type"], subquestion, data_frame, path)
        except KeyError:
            pass

    return static_path


def graph_multiple_choice(question_type, question, data_frame, path):
    """Graphing multiple choice questions"""
    if (question_type in ["radio", "dropdown"]):
        # Get this question's data
        column_data = data_frame[question["column-name"]].astype('str')

        new_labels = []
        new_counts = []
        for option in question["choices"]:
            new_labels.append(option)
            new_counts.append(column_data.str.count("^" + re.escape(option) + "$").sum())

        num_items = np.arange(0, len(new_counts))

        plt.bar(num_items, new_counts)
        plt.xticks(num_items, new_labels, rotation="vertical")
        plt.tight_layout()

        plt.savefig(path + question["column-name"] + '.svg')
        plt.clf()
        plt.close()

    if question_type == "boolean":
        column_data = data_frame[question["column-name"]].astype('str')
        new_counts = []
        choices = ["Yes", "No"]
        for option in choices:
            new_counts.append(column_data.str.count(option).sum())

        num_items = np.arange(0, len(new_counts))

        plt.bar(num_items, new_counts)
        plt.xticks(num_items, choices)
        plt.tight_layout()

        plt.savefig(path + question["column-name"] + '.svg')
        plt.clf()
        plt.close()
