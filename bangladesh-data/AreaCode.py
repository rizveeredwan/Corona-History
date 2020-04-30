def ReadRawData(file_name):
    area_raw_data={}
    area_raw_data_flag={}
    with open(file_name,'r') as csv_file:
        lines = csv_file.readlines()
        for i in range(1,len(lines)):
            print(lines[i],i)
            line = lines[i].strip().split(',')
            area_raw_data[line[0]]=line[1]
            area_raw_data_flag[line[0]]=0
    return area_raw_data,area_raw_data_flag

def UpdateMainData(file_name, date, area_raw_data, area_raw_data_flag):
    saved_lines=[]
    with open(file_name,'r') as file:
        lines = file.readlines()
        for i in range(0,len(lines)):
            saved_lines.append(lines[i].strip())
    with open(file_name,'w') as file:
        for i in range(0,len(saved_lines)):
            if(i==0):
                file.write(saved_lines[i]+","+date+'\n')
            else:
                try:
                    line=saved_lines[i].strip().split(',')
                    if(line[0] in area_raw_data):
                        data = saved_lines[i]+','+str(area_raw_data[line[0]])
                        #print("here data = ",data)
                        file.write(data+'\n')
                        area_raw_data_flag[line[0]]=1
                    else:
                        data = saved_lines[i]+','+str(saved_lines[i][len(saved_lines[i]-1)])
                        #print("there data = ",data)
                        file.write(data+'\n')
                except Exception as e:
                    print(e)
        length=len(saved_lines[0].strip().split(","))
        for key in area_raw_data_flag:
            if(area_raw_data_flag[key]==0 and key != ""):
                line = key
                for i in range(0,length):
                    line=line+","+" "
                line=line+','+str(area_raw_data[key])
                file.write(line+'\n')
                print("new line added for = ",key)

date='4/30/20'
area_raw_data,area_raw_data_flag = ReadRawData('AreaTodayData.csv')
UpdateMainData('AreaDataWithCode.csv',date,area_raw_data,area_raw_data_flag)
