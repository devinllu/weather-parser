import pandas as pd
import pprint
import re
# find daily max temp, store in col
# split per month, by per station
# 


def get_station_number(s):
    return s[0:7]

def generate_files_by_station(filename='big.txt'):

    df = pd.read_csv(filename, header=None)
    stations = {}

    for _, row in df.iterrows():
        str_row = row[0]
        station = get_station_number(str_row)


        if station not in stations.keys():
            stations[station] = [str_row]
        else:
            stations[station].append(str_row)

    # write_to_file(stations)
    print(len(stations.keys()))
    # output_max_temp(stations)
# 101G10019881203078-99999M000060 -99999M-99999M000060 -99999M-99999M000070 -99999M-99999M000070 -99999M-99999M-99999M-99999M-99999M000080 -99999M-99999M000070 -99999M-99999M000080 -99999M

def write_to_file(d):
    for k in d.keys():
        with open(f'output/{k}.txt', 'w') as f:
            f.write(f'YEAR MONTH DAY HOUR TEMP\n')
            for line in d[k]:
                vals = line.replace('-', ' ').replace('M', ' ').split()
                vals = list(filter(None, vals))
                year = vals[0][7:11]
                month = vals[0][11:13]
                day = vals[0][13:15]

                hour = 1
                for val in vals:
                    temp = val[len(val) - 6:len(val)]
                    if temp.isdigit():
                        temp = int(temp) / 10.0
                        if temp > 100:
                            temp = -999
                    f.write(f'{year} {month} {day} {hour} {temp}\n')
                    hour += 1

def output_max_temp(d):
    for k in d.keys():
        station = d[k]


        with open(f'temp/{k}.txt', 'w') as f:
            f.write(f'YEAR MONTH DAY MAX_TEMP\n')
            for line in station:

                vals = line.replace('-', ' ').replace('M', ' ').split()
                vals = list(filter(None, vals))

                year = vals[0][7:11]
                month = vals[0][11:13]
                day = vals[0][13:15]

                vals[0] = vals[0][len(vals[0]) - 6:len(vals[0])]
                
                try:
                    converted = [int(i) if i.isdigit() else int(re.sub('[^0-9]','', i)) for i in vals]
                except:
                    print(f'CodeError: could not parse list of length {len(converted)}, list: {converted}')
                for i, val in enumerate(converted):
                    val /= 10.0
                    if val > 100:
                        val = -100
                    converted[i] = val

                max_temp = max(converted)

                f.write(f'{year} {month} {day} {max_temp}\n')


generate_files_by_station()

# for val in first_col:
#     station = val[0:7]
#     year = val[7:11]
#     month = val[11:13]
#     day = val[13:15]
#     elem = val[15:18]
#     temp = val[18:len(val)]

    