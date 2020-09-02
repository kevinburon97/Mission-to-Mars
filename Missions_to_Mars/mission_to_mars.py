from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

#Create an instance of flask
app=Flask(__name__)

#Establish Mongo connection

mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars")

@app.route("/")
def home():
    data = mongo.db.nasa.find_one()
    return  render_template("index.html", data=data)

@app.route("/scrape")
def scraper():
    nasa = mongo.db.nasa
    nasa_data = scrape()
    nasa.update({}, nasa_data, upsert=True)
    return redirect("/")




if __name__ == "__main__":
    app.run(debug=True)