import csv

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
print("users:\n%s\n" %users)

     
     
