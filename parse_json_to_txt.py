import pandas as pd
import re
import json

json_df = pd.read_json("./planet_booty_songs.json")
filter_words = ["verse 1", "verse 2", "verse 3", "verse 4", "verse 5", "chorus", "intro", "outro", "bridge", "refrain", "pre chorus", ""]


# print(json_df)
counter = 0
for index,row in json_df.iterrows():
    song = row[0]
    counter += 1
    # print(index, song['name'], song['lyrics'])

    for line in song['lyrics'].split('\n'):
        line = line.replace(u"\u2018", "'").replace(u"\u2019", "'").strip().lstrip()
        line = re.sub('\W+',' ', line)
        line = line.lower().strip()
        if line not in filter_words:
            print(line)

