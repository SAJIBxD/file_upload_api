import os
import requests
import sys

def get_arg():
    return input("Enter file path or URL: ")

def verify_file_or_url(arg):
    if os.path.isfile(arg):
        return 'file'
    elif arg.startswith('http://') or arg.startswith('https://'):
        return 'url'
    else:
        return None

def post_to_server(arg, url, url2, data):
    # Assuming 'arg' is a file path
    if verify_file_or_url(arg) == 'file':
        with open(arg, 'rb') as file:
            files = {'files': file}
            response = requests.post(url, files=files, data=data).json()
            #print(response.text)
            if response['status'] == 'success':
                print(response['result']['url'])
            else:
                print("Error: ", response)
    # Assuming 'arg' is a URL
    elif verify_file_or_url(arg) == 'url':
        url = {"url": url}
        data = {**url, **data}
        response = requests.post(url2, data=data).json()
        #print(response.text)
        if response['status'] == 'success':
            print(response['result']['url'])
        else:
            print("Error: ", response)
    else:
        print("Invalid argument.")
  
# Define the API endpoint URL
url = "https://mirrorace.com/api/v1/file/upload"
# Define your API key and token
api_key = "your_api_key"
api_token = "your_api_token"


# Check if an argument is passed
if len(sys.argv) > 1:
    arg = sys.argv[1]
else:
    arg = get_arg()

# Create a session object
session = requests.Session()

# Create the payload containing the API key and token
payload = {"api_key": api_key, "api_token": api_token}

# Send the POST request using the session and parse the response JSON
resp = session.post(url, data=payload).json()

# Check if the response status is "success"
if resp['status'] == 'success':
    upload_key = resp['result']['upload_key']
    cTracker = resp['result']['cTracker']
    server_file = resp['result']['server_file']
    server_remote = resp['result']['server_remote']
    max_mirrors = resp['result']['max_mirrors'] # max mirror allowed to upload
    mirrors = list([k for k, v in resp['result']['mirrors'].items() if v])[:int(max_mirrors)] # create a list of enabled mirror id's with cap based on max_mirrors

    data = {"api_key": api_key, "api_token": api_token, "cTracker": cTracker, "upload_key": upload_key, "mirrors[]": mirrors}
    post_to_server(arg, server_file, server_remote, data=data)
else:
    # Handle the error case
    print("API request unsuccessful.")

# Close the session
session.close()

