import sys
import json
import struct
import data_saving as save_to_CSV
import news_web_scraping
import csv
import random



# Function to send a message to chrome.
def send_message(MSG_DICT):
    msg_json = json.dumps(MSG_DICT, separators=(",", ":"))          # Converts dictionary into string containing JSON format.
    msg_json_utf8 = msg_json.encode("utf-8")                        # Encodes string with UTF-8.
    sys.stdout.buffer.write(struct.pack("i", len(msg_json_utf8)))   # Writes the message size. (Writing to buffer because writing bytes object.)
    sys.stdout.buffer.write(msg_json_utf8)                          # Writes the message itself. (Writing to buffer because writing bytes object.)

# Function to read a message from Chrome.
def read_message():
    text_length_bytes = sys.stdin.buffer.read(4)                        # Reads the first 4 bytes of the message (which designates message length).
    text_length = struct.unpack("i", text_length_bytes)[0]              # Unpacks the first 4 bytes that are the message length. [0] required because unpack returns tuple with required data at index 0.
    text_decoded = sys.stdin.buffer.read(text_length).decode("utf-8")   # Reads and decodes the text (which is JSON) of the message. [...] Then use the data.
    text_dict = json.loads(text_decoded)
    return text_dict

query_dict = read_message()
query = query_dict['text']
#query = "Can Trump declare a national emergency to build a wall?"



# %% query seach and save to CSV
csv_file_path = 'consensus_data.csv'
csv_columns = ['agency', 'title', 'date', 'article', 'link']
save_to_CSV.initiate_csv(csv_file_path, csv_columns)
send_message({"name": "response", "text": "initiated CSV file"})

# NYT:
url_list, date_list = news_web_scraping.google_NYT_links(query)
title_list, article_list = news_web_scraping.NYT_links_scrape(url_list)
if title_list and date_list and article_list and url_list:
    news_dicList = save_to_CSV.lists_to_dictList('NYT', title_list, date_list, article_list, url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList) 
send_message({"name": "response", "text": "written NYT results"})

# BBC:
url_list = news_web_scraping.google_BBC_links(query)
title_list, article_list, date_list = news_web_scraping.BBC_links_scrape(url_list)
if title_list and date_list and article_list and url_list:
    news_dicList = save_to_CSV.lists_to_dictList('BBC', title_list, date_list, article_list, url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList)   
send_message({"name": "response", "text": "written BBC results"})

# AP:
url_list = news_web_scraping.google_AP_links(query)
title_list, article_list, date_list = news_web_scraping.AP_links_scrape(url_list)
if title_list and date_list and article_list and url_list:
    news_dicList = save_to_CSV.lists_to_dictList('AP', title_list, date_list, article_list, url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList)   
send_message({"name": "response", "text": "written AP results"})

# Reuters:
url_list = news_web_scraping.google_reuters_links(query)
title_list, article_list, date_list = news_web_scraping.reuters_links_scrape(url_list)
if title_list and date_list and article_list and url_list:
    news_dicList = save_to_CSV.lists_to_dictList('Reuters', title_list, date_list, article_list, url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList) 
send_message({"name": "response", "text": "written reuters results"})
    

# read titles and urls from csv file
agency_list = []
titles_list = []
date_lists = []
url_list = []
result_list = []
send_message({"name": "response", "text": "humnahumnahumna"})
with open('consensus_data.csv', mode='r') as csv_file:
    send_message({"name": "response", "text": "pass1"})
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    print(type(csv_reader))
    for row in csv_reader:
        agency_list += [row['agency']] 
        titles_list += [row['title']] 
        date_lists += [row['date']]
        url_list += [row['link']]

num_Articles = len(titles_list)
agencies = json.dumps(agency_list)
titles = json.dumps(titles_list) 
dates = json.dumps(date_lists)
urls = json.dumps(url_list)

result_ops = ["Agree", "Disagree", "discusses", "unrelated"]
for i in range(num_Articles):
    result_list += [random.choice(result_ops)]
results = json.dumps(result_list)

send_message({"name": "response", "text": "pass"})
 
send_message({"name" : "articleNumbers", "text" : "sending numbers of articles", "num_Articles" : str(num_Articles)})
send_message({"name" : "articleAgencies", "text" : "sending agencies of articles", "agencies" : agencies})
send_message({"name" : "articleTitles", "text" : "sending titles of articles", "titles" : titles})
send_message({"name" : "articleDates", "text" : "sending dates of articles", "dates" : dates})
send_message({"name" : "articleURLs", "text" : "sending urls of articles", "urls" : urls})
send_message({"name" : "articleResults", "text" : "sending results of articles", "results" : results})


# send_message({"name" : "reuters", "text" : "sending reuters", "titles" : R_json_titles})

# for idx in range(len(title_list)):
#     send_message({"name": "title" + str(idx), "text": title_list[idx]})