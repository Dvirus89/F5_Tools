import requests
import json
import re

file_path = '/home/ubuntu/attacks/xss/xss_true_output_combined_2.json' 
REGEX_PATTERN=r"Your support ID is- (.*) <br/>" # regex alternative for capture group [A-Z0-9\-]{33}
# Read the JSON data from the external file
with open(file_path, 'r') as file:
    request_data_list = json.load(file)

# Loop through each request option and send the requests
count_allow = 0
count_block = 0
for request_data in request_data_list:
    method = request_data.get("method", "GET")
    url = request_data.get("url", "")
    headers = request_data.get("headers", {})
    data = request_data.get("data", {})

    full_url = f"https://asafdemo-partner.emea-ent.f5demos.com{url}"
    response = ""
    if method == "GET":
        response = requests.get(full_url, headers=headers)
    elif method == "POST":
        response = requests.post(full_url, headers=headers, json=data)
    else:
        print("Unsupported HTTP method")

    matchs = re.findall(REGEX_PATTERN, response.text)
    for match in matchs:
        print (match)
    if matchs.__len__() > 0:
        count_block += 1
    else:
        count_allow += 1
    #print(f"sum, allow={count_allow}, blocked={count_block}")
print(f"sum, allow={count_allow}, blocked={count_block}")
    # Optionally, you can print the response content if needed
    # print(response.content)
