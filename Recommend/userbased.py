import pdb
import csv
from math import sqrt

rows = []
csvFile = open('user_book.csv', 'r')
reader = csv.reader(csvFile)
for row in reader:
     rows.append(row)
rows.remove(rows[0]) #remove 1st row
print("rows:\n%s\n" % rows)
csvFile.close()

users = {}
for row in rows:
     if row[0] not in users:        
          users[row[0]] = {}
     users[row[0]][row[2]] = float(row[1])
print("users:\n%s\n" % users)

class recommend:
    #定义的计算相似度的公式，用的是皮尔逊相关系数计算方法
    def pearson(bookdict1, bookdict2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_xx = 0
        sum_yy = 0
        n = 0
        for key in bookdict1:
            if key in bookdict2:
                n += 1
                x = bookdict1[key]
                y = bookdict2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_xx += pow(x, 2)
                sum_yy += pow(y, 2)
        if n == 0:
            return 0
        
        #皮尔逊相关系数计算公式 
        denominator = sqrt(sum_xx - pow(sum_x, 2) / n)  * sqrt(sum_yy - pow(sum_y, 2) / n)
        if denominator == 0:
            return 0
        else:
            numerator = sum_xy - (sum_x * sum_y) / n
            return numerator / denominator

if __name__ == '__main__':
    username = "Li Si"
    distances = []
    for key in users: 
        if key != username:
            distance = recommend.pearson(users[username], users[key])
            distances.append((key, distance))
    distances.sort(key=lambda artistTuple:artistTuple[1], reverse=True)
    print("distances:\n%s\n" % distances)
