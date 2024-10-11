# import time
# import requests
from dotenv import load_dotenv
import os
import time
import json

from Utils.Utils import DataSaver
from APIClient.APIClient import HTTPClientSync
from Graphics.PrintMap import print_map, generate_random_array, draw_array

from Parser.Parser import Parser

load_dotenv()
TOKEN: str = '67082a9c3378967082a9c3378c'
BASE_URL_TEST: str = 'https://games-test.datsteam.dev/'
BASE_URL_OSN: str = 'https://games.datsteam.dev/'
headers: dict = {"X-Auth-Token" : TOKEN}



def main():
    start_time = time.time()
    client: HTTPClientSync = HTTPClientSync(BASE_URL_TEST)
    get_data = client.get(headers=headers)
    saver = DataSaver()
    saver.create_output_folder()
    saver.save_to_file('test1', get_data)
    post_data = client.post(headers=headers)
    saver.save_to_file('post', post_data)
    print_map()
    
    
def test():
    with open('./buf/session_2024-10-11_21-01-45/post', 'r') as f:
        obj = Parser(json.load(f))
        # print((obj.parse_constants()))
        print(list(obj.parse_wanted_list()))

if __name__ == "__main__":
    # main() # расскоментировать при начале работы
    test()