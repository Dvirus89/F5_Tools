import requests
import urllib3
import os
import json
import re
import uuid


### Written by Asaf Sahar ###

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BLOCK_RESPONSE_REGEX_PATTERN=r"Your support ID is: (.*)<br><br>" 
TARGET_ENDPOINT="https://asafdemo-partner.emea-ent.f5demos.com"
BASE_PATH = "attacks_uuid/"
TOP_COLUMN="Platform, Attack File Path, Seq, Request Allowed, Request Blocked, Is Attack, Support ID (if exists)\n"
ENTRY_COLUMN="{platform}, {attack_file_path}, {seq}, {allowed}, {blocked}, {isattack}, {supportid}\n"
OUTPUT_PATH = "report.csv"
PLATFORM="BIGIP"

def write_file(path, content):
        with open(path, 'a', encoding='utf-8') as f:
                    f.write(content)

for attack_vector_dir in os.listdir(BASE_PATH):
    if os.path.isdir(f"{BASE_PATH}{attack_vector_dir}/"):
        print(f"Proccesing attack vector: {attack_vector_dir}...")
        for attack_file in os.listdir(f"{BASE_PATH}{attack_vector_dir}/"):
            if attack_file != ".DS_Store":
                attack_file_path = f"{BASE_PATH}{attack_vector_dir}/{attack_file}"
                uuid_attack_file_path = f"{BASE_PATH}{attack_vector_dir}/uuid_{attack_file}" 
                print(f"\tProccesing attack file: {attack_file_path}...")
                # Read the JSON data from the external file
                with open(attack_file_path, 'r') as file:
                    request_data_list = json.load(file)

                # Loop through each request and append uuid
                count_allow = 0
                count_block = 0
                count_missed = 0
                new_json = []
                for request_data in request_data_list:                
                    myuuid = uuid.uuid4()
                    entry = {"attack_uuid": f"{myuuid}"}
                    request_data['headers'].update(entry)
                    
                    
                with open(uuid_attack_file_path, 'w') as outfile:
                    json.dump(request_data_list, outfile)
            