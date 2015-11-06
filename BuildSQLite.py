import sqlite3
import os
import json
import datetime
import multiprocessing as mp


def parseJson(args):
    """
    Function that parses a given json file for kill information.

    Inputs:

        jsonFileRoot    The parent directory of the json file. This file should 
                        come from the zkill database dump released by Squizz or 
                        at least formatted in the same manner.

        jsonFileName    The name of the json file to be parsed.

        sqliteFilePath  The filepath to the sqlite database that data should be
                        written to.

        queue           This is the queue that will be checked to monitor the
                        progress of the operation.
    """

    jsonFileRoot, jsonFileName, sqliteFilePath = args

    # Check if we have a json file

    if jsonFileName.endswith(".json"):

        # Connect to the database

        conn = sqlite3.connect(
            sqliteFilePath, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()

        # Open and read in our json file

        jsonFile = open(os.path.join(jsonFileRoot, jsonFileName), "rb")
        data = json.load(jsonFile)
        jsonFile.close()

        if data:

            # Get a list of the killIDs

            killIDList = data.keys()

            for i in range(0, len(killIDList)):

                # Iterate through the killIDs for this file

                killID = int(killIDList[i])

                # Build the killTime

                year = int(data[killIDList[i]]['killTime'][0:4])
                month = int(data[killIDList[i]]['killTime'][5:7])
                day = int(data[killIDList[i]]['killTime'][8:10])
                hour = int(data[killIDList[i]]['killTime'][11:13])
                minute = int(data[killIDList[i]]['killTime'][14:16])
                second = int(data[killIDList[i]]['killTime'][17:19])

                killTime = datetime.datetime(
                    year=year, month=month, day=day, hour=hour, minute=minute, second=second)

                # Get the Solar System name

                solarSystem = str(data[killIDList[i]]['solarSystem']['name'])

                # Get the number of attackers

                numAttackers = int(data[killIDList[i]]['attackerCount'])

                # Get the damage taken

                damageTaken = int(data[killIDList[i]]['victim']['damageTaken'])

                # Get victim name

                if 'character' in data[killIDList[i]]['victim'].keys():

                    victimName = data[killIDList[i]][
                        'victim']['character']['name']

                else:

                    victimName = "None"

                # Get victim shipID

                victimShipID = int(
                    data[killIDList[i]]['victim']['shipType']['id'])

                # Get victim shipName

                victimShipName = data[killIDList[i]][
                    'victim']['shipType']['name']

                # Get victimCorpName

                victimCorpName = data[killIDList[i]][
                    'victim']['corporation']['name']

                # Get victimAllianceName

                if 'alliance' in data[killIDList[i]]['victim'].keys():

                    victimAllianceName = data[killIDList[i]][
                        'victim']['alliance']['name']

                else:

                    victimAllianceName = "None"

                # Search list of attackers to find the one that did the final
                # blow

                attackers = data[killIDList[i]]['attackers']

                for j in range(0, len(attackers)):

                    if data[killIDList[i]]['attackers'][j]['finalBlow']:
                        
                        if 'shipType' in data[killIDList[i]]['attackers'][j]:

                            killerShipType = data[killIDList[i]][
                                'attackers'][j]['shipType']['id']
                            killerShipName = data[killIDList[i]][
                                'attackers'][j]['shipType']['name']
                                
                        else:
                            
                            killerShipType = "None"
                            killerShipName = "None"

                # Write info to the database

                c.execute("INSERT OR IGNORE INTO KillInformation (" +
                          "killID, " +
                          "killTime, " +
                          "solarSystem, " +
                          "numAttackers, " +
                          "damageTaken, " +
                          "killerShipType, " +
                          "killerShipName, " +
                          "victimName, " +
                          "victimShipID, " +
                          "victimShipName, " +
                          "victimCorpName, " +
                          "victimAllianceName)" +
                          "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (killID, killTime, solarSystem, numAttackers, damageTaken, killerShipType, killerShipName, victimName, victimShipID, victimShipName, victimCorpName, victimAllianceName))

            conn.commit()

        conn.close()

if __name__ == '__main__':

    # Directory containing the sqlite database or where it should be placed

    destPathName = '/media/sf_D_DRIVE/zkb-Killmails/'
    dbName = 'zkb-killmails.sqlite'
    dbPath = os.path.join(destPathName, dbName)

    # Directory containing all the unpacked .json File
    # For my filesystem, this is the same as above

    jsonPathName = '/media/sf_D_DRIVE/zkb-Killmails/'

    # Connect or create our database

    conn = sqlite3.connect(
        destPathName + dbName, detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()

    # Check to see if the table already exists

    c.execute(
        "SELECT * FROM sqlite_master WHERE name = 'KillInformation' and type = 'table';")
    tableExists = c.fetchall()

    # Create the table if it isn't there

    if not tableExists:

        c.execute("CREATE TABLE KillInformation(" +
                  "killID INTEGER PRIMARY KEY, " +
                  "killTime, " +
                  "solarSystem TEXT, " +
                  "numAttackers INTEGER, " +
                  "damageTaken INTEGER, " +
                  "killerShipType INTEGER, " +
                  "killerShipName TEXT, " +
                  "victimName TEXT, " +
                  "victimShipID INTEGER, " +
                  "victimShipName TEXT, " +
                  "victimCorpName TEXT, " +
                  "VictimAllianceName TEXT);")

        conn.commit()

    conn.close

    startTime = datetime.datetime.now()

    for root, dirs, files in os.walk(jsonPathName):

        workers = mp.Pool()

        # Construct the arguments for the function call

        args = [(root, name, dbPath) for name in files]

        # Call our pool workers to get them started

        result = workers.map(parseJson, args)

    endTime = datetime.datetime.now()
    elapsed = endTime - startTime

    print str(int(round(elapsed.total_seconds()))) + " seconds elapsed"
