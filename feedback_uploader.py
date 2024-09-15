#!/usr/bin/env python3

import os
import requests

feedback_directory = '/data/feedback'
try:
    files = [f for f in os.listdir(feedback_directory) if f.endswith('.txt')]
except FileNotFoundError:
    print(f"Error: The directory {feedback_directory} does not exist.")
    exit(1)
except PermissionError:
    print(f"Error: Permission denied to access {feedback_directory}.")
    exit(1)

feedback_list = []

for file in files:
    file_path = os.path.join(feedback_directory, file)
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            feedback_dict = {
                "title": lines[0].strip(),         
                "name": lines[1].strip(),          
                "date": lines[2].strip(),          
                "feedback": ''.join(lines[3:]).strip()  
            }
            feedback_list.append(feedback_dict)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except IOError:
        print(f"Error: Unable to read file {file_path}.")

url = 'http://35.233.140.102/feedback'  

for feedback in feedback_list:
    try:
        response = requests.post(url, json=feedback)
        if response.status_code == 201:
            print("Feedback posted successfully!")
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except requests.RequestException as e:
        print(f"Request error: {e}")
