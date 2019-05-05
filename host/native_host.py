import sys
import json
import struct
import data_saving as save_to_CSV
import news_web_scraping


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
NYT_url_list, NYT_date_list = news_web_scraping.google_NYT_links(query)
NYT_title_list, NYT_article_list = news_web_scraping.NYT_links_scrape(NYT_url_list)
if NYT_title_list and NYT_date_list and NYT_article_list and NYT_url_list:
    news_dicList = save_to_CSV.lists_to_dictList('NYT', NYT_title_list, NYT_date_list, NYT_article_list, NYT_url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList) 
send_message({"name": "response", "text": "written NYT results"})

# BBC:
BBC_url_list = news_web_scraping.google_BBC_links(query)
BBC_title_list, BBC_article_list, BBC_date_list = news_web_scraping.BBC_links_scrape(BBC_url_list)
if BBC_title_list and BBC_date_list and BBC_article_list and BBC_url_list:
    news_dicList = save_to_CSV.lists_to_dictList('BBC', BBC_title_list, BBC_date_list, BBC_article_list, BBC_url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList)   
send_message({"name": "response", "text": "written BBC results"})

# AP:
AP_url_list = news_web_scraping.google_AP_links(query)
AP_title_list, AP_article_list, AP_date_list = news_web_scraping.AP_links_scrape(AP_url_list)
if AP_title_list and AP_date_list and AP_article_list and AP_url_list:
    news_dicList = save_to_CSV.lists_to_dictList('AP', AP_title_list, AP_date_list, AP_article_list, AP_url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList)   
send_message({"name": "response", "text": "written AP results"})

# Reuters:
R_url_list = news_web_scraping.google_reuters_links(query)
R_title_list, R_article_list, R_date_list = news_web_scraping.reuters_links_scrape(R_url_list)
if R_title_list and R_date_list and R_article_list and R_url_list:
    news_dicList = save_to_CSV.lists_to_dictList('Reuters', R_title_list, R_date_list, R_article_list, R_url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList) 
send_message({"name": "response", "text": "written reuters results"})
    


# read titles and urls from csv file
titles_list = NYT_title_list + BBC_title_list + AP_title_list + R_title_list
date_list = NYT_date_list + BBC_date_list + AP_date_list + R_date_list
url_list = NYT_url_list + BBC_url_list + AP_url_list + R_url_list

num_NYT = len(NYT_title_list)
num_BBC = len(BBC_title_list)
num_AP = len(AP_title_list)
num_R = len(R_title_list)
num_Articles = len(titles_list)

agency_list = ["NYT"]*num_NYT + ["BBC"]*num_BBC + ["AP"]*num_AP + ["R"]*num_R

agencies = json.dumps(agency_list)
titles = json.dumps(titles_list) 
dates = json.dumps(date_list)
urls = json.dumps(url_list)

 
send_message({"name" : "articleNumbers", "text" : "sending numbers of articles", "num_Articles" : str(num_Articles)})
send_message({"name" : "articleAgencies", "text" : "sending agencies of articles", "agencies" : agencies})
send_message({"name" : "articleTitles", "text" : "sending titles of articles", "titles" : titles})
send_message({"name" : "articleDates", "text" : "sending dates of articles", "dates" : dates})
send_message({"name" : "articleURLs", "text" : "sending urls of articles", "urls" : urls})

# send_message({"name" : "reuters", "text" : "sending reuters", "titles" : R_json_titles})

# for idx in range(len(title_list)):
#     send_message({"name": "title" + str(idx), "text": title_list[idx]})