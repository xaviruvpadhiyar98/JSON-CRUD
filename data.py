"""Routines associated with the application data.
"""
import json

courses = {}

def load_data():
    with open('json/course.json') as f:
        return json.load(f)

def save_data(json_data):
    with open('json\course.json', 'w') as f:
        json.dump(json_data, f, indent=4)

if __name__ == '__main__':
    print(load_data())