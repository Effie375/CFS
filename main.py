from csv import writer, reader
from pathlib import Path
from datetime import datetime
import os, glob
import plotter
import csv


def get_csv(path):
    read_file = open(path, 'r')
    csv_data = list(reader(read_file))
    read_file.close()
    return csv_data


def check_subj(subj_path, csv_path, subj_lst):
    sort_lst = []
    try:
        list_of_rows = list(get_csv(csv_path))
        if(len(list_of_rows[0])-1) != (len(subj_lst)):
            list_of_rows[0].pop(0)
            new_subj_lst = list(set(subj_lst)-set(list_of_rows[0]))
            # create a sorted listing by creation date
            for index in range(len(new_subj_lst)):
                new_subj_lst[index] = os.path.join(subj_path, new_subj_lst[index])
            new_subj_lst.sort(key=lambda x: os.path.getctime(x))
            for subj in new_subj_lst:
                sort_lst.append(os.path.basename(os.path.normpath(subj)))
            return sort_lst
    except:
        return


def write_data(csv_path, subject_lst, subj_path):
    x = []
    data = open(csv_path, 'a', newline='')
    data_wr = csv.writer(data)
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    x.insert(0,dt_string)
    for i in range(len(subject_lst)):
        # todo dynamic
        faecher_path = subj_path + "\\" + subject_lst[i]
        count = sum([len(files) for r, d, files in os.walk(faecher_path)])
        # date.today(), count
        x.insert(i+1,count)
    data_wr.writerow(x)
    x.clear()
    data.close()
    return


def update_data(path, new_subj_lst):
    old_data_lst = get_csv(path)
    old_data_lst.pop(0)
    obj = open(path, 'w', newline='')
    updater = csv.writer(obj)
    new_header = ["Date"]
    for header in new_subj_lst:
        new_header.append(header)
    updater.writerow(new_header)
    for old_data in old_data_lst:
        updater.writerow(old_data)
    obj.close()
    return


def sort_by_date(path):
    sort_lst = []
    # get a directory listing sorted by creation date
    dirs = list(filter(os.path.isdir, glob.glob(path + "\\*")))
    dirs.sort(key=lambda x: os.path.getctime(x))
    for subj in dirs:
        sort_lst.append(os.path.basename(os.path.normpath(subj)))
    return sort_lst


def CSV_handler(csv_path, subj_path): 
    # get a directory listing sorted by creation date
    subject_lst = sort_by_date(subj_path)
    # detect if any subject added
    new_element = check_subj(subj_path, csv_path, subject_lst)
    if not csv_path.exists():
        file = open(csv_path, 'w', newline='')
        writer = csv.writer(file)
        if new_element:
            subject_lst.append(new_element)
        header_lst = ["Date"]
        for header in subject_lst:
            header_lst.append(header)
        writer.writerow(header_lst)
        file.close()
    else:
        if new_element:
            update_data(csv_path, subject_lst)

    write_data(csv_path, subject_lst, subj_path)
    # plotter.plot(csv_path)
    subject_lst.clear()


# It's as if the interpreter inserts this at the top
# of your module when run as the main program.
if __name__ == "__main__":
    csv_f = Path(r"C:\Users\Ioannis\Desktop\GitHub\CFS\AEGEAN.csv")
    subject_d = r"C:\Users\Ioannis\Desktop\GitHub\CFS\AEGEAN"
    CSV_handler(csv_f, subject_d)
