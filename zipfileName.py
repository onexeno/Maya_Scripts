import zipfile
import re

z = zipfile.ZipFile("I:\channel.zip","r")

next = '90052.txt'
count = 1

comments = []

while(1):
    information = z.read(next)

    comments.append(z.getinfo(next).comment)

    information=str(information,encoding='utf-8')

    result = re.findall("[0-9]",information)

    convert = ''.join(result)

    next=convert+'.txt'

    count+=1

    end=''
    for list in comments:
        end+=str(list,encoding='utf-8')
    print(end)

    