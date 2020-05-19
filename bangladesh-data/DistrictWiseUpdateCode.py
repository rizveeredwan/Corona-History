import csv
dict_today={}

#complete data reading
with open('DistrictData.csv','r') as csv_file:
    lines = csv_file.readlines()
    for i in range(0,len(lines)):
        if(i==0):
            continue
        line=lines[i].strip().split(",")  #division, district, case, death, recovered
        while(len(line)<5):
            line.append("0")
        if(line[0] == 'Barishal'):
            line[0]='Barisal'
        if(line[0] == "Chattogram"):
            line[0] = 'Chittagong'
        if('Cox' in line[1]):
            line[1]="Cox's bazar"
        if('Rangmati' in line[1]):
            line[1] = 'Rangamati'

        if(line[2]==''):
            line[2]="0"
        if(line[3]==''):
            line[3]="0"
        if(line[4]==''):
            line[4]="0"

        print(line[0]+','+line[1])
        dict_today[line[0]+','+line[1]]={}
        dict_today[line[0]+','+line[1]]['division'] = line[0]
        dict_today[line[0]+','+line[1]]['district'] = line[1]
        dict_today[line[0]+','+line[1]]['case'] = line[2]
        dict_today[line[0]+','+line[1]]['death'] = line[3]
        dict_today[line[0]+','+line[1]]['recovered'] = line[4]
        dict_today[line[0]+','+line[1]]['flag'] = 0

def UpdateFiles(file_name,parameter,date,idx): #0=case, 1=death, 2=recovered
    saved_lines=[]
    with open(file_name,'r') as csv_file:
        saved_lines = csv_file.readlines()

    with open(file_name,'w') as csv_file:
        todays_date = date
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
                write = write + ','+dict_today[key][parameter]
                csv_file.write(write+'\n')
                dict_today[key]['flag']=idx
            except Exception as e:
                print(saved_lines[i])
                print(e,"key not found")
                write = saved_lines[i].strip()
                write = write + ","+"0"
                csv_file.write(write+'\n')
                print("written failed")

    print("\n")
    for key in dict_today:
        if(dict_today[key]['flag'] != idx):
            print(key)
            print("flag not set in ",parameter)

date = '5/18/20'
UpdateFiles('bd_cases.csv','case',date,1)
UpdateFiles('bd_deaths.csv','death',date,2)
UpdateFiles('bd_recovered.csv','recovered',date,3)
