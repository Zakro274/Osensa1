# Write a python command line program to calculate average of air pollutant PM2.5 over n minutes, of
# all the stations map bound by two pairs of latitudes and longitudes.
from pathlib import Path
import json
import requests
import subprocess
import time


token = "320edac1beca49aea1e664d88757621c74923024"


def average(nums):
    answer = 0
    for num in nums:
        answer += num
    answer = answer/len(nums)
    return answer


def find_stations(request):
    stations = []
    f_request = request.json()
    for i in range(len(f_request["data"])):
        stations.append(f_request["data"][i]["station"]["name"])
    return stations


def find_pm25(name):
    try:
        request = requests.get(url="https://api.waqi.info/feed/" +
                               name+"/?token=320edac1beca49aea1e664d88757621c74923024")
        J_request = request.json()
        value = J_request["data"]["iaqi"]["pm25"]["v"]
        pm5_recorder = value
    except TypeError:
        pm5_recorder = 0
    except KeyError:
        pm5_recorder = 0
    finally:
        return pm5_recorder


def sum_arrays(list1, list2):
    answer = []
    
    if(len(list1) == 0):
        answer = list2
        return answer
    
    for i in range(len(list1)):
        answer.append(list1[i] + list2[i])
    return answer


def divide_array(nums, divisor):
    for i in range(len(nums)):
        nums[i] = nums[i]/divisor
    return nums


def sampling(latitude_1, longitude_1, latitude_2, longitude_2, period=5, rate=1):
    request = requests.get(url="https://api.waqi.info/v2/map/bounds?latlng="+latitude_1+','+longitude_1 +
                           ','+latitude_2+','+longitude_2+"&networks=all&token=320edac1beca49aea1e664d88757621c74923024")
    stations = find_stations(request)

    quantity = period / rate

    previous = []

    for i in range(int(quantity)):
        now = []
        for station in stations:
            now.append(find_pm25(station))
        previous = sum_arrays(previous, now)
        if(i >= quantity -1):
            pass
        else:
            time.sleep(quantity*60)

    previous = divide_array(previous, quantity)
    return previous

# User Interaction

latitude_1 = "39"  # input("Insert first latitude: ")
latitude_2 = "116"  # input("Insert second latitude: ")

longitude_1 = "40"  # input("Insert first longitude: ")
longitude_2 = "117"  # input("Insert second longitude: ")

# Requesting all stations in a given latitude-longitud
request = requests.get(url="https://api.waqi.info/v2/map/bounds?latlng="+latitude_1+','+longitude_1 +
                       ','+latitude_2+','+longitude_2+"&networks=all&token=320edac1beca49aea1e664d88757621c74923024")

stations = find_stations(request)

Myarray = sampling(latitude_1, longitude_1, latitude_2, longitude_2, 1, 1)

for i in range(len(stations)):
    print("Station: " + stations[i])
    print("PM25: " + str(Myarray[i]))
    print()

luisa = average(Myarray)
print("Global average: " + str(luisa))
