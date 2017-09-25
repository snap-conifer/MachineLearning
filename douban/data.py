import json
import glob
import pdb
import matplotlib.pyplot as plt
import matplotlib.font_manager
ZH = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')

PATH = "data/"

#载入json数据
def load_json(path:str):
	file_list = glob.glob(path + "*.txt")
	print("total file:",len(file_list),"---------",end="")
	json_list = []
	for file in file_list:
		fp = open(file)
		json_list.append(
			json.load(fp)
		)
		fp.close()
	return json_list

#分析时长跟star的关系
def runtime_and_star(json_list:list,Star=5):
	record = dict()
	record["less_than_60"] = {"good":0,"bad":0}
	record["60-100"] =  {"good":0,"bad":0}
	record["100-145"] = {"good":0,"bad":0}
	record["145-185"] = {"good":0,"bad":0}
	record["more_than_185"] = {"good":0,"bad":0}
	for j in json_list:
		try:
			star = float(j.get("star",0) )
		except Exception:
			star = 0
		runtime = j.get("runtime","")
		try:
			number_runtime = int(
				runtime.replace("分钟","")
			)
		except Exception:
			number_runtime = 0
		# >= 7 good（+1） / <7 Bad（-1）
		g_score = 0
		b_score = 0
		if star >= Star:
			g_score = 1
		elif star > 0:
			b_score = 1

		if number_runtime < 60 and number_runtime>0:
			record["less_than_60"]["good"] += g_score
			record["less_than_60"]["bad"] += b_score
		elif number_runtime >= 60 and number_runtime < 100:
			record["60-100"]["good"] += g_score
			record["60-100"]["bad"] += b_score
		elif number_runtime >= 100 and number_runtime < 145:
			record["100-145"]["good"] += g_score
			record["100-145"]["bad"] += b_score
		elif number_runtime >= 145 and number_runtime <= 185:
			record["145-185"]["good"] += g_score
			record["145-185"]["bad"] += b_score
		elif number_runtime >185:
			record["more_than_185"]["good"] += g_score
			record["more_than_185"]["bad"] += b_score

	return  record

def save_r_a_s(x,y1,y2,filename):
	fig = plt.figure(1, figsize=(12, 8))
	ax1 = fig.add_subplot(111)
	plt.xticks([a + 1.25 for a in range(len(y1))], x, rotation=0)
	plt.xlabel("Runtime(min)")
	plt.ylabel("Number")
	ax1.bar([1, 2, 3, 4, 5], y1, width=.25, color='orange', alpha=.5, label="good")
	ax1.bar([1.25, 2.25, 3.25, 4.25, 5.25], y2, width=.25, color='r', alpha=.5, label="bad")
	ax1.set_title('Runtime And Star')
	plt.legend()
	plt.savefig(filename)
	plt.close(1)

#主演与类型
def actor_and_type(json_list:list)->dict:
        record = dict()
        for j  in json_list:
                actor_str = j.get("actor")
                if not actor_str:
                        continue
                actor_list = actor_str.split("/")
                type_str = j.get("type")
                if not type_str:
                        continue
                type_list = type_str.split("/")
                for actor in actor_list:
                        if actor not in record:
                                record[actor] = dict()
                        for type in type_list:
                                if type not  in record[actor]:
                                        record[actor][type] = 0
                                record[actor][type] += 1
        return record

# 演员和类型的清洗
# return{
# info:[(name1,权重),(name2,权重……)……]，
# info2:[……]
# }
def clear0(record:dict,number=5):
        def set_key(key):
                def func(x):
                        try:
                                return record[x][key]
                        except KeyError:
                                return -1
                return func

        type_list = ["喜剧","剧情","爱情","悬疑","科幻","惊悚","动作","恐怖","犯罪"]
        result = dict()
        for _type in type_list:
                info_list = sorted(record,key=set_key(_type),reverse=True)
                info = [(key,record[key].get(_type,0)) for key in info_list[:number]]
                result[_type] = info
        return result

#类型和主演
def picture0(clear_res:dict,filename:str):
	plt.figure(1, figsize=(12, 9))
	# 总题目
	plt.suptitle("Type and Actor", fontsize=17, fontweight='bold')
	label_all = [t for t in clear_res]
	print(clear_res)
	print(label_all)

	for index in range(len(label_all)):
		color_list = ["red", "blue", "lightskyblue", "orange", "green"]#"pink","purple","yellow",'yellowgreen']
		p1 = plt.subplot(331 + index)
		key = label_all[index]
		p1.set_title(key,fontproperties=ZH)
		explode = [0 for x in range(5)]
		label = [info[0] for info in clear_res[key]]
		size = [info[1] for info in clear_res[key]]
		Angle = 0
		if len(size) == 0 or size == [0 for x in range(5)]:
			size = [0]
			label = [""]
			explode = [0]
			color_list = ["white"]
			Angle = 90
		else:

			# 手动计算百分比，去掉一些比例过小的元素的标签，统称other
			_sum = sum(size)
			size = [round((x / _sum), 2) for x in size]
			label = [  label[x]   if size[x] > 0.02 else "Other"
			         for x in range(len(label))]
			# 寻找size中的最大元素，然后返回其下标
			def find_index(l: list):
				temp = 0
				index = 0  # 全部相对返回0，将第一块圆饼分出来
				for i in range(len(l)):
					if l[i] > temp:
						temp = l[i]
						index = i
				return index

			explode[find_index(size)] = 0.08
		patches, l_text, p_text = p1.pie(size, colors=color_list, startangle=Angle, shadow=False, explode=explode
		                                 , labels=label, autopct='%3.1f%%', pctdistance=0.6)
		for text in l_text:
			text.set_fontproperties(ZH)
			text.set_size(9)
		p1.axis('equal')
	plt.savefig(filename)
	# plt.show()
	plt.close(1)
	
if __name__ == "__main__":
        print("loading-----",end="")
        json_list = load_json(PATH)
        print("OK!")
        #获取播映时间和评分数的数据
        r_a_s = runtime_and_star(json_list)
        x = []
        y1 =[]
        y2 =[]
        for k,v in r_a_s.items():
                x.append(k.replace("_"," "))
                y1.append(v.get("good")+1)
                y2.append(v.get("bad")+1)
        save_r_a_s(x,y1,y2,"result/runtime_and_star.jpg")
        print("Finish-----Runtime and star")

        # 主演和类型(过滤选出前5位，每人一个饼状图)
        a_a_t = actor_and_type(json_list)
        res = clear0(a_a_t)
        picture0(res,"result/Type_and_Actor.jpg")
        print("Finish-----Type and Actor")


        '''
        #播放时间系列=========================================
        #播放时间与类型
        r_a_t = runtime_and_any(json_list,key="type")
        save_r_a_t(r_a_t,"result/runtime_and_type.jpg")
        print("Finish-----Runtime and type")

        #播放时间和主演(每个阶段过滤出5位，饼状图，占5位总数的百分比)
        r_a_a = runtime_and_any(json_list,key="actor")
        res = clear2(r_a_a)
        picture2(res,"Actor","result/Actor_and_runtime.jpg")
        print("Finish-----Actor and runtime")
        '''
