from flask import Flask, render_template, request
from selenium import webdriver
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

data = {'Elon Musk':'https://opensky-network.org/aircraft-profile?icao24=a835af',
        'Roman Abramovich':'https://opensky-network.org/aircraft-profile?icao24=4844a1',
        'Putin':'https://opensky-network.org/aircraft-profile?icao24=157716',
        'Buhari':'https://opensky-network.org/aircraft-profile?icao24=064051'}

keys = data.keys()

@app.route('/')
def index():
    options = []
    for i, key in enumerate(keys):
        options.append({'value': i, 'name': key})
    return render_template('index.html', options=options)

@app.route('/scrape', methods=['POST'])
def scrape():
    driver = webdriver.Chrome()
    choice = int(request.form['options'])
    key = list(keys)[choice]
    driver.get(data[key])
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    flight_data = soup.select(".col-xs-12.even.apFlightRow")
    driver.quit()
    return render_template('scrape.html', key=key, flight_data=flight_data)

if __name__ == '__main__':
    app.run(debug=True)
