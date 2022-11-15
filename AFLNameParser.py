"""
Strip out player names from a fryzigg player data csv and save to a file
"""

import pandas

INPUTFILE = "data/rawAFLSeasonData.csv"
OUTPUTFILE = "data/player_names.txt"

seasonData = pandas.read_csv(INPUTFILE)
playerNames = seasonData[["player_id","player_first_name","player_last_name"]].drop_duplicates()

with open(OUTPUTFILE,"w") as PLAYER_FILE:
    outStr = ""
    for index,row in playerNames.iterrows():
        id = row["player_id"]
        fname = row["player_first_name"]
        lname = row["player_last_name"]

        outStr += f"{id}\t{fname}\t{lname}\n"

    PLAYER_FILE.write(outStr)        

    PLAYER_FILE.close()