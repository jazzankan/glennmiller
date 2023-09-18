import main
from bs4 import BeautifulSoup
import requests
import time
import json


month_index = main.glenn_page.index(main.latest_month)
latest_content = main.glenn_page[month_index:]
latest_soup = BeautifulSoup(latest_content, "html.parser")

artist_elements = latest_soup.find_all("p", class_="artist")
artists = []
for element in artist_elements:
    art = element.getText()
    art = art.replace('\xa0', ' ')
    artists.append(art)

date_elements = latest_soup.find_all("p", class_="date")
dates = []
for element in date_elements:
    dt = element.getText()
    dates.append(dt)
concert_list = []
if len(artists) > 0 and len(artists) == len(dates):
   for e in range(len(artists)):
        dict = {'names': artists[e], 'date': dates[e]}
        concert_list.append(dict)
else:
    print("Finns inga konserter eller antalet stämmer inte med datumkolumnen!")

for concert in concert_list:
    print(f"{concert['names']}\n{concert['date']}\n----------")

print("Mata in posterna, j/n:")
ok = input()
if ok == "j":
    #localhost
    #JAZZTIDER_ENDPOINT = 'http://localhost/api/v1/events'
    #prod
    JAZZTIDER_ENDPOINT = 'https://jazztider.webbsallad.se/api/v1/events'
    #localhost
    #ACCESS_TOKEN = '1|SxKxNcVRebSKIVS2QEwhObEM6rcInw3OqspKzYqj'
    #prod
    ACCESS_TOKEN = '1|M1HhUxZzpiucZIBrh319xOPspjwbekTPceQpMg1f'

    headers = {
        "Accept": 'application/json',
        "Content-Type": 'application/json',
        "Authorization": f"Bearer {ACCESS_TOKEN}"
        }

    for concert in concert_list:
        event_params = {
            "name": concert["names"],
            "place_id": 1,
            #"organizer_id": 1,
            "organizer_id": 32,
            "day": concert["date"],
            "timeofday": "20.00",
            "link": "https://www.glennmillercafe.se/konserter"
        }
        response = requests.post(url=JAZZTIDER_ENDPOINT, json=event_params, headers=headers)
        resp_dict = json.loads(response.text)
        try:
            print(resp_dict["status"])
        except:
            print(response.text)
        time.sleep(1)






