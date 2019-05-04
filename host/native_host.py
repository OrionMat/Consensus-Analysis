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
url_list, date_list = news_web_scraping.google_NYT_links(query)
title_list, article_list = news_web_scraping.NYT_links_scrape(url_list)
#for idx in range(len(title_list)):
#    print(date_list[idx], "  :  ", title_list[idx], "  :  ", url_list[idx])
#    print(article_list[idx][0:50], '\n')
if title_list and date_list and article_list and url_list:
    news_dicList = save_to_CSV.lists_to_dictList('NYT', title_list, date_list, article_list, url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList) 
send_message({"name": "response", "text": "written NYT results"})

# BBC:
url_list = news_web_scraping.google_BBC_links(query)
title_list, article_list, date_list = news_web_scraping.BBC_links_scrape(url_list)
#for idx in range(len(title_list)):
#    print(date_list[idx], "  :  ", title_list[idx], "  :  ", url_list[idx])
#    print(article_list[idx][0:50], '\n')
if title_list and date_list and article_list and url_list:
    news_dicList = save_to_CSV.lists_to_dictList('BBC', title_list, date_list, article_list, url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList)   
send_message({"name": "response", "text": "written BBC results"})

# AP:
url_list = news_web_scraping.google_AP_links(query)
title_list, article_list, date_list = news_web_scraping.AP_links_scrape(url_list)
#for idx in range(len(title_list)):
#    print(date_list[idx], "  :  ", title_list[idx], "  :  ", url_list[idx])
#    print(article_list[idx][0:50], '\n')
if title_list and date_list and article_list and url_list:
    news_dicList = save_to_CSV.lists_to_dictList('AP', title_list, date_list, article_list, url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList)   
send_message({"name": "response", "text": "written AP results"})

# Reuters:
url_list = news_web_scraping.google_reuters_links(query)
title_list, article_list, date_list = news_web_scraping.reuters_links_scrape(url_list)
#for idx in range(len(title_list)):
#    print(date_list[idx], "  :  ", title_list[idx], "  :  ", url_list[idx])
#    print(article_list[idx][0:50], '\n')
if title_list and date_list and article_list and url_list:
    news_dicList = save_to_CSV.lists_to_dictList('Reuters', title_list, date_list, article_list, url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList) 
send_message({"name": "response", "text": "written reuters results", "numReuters": len(title_list)})

for idx in range(len(title_list)):
    send_message({"name": "title" + str(idx), "text": title_list[idx]})