import requests
import twitter
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np 

# this is our taggerresponder class. 
class TaggerResponder:

    def __init__(self):
        # load from env variables
        self.api = twitter.Api(consumer_key='-',
                      consumer_secret='-',
                      access_token_key='-',
                      access_token_secret='-')

    def get_latest_handled_mention_id(self):
        # we always write the latest handled id into a file so we know which are the new tweets
        file = "/home/ble/dev/corona-twitter-bot/latest_mention_id.txt"
        with open(file, "r") as f:
            data = f.read()
        return data
        
    def get_mentions(self):
        results = self.api.GetMentions(count=200, since_id=self.get_latest_handled_mention_id())
        return results

    def update_mention_file_id(self, latest_mention_id):
        file = "/home/ble/dev/corona-twitter-bot/latest_mention_id.txt"
        with open(file, "w") as f:
            data = f.write(latest_mention_id)


    def generate_graphs(self, country_code):
        today = datetime.now()
        week_ago = today - timedelta(days = 7)

        country_cases = (requests.get('https://api.covid19api.com/country/' + country_code + '?from=' + week_ago.strftime("%Y-%m-%d") +'T00:00:00Z&to=' + today.strftime("%Y-%m-%d") + 'T00:00:00Z')).json()
        # Day Loop to put all days in an array for the generation
        days = []
        i = 0
        while i < 7:
            days.append((today - timedelta(days = i)).strftime("%d-%m-%y"))
            i += 1

        # Corona Cases Chart
        corona_cases = []
        for res in country_cases:
            corona_cases.append(res["Confirmed"])

        corona_cases_title = ("Confirmed cases in " + country_code + " " + today.strftime("%Y") + " Week: " + today.strftime("%V"))

        fig, ax = plt.subplots(figsize=(12, 10))
        bar = ax.plot(np.flip(days), corona_cases, "o-")
        plt.title(label=corona_cases_title, fontdict={"fontsize": 32})
        plt.xlabel('Date', fontdict={"fontsize": 20})
        plt.ylabel('Confirmed Cases', fontdict={"fontsize": 20})
        plt.grid(color='gray', linestyle='-', linewidth=0.5, aa=True, alpha=0.5)
        plt.savefig(("/home/ble/dev/corona-twitter-bot/new-cases/"+today.strftime("%d-%m-%y")+"-new-cases_" + country_code), optimize=True, orientation='portrait')
        return ("/home/ble/dev/corona-twitter-bot/new-cases/" +today.strftime("%d-%m-%y")+"-new-cases_" + country_code + ".png")


    def respond_to_messages_with_graph(self, mentions):
        for mention in mentions:
            # todo: check if if actually is a valid request or the country code does not exist and so on.
            # we post an update to the users with a graph for their specific country
            country_code = mention.text[-2:]
            status_text = "The current situation in " + country_code
            graph_path_files = self.generate_graphs(country_code)
            with open(graph_path_files, "rb") as image_file:
                image_id1 = self.api.UploadMediaSimple(image_file)

            try: 
                self.api.PostUpdate(status=status_text, auto_populate_reply_metadata=True, in_reply_to_status_id=mention.id, media=image_id1)
                print("Posted Tweet")
            except:
                print("Failed to post Tweet")
                exit()


    def handle_mentions(self):
        mentions = self.get_mentions()
        if mentions:
            self.update_mention_file_id(mentions[0].id_str)
            self.respond_to_messages_with_graph(mentions)
        return mentions


TaggerResponder().handle_mentions()
