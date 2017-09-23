import pdb;

fp = open("uid_score_bid.txt","r")
users = {}
pdb.set_trace()

for line in open("uid_score_bid.txt"):
    cols = line.strip().split(",")
    if cols[0] not in users:
        users[cols[0]] = {}
    users[cols[0]][cols[2]] = float(cols[1])

class recommend:
    #定义的计算相似度的公式，用的是皮尔逊相关系数计算方法
    def pearson(rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_xx = 0
        sum_yy = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
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
        for instance in users:
            if instance != "changanamei":
                distance = (users["changanamei"], users[instance])
