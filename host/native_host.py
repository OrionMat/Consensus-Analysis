import sys
import json
import struct


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

test = {"name": "response1", "text": "Hello, Orion's extension."}

read_dict = read_message()
send_message(test)

file_obj = open("check.txt ", 'a')
file_obj.write("hello all worlds\n")
file_obj.write(str(read_dict))
file_obj.write("\n")