#code to extract the popular newspaers with country names
data=[]
with open('popular_news_papers_raw.txt','r') as f:
    lines = f.readlines()
    for i in range(0,len(lines),3):
        paper_name = lines[i+1].strip()
        country_name = lines[i+2].strip()
        data.append([paper_name, country_name])
        print(paper_name,country_name)

f=open('popular_news_papers_structured.csv','w')
lines='paper_name,country'
f.write(lines+'\n')
for i in range(0,len(data)):
    lines=data[i][0]+','+data[i][1]
    f.write(lines+'\n')
f.close()
