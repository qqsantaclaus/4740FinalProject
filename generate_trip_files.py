import csv
from datetime import datetime

weather={}
with open('./data/weather.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    weather_fieldnames = next(reader)
    weather_fieldnames.extend(["is_weekday"])
    for row in reader:
        date_obj = datetime.strptime(row[0], "%m/%d/%Y")
        weather[row[0]]=row
        if (date_obj.weekday()<=4):
            weather[row[0]].extend([1])
        else:
            weather[row[0]].extend([0])

print(len(weather.keys()))

trips_dict={}
with open('./data/trip.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if (row["start_date"] and row["start_station_id"] and row["end_date"] and row["end_station_id"]):
            start_date_obj = datetime.strptime(row["start_date"], '%m/%d/%Y %H:%M')
            start_date_str = start_date_obj.strftime("%#m/%#d/%Y")
            if (not (row["start_station_id"], row["end_station_id"]) in trips_dict):
                trips_dict[(row["start_station_id"], row["end_station_id"])] = {}
                trips_dict[(row["start_station_id"], row["end_station_id"])]["total"] = 0
                for w in weather.keys():
                    trips_dict[(row["start_station_id"], row["end_station_id"])][w] = 0
            if (not (row["end_station_id"], row["start_station_id"]) in trips_dict):
                trips_dict[(row["end_station_id"], row["start_station_id"])] = {}
                trips_dict[(row["end_station_id"], row["start_station_id"])]["total"] = 0
                for w in weather.keys():
                    trips_dict[(row["end_station_id"], row["start_station_id"])][w] = 0
            if (not start_date_str in weather.keys()):
                print(start_date_str)
            else:
                trips_dict[(row["start_station_id"], row["end_station_id"])][start_date_str] = trips_dict[(row["start_station_id"], row["end_station_id"])][start_date_str] + 1
                trips_dict[(row["start_station_id"], row["end_station_id"])]["total"] = trips_dict[(row["start_station_id"], row["end_station_id"])]["total"] + 1


trips_sorted_indices = sorted(trips_dict.keys(), key=lambda x: trips_dict[x]['total']+trips_dict[tuple(reversed(x))]['total'])
trips_sorted_indices.reverse()
print(trips_sorted_indices[:20])
print([trips_dict[i]["total"] for i in trips_sorted_indices[:20]])

# Observations:
# Flows are unbalanced inside a pair of stations
# Topic pairs that we might want to pick:
# ('65', '69'), ('60', '50'), ('50', '61'), ('60', '74')

key_station_pairs = [('65', '69'), ('60', '50'), ('50', '61'), ('60', '74')]


# print(trips_dict)

# write to csvs per pair of stations
for spair in key_station_pairs:
    for i in range(2):
        fname = spair[0]+"_to_"+spair[1]+"_by_date"+".csv"
        with open("./data/"+fname, "w") as output:
            fieldnames=["start_station_id", "end_station_id", "num_trips"]
            fieldnames.extend(weather_fieldnames)
            writer = csv.writer(output)
            writer.writerow(fieldnames)
            for cur_date in weather.keys():
                temp = [spair[0], spair[1], trips_dict[spair][cur_date]]
                temp.extend(weather[cur_date])
                writer.writerow(temp)
        spair = tuple(reversed(spair))
    fname = spair[0]+"_"+spair[1]+"_aggregated_by_date.csv"
    with open("./data/"+fname, "w") as output:
        fieldnames=["station_id_1", "station_id_2", "num_trips"]
        fieldnames.extend(weather_fieldnames)
        writer = csv.writer(output)
        writer.writerow(fieldnames)
        for cur_date in weather.keys():
            temp = [spair[0], spair[1], trips_dict[spair][cur_date]+trips_dict[tuple(reversed(spair))][cur_date] ]
            temp.extend(weather[cur_date])
            writer.writerow(temp)
