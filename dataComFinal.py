''' 
  this serves as the server currently running on local host
  will recieve parameters from the client (website) when the 
  user presses search and will return back the json in a string
  from the locu api then will query the yelp api to display reviews
  based on what the user clicks
'''
import rauth
import time
import json
from urllib.request import *
import json
from flask import Flask, render_template, jsonify
''' FIX TO ENCODING PROBLEM chcp 65001'''
app = Flask(__name__)
# You will need to obtain your own API key from 
# https://dev.locu.com/
locu_api = 'c4e2a6ec419e82c8432bff3ce3aca9b232695f01'

# renders the client template
@app.route("/", methods=["GET"])
def retreive():
    return render_template('map.html') 

@app.route("/sendMarker/<string:marker>")
def get_results(marker):
  #print(marker)
  marker = marker.split(',')
  params = {}
  params["term"] = marker[0]
  params['location'] = marker[1]
  params['limit'] = 1

  #Obtain these from Yelp's manage access page
  consumer_key = "4b4fYhbrF1iACNoVhJgcUw"
  consumer_secret = "KisZwYHT3ajmwlJ1NQV2KQ2Na4A"
  token = "lMULtSEEwQ3ijnhHSDcqlzLeXod1xQ65"
  token_secret = "OPZ_UG0aYIWrv2Am6WfUBwf-ccg"
  
  session = rauth.OAuth1Session(
    consumer_key = consumer_key
    ,consumer_secret = consumer_secret
    ,access_token = token
    ,access_token_secret = token_secret)
  
  request = session.get("http://api.yelp.com/v2/search/?",params=params)
  
  #Transforms the JSON API response into a Python dictionary
  data = ""
  try:
    data = request.json()
  except:
    pass

  try:
    session.close()
  except:
    pass
  
  return json.dumps(data)

@app.route("/sendRequest/<string:query>")
def locu_search(query):
  final_url = 'https://api.locu.com/v1_0/venue/search/?'
  query = query.split(',')
  print(query)
  if query[0] == "using latlong":
    latitude = query[1]
    longitude = query[2]
    final_url += 'location=' + latitude + "%2C" + longitude + '&' + 'radius=2000' + '&'
  if query[0] != "" and query[0] != "using latlong":
    locality = query[0].replace(' ','%20')
    final_url += 'locality=' + locality + '&'
  if query[1] != "" and query[0] != "using latlong":
    region = query[1].replace(' ','%20')
    final_url += 'region=' + region + '&'
  if query[2] != "" and query[0] != "using latlong":
    postal_code = query[2].replace(' ','%20')
    final_url += 'postal_code=' + postal_code + '&'
  
  final_url += 'api_key=' +locu_api
  print("Final url")
  print(final_url)
  response = urlopen(final_url).read().decode("utf-8")

  #data = json.loads(response) 
  # will return a string of json to the javascript (client side)
  return response

if __name__ ==  "__main__":
  app.run()




  