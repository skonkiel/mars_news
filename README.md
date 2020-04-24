# Mars News

## Project background

This application includes scraped data from a series of websites, stored locally in a MongoDB database, then repurposed
into a webpage that contains facts and images about Mars.

This Flask app uses splinter (Selenium), MongoDB, Beautiful Soup and Pandas. It was designed using Bootstrap.

## What's in this repo

* A Jupyter notebook, including Python code to scrape the data and store it in a MongoDB database
* `scrape_mars.py`, containing the executable code for use in the Flask app
* A Flask app that powers a webpage to display the data
* A `templates` folder that contains the webpage
