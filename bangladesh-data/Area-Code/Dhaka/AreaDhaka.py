file_name = 'DhakaAreaNames.csv'
list=[]
with open(file_name,'r') as file:
    lines = file.readlines()
    for line in lines:
        l=line.strip()
        l=l.upper()
        flag=False
        for i in range(0,len(l)):
            if(l[i]>='A' and l[i]<='Z'):
                flag=True
                break
        if(flag==True):
            #print(l)
            list.append(l.strip('"'))

with open(file_name,'w') as file:
    for i in range(0,len(list)):
        file.write(list[i]+'\n')
    file.close()
