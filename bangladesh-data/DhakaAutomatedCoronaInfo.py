import requests
r = requests.get('http://covid19tracker.gov.bd/api/dhaka')
obj = r.json()
dhaka_dict={}
list=[]

key_map={
    'Sher-E-Bangla':'Sher-E-Bangla Nagar'
}

for i in obj:
    print(i,i['name'])
    if('Sher-E-Bangla' in i['name'] ):
        i['name']=key_map['Sher-E-Bangla']
    dhaka_dict[i['name'].strip()]={}
    dhaka_dict[i['name'].strip()]['bangla']=i['bnName']
    dhaka_dict[i['name'].strip()]['confirmed']=int(i['confirmed'])
    dhaka_dict[i['name'].strip()]['old-confirmed']=[]
    dhaka_dict[i['name'].strip()]['flag']=0
    list.append(i['name'])

dates=[]
change = False
with open('DhakaInfo.csv','r') as file:
    lines = file.readlines()
    if(len(lines) == 0):
        change=True
    if(len(lines) > 0):
        l=lines[0].strip().split(',')
        for i in range(1,len(l)):
            dates.append(l[i])
        for i in range(1,len(lines)):
            l = lines[i].strip().split(',')
            area = l[0].strip()
            current_value = int(l[len(l)-1])
            if(area in list):
                if(dhaka_dict[area]['confirmed']>current_value):
                    change=True
                    dhaka_dict[area]['flag']=1
                    for j in range(1,len(l)):
                        dhaka_dict[area]['old-confirmed'].append(l[j])
            else:
                print(area ," not found")
                dhaka_dict[area]={}
                dhaka_dict[area]['confirmed']=0
                dhaka_dict[area]['old-confirmed']=[]
                dhaka_dict[area]['flag']=1
                for j in range(1,len(l)):
                    dhaka_dict[area]['old-confirmed'].append(l[j])
                list.append(area)

for i in range(0,len(list)):
    if(dhaka_dict[list[i]]['flag']==0):
        change=True
        break

if(change==True):
    d=input('Give date: ')
    dates.append(d)
    list = sorted(list)
    with open('DhakaInfo.csv','w') as file:
        string = 'Location'
        for i in range(0,len(dates)):
            string = string + ',' + dates[i]
        file.write(string+'\n')
        for j in range(0,len(list)):
            key=list[j]
            string = key
            if(len(dhaka_dict[key]['old-confirmed'])>0):
                for i in range(0,len(dhaka_dict[key]['old-confirmed'])):
                    string = string + ',' + dhaka_dict[key]['old-confirmed'][i]
            else:
                for i in range(0,len(dates)-1):
                    string = string + ',' + '0'
            string = string + ',' + str(dhaka_dict[key]['confirmed'])
            print(string)
            file.write(string+'\n')
    file.close()


#print(obj)
#keys = obj.keys()
#print(keys)
