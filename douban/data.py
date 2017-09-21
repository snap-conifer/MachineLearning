import json
import glob
import pdb
import matplotlib.pyplot as plt

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
	
if __name__ == "__main__":
    print("loading----", end="")
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
    save_r_a_s(x,y1,y2,"result/runtime_and_star.png")
    print("Finish-----Runtime and star")
