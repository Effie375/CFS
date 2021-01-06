import plotly.graph_objects as go
from pathlib import Path
from csv import reader
import numpy as np
import six

fig_lst =  []
subj_lst = []
T_subj_lst = []


def plot(path):
    # read csv file as a list of lists
    read_obj = open(path, 'r')
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # get a list of the csv file
    csv_lst = list(csv_reader)
    # loop for each subject in header
    for subj in csv_lst[0]:
        # append the list with the subjects
        subj_lst.append(subj)
    # remove the date from the header row
    subj_lst.pop(0)
    # remove the header row
    csv_lst.pop(0)
    # transpose the subject list and fill it with None if an element doesn't exists
    T_subj_lst = list(map(list, six.moves.zip_longest(*csv_lst, fillvalue=None)))
    for index in range(1, (len(subj_lst)+1)):
        fig_lst.append(go.Scatter(x=T_subj_lst[0], y=T_subj_lst[index], mode="lines", name=str(subj_lst[index-1])))
    fig = go.Figure(data=fig_lst)
    # show the figure
    fig.show()
    # close the reader object
    read_obj.close()


# It's as if the interpreter inserts this at the top
# of your module when run as the main program.
if __name__ == "__main__":
    csv_file = Path(r"C:\Users\Ioannis\Desktop\GitHub\CFS\AEGEAN.csv")
    plot(csv_file)
