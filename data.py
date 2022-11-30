import json

with open('data.json', 'r') as f:
  data = json.load(f)

def get_credentials():
  return [data['Username'],data['Email'],data['Password'],data['Unique Id']]

def get_Theme():
  return data['Theme']