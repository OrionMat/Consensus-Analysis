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
#for idx in range(len(NYT_title_list)):
#    print(NYT_date_list[idx], "  :  ", NYT_title_list[idx], "  :  ", NYT_url_list[idx])
#    print(NYT_article_list[idx][0:50], '\n')
if NYT_title_list and NYT_date_list and NYT_article_list and NYT_url_list:
    news_dicList = save_to_CSV.lists_to_dictList('NYT', NYT_title_list, NYT_date_list, NYT_article_list, NYT_url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList) 
send_message({"name": "response", "text": "written NYT results"})

# BBC:
BBC_url_list = news_web_scraping.google_BBC_links(query)
BBC_title_list, BBC_article_list, BBC_date_list = news_web_scraping.BBC_links_scrape(BBC_url_list)
#for idx in range(len(BBC_title_list)):
#    print(BBC_date_list[idx], "  :  ", BBC_title_list[idx], "  :  ", BBC_url_list[idx])
#    print(BBC_article_list[idx][0:50], '\n')
if BBC_title_list and BBC_date_list and BBC_article_list and BBC_url_list:
    news_dicList = save_to_CSV.lists_to_dictList('BBC', BBC_title_list, BBC_date_list, BBC_article_list, BBC_url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList)   
send_message({"name": "response", "text": "written BBC results"})

# AP:
AP_url_list = news_web_scraping.google_AP_links(query)
AP_title_list, AP_article_list, AP_date_list = news_web_scraping.AP_links_scrape(AP_url_list)
#for idx in range(len(AP_title_list)):
#    print(AP_date_list[idx], "  :  ", AP_title_list[idx], "  :  ", AP_url_list[idx])
#    print(AP_article_list[idx][0:50], '\n')
if AP_title_list and AP_date_list and AP_article_list and AP_url_list:
    news_dicList = save_to_CSV.lists_to_dictList('AP', AP_title_list, AP_date_list, AP_article_list, AP_url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList)   
send_message({"name": "response", "text": "written AP results"})

# Reuters:
R_url_list = news_web_scraping.google_reuters_links(query)
R_title_list, R_article_list, R_date_list = news_web_scraping.reuters_links_scrape(R_url_list)
#for idx in range(len(R_title_list)):
#    print(R_date_list[idx], "  :  ", R_title_list[idx], "  :  ", R_url_list[idx])
#    print(R_article_list[idx][0:50], '\n')
if R_title_list and R_date_list and R_article_list and R_url_list:
    news_dicList = save_to_CSV.lists_to_dictList('Reuters', R_title_list, R_date_list, R_article_list, R_url_list)
    save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList) 
send_message({"name": "response", "text": "written reuters results"})
    




NYT_json_titles = json.dumps(NYT_title_list)
BBC_json_titles = json.dumps(BBC_title_list)
AP_json_titles = json.dumps(AP_title_list)
R_json_titles = json.dumps(R_title_list)
titles_list = NYT_title_list + BBC_title_list + AP_title_list + R_title_list
titles = json.dumps(titles_list) 
numArticles = len(titles_list)

send_message({"name" : "articleTitles", "text" : "sending titles of articles", "numArticles" : str(numArticles), "titles" : titles})
# send_message({"name" : "reuters", "text" : "sending reuters", "titles" : R_json_titles})

# for idx in range(len(title_list)):
#     send_message({"name": "title" + str(idx), "text": title_list[idx]})