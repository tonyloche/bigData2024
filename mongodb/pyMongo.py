#make sure to use pip install pymongo
from pymongo import MongoClient
import json

def main():

    #connecting to database
    client = MongoClient()
    db = client.get_database("myfirstdb")
    collection_movies = db.movies

    #quering movies collection
    movies = collection_movies.find()
    for movie in movies:
        print(movie)

    #load in json
    with open("orders.json") as f:
        orders_data = json.load(f)
    print(orders_data)

    #insert json data to database
    # db.orders.insert_many(orders_data)
    # all_orders = db.orders.find()
    # for order in all_orders:
    #     print(order)

    with open("employees.json") as e:
        employees_data = json.load(e)
    print(employees_data)

    #insert employees data to database
    # db.employees.insert_many(employees_data)

    #aggregate mongo commands:
    #db.orders.aggregate([{$group: {_id: "$customerName", totalAmount: {$sum: "$amount"}}}])
    #db.order.aggregate([{$group: {_id: null, average_spent: {$avg: "a$amount"}}}])
    


if __name__ == '__main__':
    main()