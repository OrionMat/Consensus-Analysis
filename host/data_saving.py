# DATA SAVING
import csv





#%% CSV saving

# initiates csv file and writes headers
# use when running script for first time 
# i.e no existing data in csv file
def initiate_csv(csv_file, csv_headers):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            writer.writeheader()
    except IOError:
        print("I/O error") 

def append_csv(csv_file, csv_headers, dict_data):
    # checks for repeated articles by their titles and agency
    agency_list = []
    title_list = []
    try:
        with open(csv_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                agency_list = agency_list + [row['agency']]
                title_list = title_list + [row['title']]
    except IOError:
        print("I/O error") 
    # appends data to csv file
    try:
        with open(csv_file, 'a', errors='ignore') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            for data in dict_data:
                if data['title'] not in title_list:
                    writer.writerow(data)
                else:
                    indices = [i for i, x in enumerate(title_list) if x == data['title']]   # gets list of indexes where title is the same
                    agencies = [agency_list[index] for index in indices]                    # selects the correspoding agencies
                    for agency in agencies:
                        # checks if agency is the different 
                        if data['agency'] != agency:
                            writer.writerow(data)
    except IOError:
        print("I/O error") 

def lists_to_dictList(agency, title_list, date_list, article_list, url_list):
    dic_list =[]
    for idx in range(len(title_list)):
        dic = {'agency' : agency, 'title' : title_list[idx], 'date' : date_list[idx], 'article' : article_list[idx], 'link' : url_list[idx]}
        dic_list.append(dic)
    return dic_list


def format_art_bodies(consensus_data, art_bodies, statement_file, statement):
    # read article bodies from csv file
    article_list = []
    with open(consensus_data, mode='r', errors='ignore') as csv_file: 
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            article_list += [row['article']] 

    # write article bodies with ID to art_bodies.csv
    try:
        with open(art_bodies, 'w') as csv_file:

            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Body ID', 'articleBody'])
            idx = 1
            for article in article_list:
                writer.writerow([str(idx), article])
                idx += 1
    except IOError:
        print("I/O error")

    # write article statement with ID to statement.csv
    try:
        with open(statement_file, 'w') as csv_file:

            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Headline', 'Body ID'])
            for idx in range(len(article_list)):
                writer.writerow([statement, str(idx+1)])
    except IOError:
        print("I/O error")