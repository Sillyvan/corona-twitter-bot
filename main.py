import requests
import twitter
from datetime import datetime, timedelta 
from pprint import pprint
import os
import matplotlib.pyplot as plt
import numpy as np 

# Github Links
#https://github.com/bear/python-twitter/

# Date 
today = datetime.now()
week_ago = today - timedelta(days = 7)


# Fetch Corona Data
ww = requests.get('https://api.covid19api.com/world?from=' + week_ago.strftime("%Y-%m-%d") +'T00:00:00Z&to=' + today.strftime("%Y-%m-%d") + 'T00:00:00Z')
worldWideCases = ww.json()

# Twitter Auth
# load from env variables
api = twitter.Api(consumer_key='-',
                      consumer_secret='-',
                      access_token_key='-',
                      access_token_secret='-')


# Day Loop for Chart generation
days = []
i = 0
while i < 7:
  days.append((today - timedelta(days = i)).strftime("%d-%m-%y"))
  i += 1

# Corona Cases Chart
corona_cases = []
for res in worldWideCases:
    corona_cases.append(res["NewConfirmed"])

corona_cases_title = ("New Corona Cases " + today.strftime("%Y") + " Week: " + today.strftime("%V"))


fig, ax = plt.subplots(figsize=(12, 10))
bar = ax.plot(np.flip(days), corona_cases, "o-")
ax.set_ylim(ymin=(corona_cases[-1] * 0.7), ymax=(corona_cases[-1] * 1.3))
plt.title(label=corona_cases_title, fontdict={"fontsize": 32})
plt.xlabel('Date', fontdict={"fontsize": 20})
plt.ylabel('New Cases', fontdict={"fontsize": 20})
plt.grid(color='gray', linestyle='-', linewidth=0.5, aa=True, alpha=0.5)
plt.savefig(("/home/ble/dev/corona-twitter-bot/new-cases/"+today.strftime("%d-%m-%y")+"-new-cases"), optimize=True, orientation='portrait')


# Corona Death Chart
corona_deaths = []
for res in worldWideCases:
    corona_deaths.append(res["NewDeaths"])

corona_deaths_title = ("New Corona Deaths " + today.strftime("%Y") + " Week: " + today.strftime("%V"))


fig2, ax2 = plt.subplots(figsize=(12, 10))
bar2 = ax2.plot(np.flip(days), corona_deaths, "o-")
ax2.set_ylim(ymin=0, ymax=(corona_deaths[-1] * 2))
plt.title(label=corona_deaths_title, fontdict={"fontsize": 32})
plt.xlabel('Date', fontdict={"fontsize": 20})
plt.ylabel('New Deaths', fontdict={"fontsize": 20})
plt.grid(color='gray', linestyle='-', linewidth=0.5, aa=True, alpha=0.5)
plt.savefig(("/home/ble/dev/corona-twitter-bot/new-deaths/"+today.strftime("%d-%m-%y")+"-new-deaths"), optimize=True, orientation='portrait')


# Post Tweet
img1 = ("/home/ble/dev/corona-twitter-bot/new-cases/" +today.strftime("%d-%m-%y")+"-new-cases.png" )
img2 = ("/home/ble/dev/corona-twitter-bot/new-deaths/" +today.strftime("%d-%m-%y")+"-new-deaths.png" )

text = "❗ Daily Corona Report ❗\n\n🌐 New Cases Today: "+str(worldWideCases[-1]["NewConfirmed"])+"\n💀 New Deaths Today: " +str(worldWideCases[-1]["NewDeaths"])+"\n🩹 New Recoveries Today: "+ str(worldWideCases[-1]["NewRecovered"])

with open(img1, "rb") as image_file:
    image_id1 = api.UploadMediaSimple(image_file)

with open(img2, "rb") as image_file:
    image_id2 = api.UploadMediaSimple(image_file)

    try: 
        api.PostUpdate(text, media=[image_id1, image_id2])
        print("Posted Tweet")
    except:
        print("Failed to post Tweet")
        exit()



# Update Profile
api.UpdateProfile(
    name="CoronaStatusBot 🌎 (" + str(corona_cases[-1]) +" New Cases)",
    description=(
    "🌐 Total Cases: " + str(worldWideCases[-1]["TotalConfirmed"]) + 
    "\n\n💀 Total Deaths: "+ str(worldWideCases[-1]["TotalDeaths"]) + 
    "\n\n🩹 Total Recovered: " + str(worldWideCases[-1]["TotalRecovered"]
    ))
    )

