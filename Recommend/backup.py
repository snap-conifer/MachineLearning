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


#----------------新增代码段END----------------------



class recommender:
    #data：数据集，这里指users
    #k：表示得出最相近的k的近邻
    #metric：表示使用计算相似度的方法
    #n：表示推荐book的个数
    def __init__(self, data, k=3, metric='pearson', n=1):
        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}

        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        if type(data).__name__ == 'dict':
            self.data = data
      

    #定义的计算相似度的公式，用的是皮尔逊相关系数计算方法
    def pearson(self, bookdict1, bookdict2):
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
    
    def computeNearestNeighbor(self, username):
        distances = []
        for key in self.data:
            if key != username:
                distance = self.fn(self.data[username],self.data[key])
                distances.append((key, distance))

        distances.sort(key=lambda artistTuple: artistTuple[1],reverse=True)
        return distances
    
    #推荐算法的主体函数
    def recommend(self, user):
        #定义一个字典，用来存储推荐的书单和分数
        recommendations = {}
        #计算出user与所有其他用户的相似度，返回一个list
        nearest = self.computeNearestNeighbor(user)
#         print nearest
        
        userRatings = self.data[user]
#         print userRatings
        totalDistance = 0.0
        #得住最近的k个近邻的总距离
        for i in range(self.k):
            totalDistance += nearest[i][1]
        if totalDistance==0.0:
            totalDistance=1.0
            
        #将与user最相近的k个人中user没有看过的书推荐给user，并且这里又做了一个分数的计算排名
        for i in range(self.k):
            #第i个人的与user的相似度，转换到[0,1]之间
            weight = nearest[i][1] / totalDistance
            
            #第i个人的name
            name = nearest[i][0]
            #第i个用户看过的书和相应的打分
            neighborRatings = self.data[name]
            for bookid in neighborRatings:
                if not bookid in userRatings:
                    if bookid not in recommendations:
                        recommendations[bookid] = (neighborRatings[bookid] * weight)
                    else:
                        recommendations[bookid] += neighborRatings[bookid] * weight
                        
        # convert dict to list
        recommendations = list(recommendations.items())
        
        #做了一个排序
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)

#         print recommendations[:self.n],"-------"
        return recommendations[:self.n]

def recommend_bookid_to_user(username):
    bookid_list = []
    r = recommender(users)
    bookid_and_weight = r.recommend(username)
    print ("Recommend bookid and weight:",bookid_and_weight)
    for i in range(len(bookid_and_weight)):
        bookid_list.append(bookid_and_weight[i][0])
    print ("Recommend bookid: ", bookid_list)
        
if __name__ == '__main__':
   recommend_bookid_to_user("Li Si")