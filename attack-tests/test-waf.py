import requests
import urllib3
import os
import json
import re


### Written by Asaf Sahar ###

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BLOCK_RESPONSE_REGEX_PATTERN=r"Your support ID is- (.*) <br/>" 
TARGET_ENDPOINT="https://asafdemo-partner.emea-ent.f5demos.com"
TOP_COLUMN="Platform, Attack File Path, Request Allowed, Request Blocked, Support ID (if exists)\n"
ENTRY_COLUMN="{platform}, {attack_file_path}, {allowed}, {blocked}, {supportid}\n"
OUTPUT_PATH = "report.csv"
PLATFORM="BIGIP"

def write_file(path, content):
        with open(path, 'a', encoding='utf-8') as f:
                    f.write(content)

write_file(OUTPUT_PATH, TOP_COLUMN)
for attack_vector_dir in os.listdir('attacks/'):
    print(f"Proccesing attack vector: {attack_vector_dir}...")
    for attack_file in os.listdir(f"attacks/{attack_vector_dir}/"):
        attack_file_path = f"attacks/{attack_vector_dir}/{attack_file}" 
        print(f"\tProccesing attack file: {attack_file_path}...")
        # Read the JSON data from the external file
        with open(attack_file_path, 'r') as file:
            request_data_list = json.load(file)

        # Loop through each request option and send the requests
        count_allow = 0
        count_block = 0
        for request_data in request_data_list:
            method = request_data.get("method", "GET")
            url = request_data.get("url", "")
            headers = request_data.get("headers", {})
            data = request_data.get("data", {})
            print(f"\t\tProccesing attack #{str(count_allow+count_block)}...")

            full_url = f"{TARGET_ENDPOINT}{url}"
            response = ""
            if method == "GET":
                response = requests.get(full_url, headers=headers, verify=False)
            elif method == "POST":
                response = requests.post(full_url, headers=headers, json=data, verify=False)
            else:
                print("Unsupported HTTP method")

            matchs = re.findall(BLOCK_RESPONSE_REGEX_PATTERN, response.text)
            for match in matchs:
                print (match)
            if matchs.__len__() > 0:
                count_block += 1
                print("\t\t\tblocked")
                write_file(OUTPUT_PATH, ENTRY_COLUMN.format(platform=PLATFORM, attack_file_path=attack_file_path, allowed="no", blocked="yes", supportid=match)) 
            else:
                count_allow += 1
                print("\t\t\tpassed")
                write_file(OUTPUT_PATH, ENTRY_COLUMN.format(platform=PLATFORM, attack_file_path=attack_file_path, allowed="yes", blocked="no", supportid="0")) 
    print(f"summary for {attack_file}: allow={count_allow}, blocked={count_block}")
