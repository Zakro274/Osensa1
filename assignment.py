# Write a python command line program to calculate average of air pollutant PM2.5 over n minutes, of
# all the stations map bound by two pairs of latitudes and longitudes.
from pathlib import Path
import json
import requests
import subprocess


def average(nums):
    answer = 0
    for num in nums:
       answer+=num
    answer = answer/len(nums)
    return answer 

token = "320edac1beca49aea1e664d88757621c74923024"
stations = []
pm5_recorder = []
min_sum = 0

# User Interaction

latitude_1 = "39"  # input("Insert first latitude: ")
latitude_2 = "116"  # input("Insert second latitude: ")

longitude_1 = "40"  # input("Insert first longitude: ")
longitude_2 = "117"  # input("Insert second longitude: ")

# Requesting all stations in a given latitude-longitud
request = requests.get(url="https://api.waqi.info/v2/map/bounds?latlng="+latitude_1+','+longitude_1 +
                       ','+latitude_2+','+longitude_2+"&networks=all&token=320edac1beca49aea1e664d88757621c74923024")

f_request = request.json()

for i in range(len(f_request["data"])):
    stations.append(f_request["data"][i]["station"]["name"])

# Now in the stations array we have all stations in the given area. So, let's find the pm5 on each station

for i in stations:
    try:
        request = requests.get(url = "https://api.waqi.info/feed/"+i+"/?token=320edac1beca49aea1e664d88757621c74923024")
        J_request = request.json()
        value = J_request["data"]["iaqi"]["pm25"]["v"]
        pm5_recorder.append(value)
    except TypeError:
        pm5_recorder.append(0)
    except KeyError:
        pm5_recorder.append(0)
        

for i in range(len(stations)):
    print("Station: " + stations[i])
    print("PM25: " + str(pm5_recorder[i]))
    print()
    
luisa = average(pm5_recorder)
print("Global average: "+ str(luisa))
    
