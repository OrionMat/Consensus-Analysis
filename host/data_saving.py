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






# deal with this: (format, add getting dates and links to corresponding functions)

#nyt_opinion_url = 'https://www.nytimes.com/section/opinion'
#nyt_world_url = 'https://www.nytimes.com/section/world'

#NYTscrap_opinion_title_list, NYTscrap_opinion_sentence_list, NYTscrap_opinion_sentence_sentiments, NYTscrap_opinion_article_sentiments = NSA.NYT_scrape_SA(nyt_opinion_url)
#NYTscrap_world_title_list, NYTscrap_world_sentence_list, NYTscrap_world_sentence_sentiments, NYTscrap_world_article_sentiments = NSA.NYT_scrape_SA(nyt_world_url)

#news_dicList = lists_to_dictList('NYT opinion', NYTscrap_opinion_title_list, NYTscrap_opinion_sentence_list)
#print(news_dicList)
#news_dictionary = dict(zip(NYTscrap_opinion_title_list, NYTscrap_opinion_sentence_list))





#csv_file_path = 'consensus_data.csv'
#csv_columns = ['agency','title', 'date', 'article', 'link']

#initiate_csv(csv_file_path, csv_columns)                 # use first time 
#append_csv(csv_file_path, csv_columns, news_dicList)     # use rest of the time


