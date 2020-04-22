import csv
dict_today={}
with open('DistrictData.csv','r') as csv_file:
    lines = csv_file.readlines()
    for i in range(0,len(lines)):
        if(i==0):
            continue
        line=lines[i].strip().split(",")
        if(line[0] == 'Barishal'):
            line[0]='Barisal'
        if(line[0] == "Chattogram"):
            line[0] = 'Chittagong'
        if('Cox' in line[1]):
            line[1]="Cox's bazar"
        print(line[0]+','+line[1])
        dict_today[line[0]+','+line[1]]={}
        dict_today[line[0]+','+line[1]]['division'] = line[0]
        dict_today[line[0]+','+line[1]]['district'] = line[1]
        dict_today[line[0]+','+line[1]]['total'] = line[2]
        dict_today[line[0]+','+line[1]]['flag'] = 0

saved_lines=[]
with open('bd_cases.csv','r') as csv_file:
    saved_lines = csv_file.readlines()

with open('bd_cases.csv','w') as csv_file:
    todays_date = '4/22/20'
    for i in range(0,len(saved_lines)):
        #print(saved_lines[i])
        if(i==0):
            saved_lines[i]=saved_lines[i].strip()
            csv_file.write(saved_lines[i]+','+todays_date+'\n')
            continue
        try:
            line = saved_lines[i].strip().split(',')
            key = line[0]+","+line[1]
            write = saved_lines[i].strip()
            write = write + ','+dict_today[key]['total']
            csv_file.write(write+'\n')
            dict_today[key]['flag']=1
        except Exception as e:
            print(saved_lines[i])
            print(e,"key not found")
            write = saved_lines[i].strip()
            write = write + ","+"0"
            csv_file.write(write+'\n')
            print("written failed")

print("\n")
for key in dict_today:
    if(dict_today[key]['flag'] == 0):
        print(key)
        print("flag not set")
