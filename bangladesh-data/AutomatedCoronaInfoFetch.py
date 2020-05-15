import requests

r = requests.get('http://covid19tracker.gov.bd/api/district')
obj = r.json()
keys = obj.keys()
print(keys)
keys = obj['features']
district={}

def DistrictKeyMap(dis):
    if(dis=='Munshiganj'):
        return 'Munshigonj'
    if(dis=='Narsingdi'):
        return 'Narshingdi'
    if(dis == 'Chittagong'):
        return 'Chattogram'
    if('Cox' in dis):
        return "Cox's bazar"
    if(dis == 'Comilla'):
        return 'Cumilla'
    if(dis == 'Brahamanbaria'):
        return 'B. Baria'
    if(dis == 'Lakshmipur'):
        return 'Laksmipur'
    if(dis == 'Khagrachhari'):
        return 'Khagrachari'
    if(dis == 'Maulvibazar'):
        return 'Moulovi Bazar'
    if(dis == 'Habiganj'):
        return 'Hobiganj'
    if(dis == 'Panchagarh'):
        return 'Panchagar'
    if(dis == 'Netrakona'):
        return 'Netrokona'
    if(dis == 'Barisal'):
        return 'Barishal'
    if(dis == 'Patuakhali'):
        return 'Potuakhali'
    if(dis == 'Jhalokati'):
        return 'Jhalokathi'
    if(dis == 'Nawabganj'):
        return 'Chapainawabganj'
    return dis

for i in range(0,len(obj['features'])):
    print(obj['features'][i]['properties'])
    key = DistrictKeyMap(obj['features'][i]['properties']['key'])
    district[key]={}
    district[key]['last-case']=int(obj['features'][i]['properties']['confirmed'])

def ReadFile(file_name,type):
    global district
    flag=0
    dates=[]
    with open(file_name,'r') as file:
        lines = file.readlines()
        l=lines[0].strip().split(',')
        for i in range(3,len(l)):
            dates.append(l[i])
        for i in range(1,len(lines)):
            l=lines[i].strip().split(',')
            district[l[1]][type]=[]
            district[l[1]]['division']=l[0]
            district[l[1]]['alt_name']=l[2]
            for j in range(3,len(l)):
                district[l[1]][type].append(int(l[j]))
                if(j==(len(l)-1) and int(l[j])<district[l[1]]['last-'+type]):
                    flag=1
        file.close()
    if(flag==1):
        d=input("Give new date: ")
        dates.append(d)
        with open(file_name,'w') as file:
            string = 'Division,District,Alt_Name'
            for i in range(0,len(dates)):
                string=string+','+dates[i]
            file.write(string+'\n')
            for key in district:
                string = district[key]['division']+','+key+','+district[key]['alt_name']
                for i in range(0,len(district[key][type])):
                    string = string + ',' + str(district[key][type][i])
                string = string + ',' + str(district[key]['last-'+type])
                file.write(string+'\n')
            file.close()

ReadFile('bd_cases - Copy.csv','case')
