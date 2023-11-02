# map for zabastcom.org by @whitewind101

import requests_cache
import requests
import json
import time

# cache requests to zabastcom API
requests_cache.install_cache()

# start a map "m"
import folium
import folium.plugins
map_z = folium.Map(
    location=(54.84186965821643, 83.11286485356726),
    #tiles="cartodb positron",
    tiles=r"https://{s}.tile.jawg.io/jawg-matrix/{z}/{x}/{y}{r}.png?access-token=vuIWGdUqkrF2HyhMBi2MFxaFSmtFMnc07cMWAv7LPjDpP99cKo8hPuBl7qV3Hpgq",
    attr=r"<a href=\"https://www.jawg.io?utm_medium=map&utm_source=attribution\" target=\"_blank\">&copy; Jawg</a> - <a href=\"https://www.openstreetmap.org?utm_medium=map-attribution&utm_source=jawg\" target=\"_blank\">&copy; OpenStreetMap</a>&nbsp;contributors",
    control_scale=True,
    zoom_control=False,
    zoom_start=2)
folium.plugins.Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
).add_to(map_z)


# collect data from zabastcom API in "responses"
responses = []
LINK = 'https://zabastcom.org/api/v2/all/events'
page = 1
total_pages = 5
# this is just a dummy number so the loop starts

while page <= total_pages:

    # print some output so we can see the status
    print("Requesting page {}/{}".format(page, total_pages)," ", end="")


    # make the API call
    response = requests.get(LINK, params={'page': page, 'perPage': 10, 'sort.field': 'createdAt', 'sort.order': 'desc'})


    # if we get an error, print the response and halt the loop
    if response.status_code != 200:
        print(response.text)
        break

    # extract pagination info
    page = int(response.json()['meta']['currentPage'])
    # total_pages = int(response.json()['meta']["total"]) #updating "total_pages' to actual number

    # append response
    responses.append(response)


    # adding markers on map_z
    r = response.json()["data"]
    for conf in r:
        folium.Marker(
            location=[conf["latitude"], conf["longitude"]],
            tooltip=conf["titleRu"],
            popup=conf["contentRu"],
            icon=folium.Icon(color="red"),
        ).add_to(map_z)



    # if it's not a cached result, sleep
    if not getattr(response, 'from_cache', False):
        time.sleep(0.25)
        print("req-sleep")
    if getattr(response, 'from_cache', False):
        print("cache")
    # increment the page number
    page += 1

    # print(json.loads(response.text))

    #pause requests
    #input()

# with open("zab_dump.json", "w", encoding="utf-8") as f:
#     json.dump(responses, f, indent=4)
#     print("saved in file")
#
#print(responses)

# responses to DataFrame import
# import pandas as pd
#
# frames = [pd.DataFrame(r.json()['data']) for r in responses]
# confl = pd.concat(frames)

# confl = confl.drop('titleRu', axis=1)
# confl.head()
#
# print data statistic
#print(confl.describe())

# print data info
#print(confl.info())
# confl.describe()
#tags = [t['name'] for t in r.json()['toptags']['tag'][:3]]


# save result
map_z.save('map_zabastcom.html')