from pymongo import MongoClient
import json

def main():
    client = MongoClient('localhost', 27017)
    db = client['project1']


