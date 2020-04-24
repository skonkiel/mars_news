from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

# Display locally stored data when page is first loaded
@app.route("/")
def index():
    # Pull data from mongodb
    mars = mongo.db.mars.find_one()
    # display data on page
    return render_template("index.html", mars=mars)

# Scrape fresh data when button is pushed on index.html
@app.route("/scrape")
def scraper():
    # set up mongo table
    mars = mongo.db.mars
    # call scrape function
    mars_data = scrape_mars.scrape()
    # update table using returned data
    mars.update({}, mars_data, upsert=True) # Try upsert=True if error
    # redirect to homepage (to display the data)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)