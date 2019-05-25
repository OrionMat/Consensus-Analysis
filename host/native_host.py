import sys
import json
import struct
import data_saving as save_to_CSV
import news_web_scraping
import csv
import random
from util import *
import tensorflow as tf


# # Function to send a message to chrome.
# def send_message(MSG_DICT):
#     msg_json = json.dumps(MSG_DICT, separators=(",", ":"))          # Converts dictionary into string containing JSON format.
#     msg_json_utf8 = msg_json.encode("utf-8")                        # Encodes string with UTF-8.
#     sys.stdout.buffer.write(struct.pack("i", len(msg_json_utf8)))   # Writes the message size. (Writing to buffer because writing bytes object.)
#     sys.stdout.buffer.write(msg_json_utf8)                          # Writes the message itself. (Writing to buffer because writing bytes object.)

# # Function to read a message from Chrome.
# def read_message():
#     text_length_bytes = sys.stdin.buffer.read(4)                        # Reads the first 4 bytes of the message (which designates message length).
#     text_length = struct.unpack("i", text_length_bytes)[0]              # Unpacks the first 4 bytes that are the message length. [0] required because unpack returns tuple with required data at index 0.
#     text_decoded = sys.stdin.buffer.read(text_length).decode("utf-8")   # Reads and decodes the text (which is JSON) of the message. [...] Then use the data.
#     text_dict = json.loads(text_decoded)
#     return text_dict

# query_dict = read_message()
# query = query_dict['text']
# #query = "Can Trump declare a national emergency to build a wall?"

# # %% query seach and save to CSV
# csv_file_path = 'consensus_data.csv'
# csv_columns = ['agency', 'title', 'date', 'article', 'link']
# save_to_CSV.initiate_csv(csv_file_path, csv_columns)
# send_message({"name": "response", "text": "initiated CSV file"})

# # NYT:
# url_list, date_list = news_web_scraping.google_NYT_links(query)
# title_list, article_list = news_web_scraping.NYT_links_scrape(url_list)
# if title_list and date_list and article_list and url_list:
#     news_dicList = save_to_CSV.lists_to_dictList('NYT', title_list, date_list, article_list, url_list)
#     save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList) 
# send_message({"name": "response", "text": "written NYT results"})

# # BBC:
# url_list = news_web_scraping.google_BBC_links(query)
# title_list, article_list, date_list = news_web_scraping.BBC_links_scrape(url_list)
# if title_list and date_list and article_list and url_list:
#     news_dicList = save_to_CSV.lists_to_dictList('BBC', title_list, date_list, article_list, url_list)
#     save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList)   
# send_message({"name": "response", "text": "written BBC results"})

# # AP:
# url_list = news_web_scraping.google_AP_links(query)
# title_list, article_list, date_list = news_web_scraping.AP_links_scrape(url_list)
# if title_list and date_list and article_list and url_list:
#     news_dicList = save_to_CSV.lists_to_dictList('AP', title_list, date_list, article_list, url_list)
#     save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList)   
# send_message({"name": "response", "text": "written AP results"})

# # Reuters:
# url_list = news_web_scraping.google_reuters_links(query)
# title_list, article_list, date_list = news_web_scraping.reuters_links_scrape(url_list)
# if title_list and date_list and article_list and url_list:
#     news_dicList = save_to_CSV.lists_to_dictList('Reuters', title_list, date_list, article_list, url_list)
#     save_to_CSV.append_csv(csv_file_path, csv_columns, news_dicList) 
# send_message({"name": "response", "text": "written reuters results"})
    

# # read agency, title, date and url from csv file
# agency_list = []
# titles_list = []
# date_lists = []
# url_list = []
# result_list = []
# with open('consensus_data.csv', mode='r') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     for row in csv_reader:
#         agency_list += [row['agency']] 
#         titles_list += [row['title']] 
#         date_lists += [row['date']]
#         url_list += [row['link']]

# num_Articles = len(titles_list)
# agencies = json.dumps(agency_list)
# titles = json.dumps(titles_list) 
# dates = json.dumps(date_lists)
# urls = json.dumps(url_list)

# result_ops = ["Agree", "Disagree", "discusses", "unrelated"]
# for i in range(num_Articles):
#     result_list += [random.choice(result_ops)]
# results = json.dumps(result_list)



 
# send_message({"name" : "articleNumbers", "text" : "sending numbers of articles", "num_Articles" : str(num_Articles)})
# send_message({"name" : "articleAgencies", "text" : "sending agencies of articles", "agencies" : agencies})
# send_message({"name" : "articleTitles", "text" : "sending titles of articles", "titles" : titles})
# send_message({"name" : "articleDates", "text" : "sending dates of articles", "dates" : dates})
# send_message({"name" : "articleURLs", "text" : "sending urls of articles", "urls" : urls})
# send_message({"name" : "articleResults", "text" : "sending results of articles", "results" : results})


save_to_CSV.format_art_bodies('consensus_data.csv', 'art_bodies.csv', 'statement.csv', 'trump is predudice') # query

# Set file names
file_train_instances = "train_stances.csv"
file_train_bodies = "train_bodies.csv"
file_test_instances = "statement.csv"
file_test_bodies = "art_bodies.csv"
file_predictions = 'predictions_test.csv'

# Initialise hyperparameters
# r = random.Random()
lim_unigram = 5000
target_size = 4
hidden_size = 100

# Load data sets
raw_train = FNCData(file_train_instances, file_train_bodies)
raw_test = FNCData(file_test_instances, file_test_bodies)

# Process data sets
feature_size = 10001
test_set = pipeline_test(raw_train, raw_test, lim_unigram=lim_unigram)

# Define model

# Create placeholders
features_pl = tf.placeholder(tf.float32, [None, feature_size], 'features')
keep_prob_pl = tf.placeholder(tf.float32)

# Infer batch size
batch_size = tf.shape(features_pl)[0]

# Define multi-layer perceptron
hidden_layer = tf.nn.dropout(tf.nn.relu(tf.contrib.layers.linear(features_pl, hidden_size)), keep_prob=keep_prob_pl)
logits_flat = tf.nn.dropout(tf.contrib.layers.linear(hidden_layer, target_size), keep_prob=keep_prob_pl)
logits = tf.reshape(logits_flat, [batch_size, target_size])

# Define prediction
softmaxed_logits = tf.nn.softmax(logits)
predict = tf.arg_max(softmaxed_logits, 1)

# Load model
with tf.Session() as sess:
    load_model(sess)


    # Predict
    test_feed_dict = {features_pl: test_set, keep_prob_pl: 1.0}
    test_pred = sess.run(predict, feed_dict=test_feed_dict)


# Save predictions
save_predictions(test_pred, file_predictions)

print("Done!")