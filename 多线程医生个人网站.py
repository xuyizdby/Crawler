import re
import requests
from lxml import etree
import math
import threading
import random
import time
import datetime
import csv
import gc
from bs4 import BeautifulSoup
from selenium import webdriver
#1.引入 ActionChains 类
from selenium.webdriver.common.action_chains import ActionChains

def write_xlms(path_file, mode, list_row):
    with open(path_file, mode, newline='') as xlms_file:
        xlms_writer = csv.writer(csv_file)
        csv_writer.writerow(list_row)

def get_pricepage_source(url):
	try:
		driver= webdriver.Chrome("C:/Driver/chromedriver")

		driver.get(url)

		

		
		time.sleep(5)

		#2.定位到要悬停的元素
		element1= driver.find_element_by_xpath('//div[@class="w1000 bc pt50 f-yahei"]/div[@class="zxNeedRead"]/a')
		#3.对定位到的元素执行鼠标悬停操作
		element1.click()
		source = driver.page_source
		driver.close()
	except:
		pass
	return source


def read_csv(filepath):
	with open(filepath,'r',encoding='gb18030') as csvfile:
		reader = csv.reader(csvfile)
		row = [row for row in reader]
		
	return row

def read_href(html):
	'''res_url=r'href="(.*?)"'''
	soup = str(BeautifulSoup(html, 'html.parser'))
	res_url=r'<p class="d-c-i-c-name"><a class="d-c-i-c-n-click" href="(.*?)"'
	link = re.findall(res_url,soup,re.DOTALL)
	return link

def getHTMLText(url):
	try:
		User_Agent = [
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
		'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
		'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'
		]
		len_user_agent = len(User_Agent)
		random_num = random.randint(0, len_user_agent-1)
		user_agent = User_Agent[random_num]
		kv={'user-agent':user_agent}
		r=requests.get(url,headers=kv,timeout=30)
		r.raise_for_status()
		r.encoding=r.apparent_encoding
		return r.text
	except:
		return ""
#写文件
def write_csv(path_file, mode, list_row):
	with open(path_file, mode, newline='') as csv_file:
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow(list_row)


def get_andere_page(num):
	try:
		kv={'user-agent':'Mozilla/5.0'}
		url="https://www.haodf.com/doctorteam/p_"+str(num)+".htm"
		r=requests.get(url,headers=kv)
		r.encoding=r.apparent_encoding
		responce=r.text
		return responce,url
	except:
		return("爬取失败")
#获得在线问诊页信息
def get_price_info(html):
	priceinfo=list()
	soup = str(BeautifulSoup(html, 'html.parser'))
	selector = etree.HTML(html)
	try:
		try:
			#疗效
			liaoxiao = selector.xpath('/html/body/div[2]/div[1]/div[2]/div[2]/p[1]/span[@class="score_fen"]/text()')[0]
			priceinfo.append(liaoxiao[:-2])
			#态度
			taidu = selector.xpath('/html/body/div[2]/div[1]/div[2]/div[2]/p[2]/span[@class="score_fen"]/text()')[0]
			priceinfo.append(taidu[:-2])
		except:
			priceinfo.append('无')
			priceinfo.append('无')


		try:
			#图文问诊一般等待时长
			yibandengdaishichang = selector.xpath('//div[@class="service-box"]/p[@class="f18 mt35b11"][1]/span[@class="score_fen"]/text()')[0]
			priceinfo.append(yibandengdaishichang)
		except:
			priceinfo.append('无')


		try:
			#图文问诊费用
			tuwenwenzhen = selector.xpath('//div[@class="service-info"]/p[@class="service-name"]/span[@class="service-name-price"]/text()')[0]
			priceinfo.append(int(tuwenwenzhen[:-1]))
		except:
			priceinfo.append('无')


		try:
			#一问一答费用
			yiwenyidafeiyong = selector.xpath('//ul[@class="service-list js-service-list"]/li[2]/div[@class="service-info"]/p[@class="service-name"]/span[@class="service-name-price"]/text()')[0]
			priceinfo.append(int(yiwenyidafeiyong[:-1]))
		except:
			priceinfo.append('无')


		try:
			#患者投票数（价格页）
			huanzhetoupianshujiageye = selector.xpath('/html/body/div[2]/div[1]/div[2]/div[1]/p[1]/span/text()')[0]
			priceinfo.append(huanzhetoupianshujiageye)
		except:
			priceinfo.append('无')
		#电话问诊费用
		try:
			dianhuawenzhenfeiyong1 = selector.xpath('//span[@class="service-name-price"]/text()')[2]
			priceinfo.append(dianhuawenzhenfeiyong1)
			print(dianhuawenzhenfeiyong1)
			allprice=selector.xpath('//span[@class="service-name-price"]/text()')
			priceinfo.append(allprice)
			#电话问诊24小时接听率
			dainhua24jietinglv = selector.xpath('//p[@class="f18 mt35b11 clearfix"]/span[@class="score_fen"]/text()')[0]
			priceinfo.append(dainhua24jietinglv)
		except:
			pass
	except:
		pass
	return priceinfo


#获得个人信息页信息
def get_private_info(html):
	privateInfoPagelist=list()
	soup = str(BeautifulSoup(html, 'html.parser'))
	selector = etree.HTML(html)
	try:
		#近两周帮助患者数
		jinliangzhou = selector.xpath('//div[@id="bp_doctor_about"]/div/div[2]/div/div[2]/div/div[2]/p[2]/span[2]/text()')[0]

		privateInfoPagelist.append(jinliangzhou)
	except:
		pass
	print(privateInfoPagelist)
	return privateInfoPagelist

#获得医生个人主页信息
def get_team_info(html):
	privateInfoPage=''
	info=list()
	soup = BeautifulSoup(html, 'html.parser')
	selector = etree.HTML(html)
	try:
		#姓名
		xingming=selector.xpath('//div[@class="space_b_title"]/h1/a[@class="space_b_link_url"]/text()')[0]
		info.append(xingming[:-7])
		#医院
		yiyuan=selector.xpath('//div[@class="doc_hospital clearfix"]/div[@class="fl pr"]/p/a[1]/text()')[0]
		info.append(yiyuan)
		#科室
		keshi=selector.xpath('//div[@class="doc_hospital clearfix"]/div[@class="fl pr"]/p/a[2]/text()')[0]
		info.append(keshi)
		#诊后服务星个数
		try:
			zhenhoufuwuxing=selector.xpath('//div[@class="doctor_star_new"]/span[@class="doctor_star_disease"]/span[@class="doctor_star_yellow"]')
			zhenhoufuwuxinggeshu=len(zhenhoufuwuxing)
		except:
			zhenhoufuwuxinggeshu=0
		info.append(zhenhoufuwuxinggeshu)

		#感谢信数量
		ganxiexin=selector.xpath('//span[@class="mr20"]/a/text()')[0]
		info.append(ganxiexin)
		
		#科室
		'''keshi=selector.xpath('//div[@class="clearfix pt5 bb_d pb5"]/div[@class="hh"]/a/text()')[0]
								info.append(str(keshi.replace('\n','').replace(' ','')))
						'''
		# 推荐热度
		try:
			recommend = selector.xpath('//span[@class="patient_recommend"]/i/text()')[0]
		except:
			recommend = ''
		info.append(recommend)
		# 总访问
		visits = selector.xpath('//ul[@class="space_statistics"]/li[1]/span/text()')[0]
		info.append(visits)
		# 昨日访问
		visits_yesterday = selector.xpath('//ul[@class="space_statistics"]/li[2]/span/text()')[0]
		info.append(visits_yesterday)
		# 昨日访问日期
		visits_yesterday_date = selector.xpath('//ul[@class="space_statistics"]/li[2]/text()')[1]
		visits_yesterday_date = visits_yesterday_date.replace('次(', '').replace(')', '')
		info.append(visits_yesterday_date)
		# 总文章
		articles = selector.xpath('//ul[@class="space_statistics"]/li[3]/span/text()')[0]
		info.append(articles)
		# 总患者
		patients = selector.xpath('//ul[@class="space_statistics"]/li[4]/span/text()')[0]
		info.append(patients)
		# 昨日诊后报到患者
		patients_after_yesterday = selector.xpath('//ul[@class="space_statistics"]/li[5]/span/text()')[0]
		info.append(patients_after_yesterday)
		# 微信诊后报到患者
		patients_after_wechat = selector.xpath('//ul[@class="space_statistics"]/li[6]/span/text()')[0]
		info.append(patients_after_wechat)
		# 总诊后报到患者
		patients_after = selector.xpath('//ul[@class="space_statistics"]/li[7]/span/text()')[0]
		info.append(patients_after)
		# 患者投票
		votes_patient = selector.xpath('//ul[@class="space_statistics"]/li[8]/span/text()')[0]
		info.append(votes_patient)
		# 感谢信
		letters_thanks = selector.xpath('//ul[@class="space_statistics"]/li[9]/span/text()')[0]
		info.append(letters_thanks)
		# 心意礼物
		gifts = selector.xpath('//ul[@class="space_statistics"]/li[10]/span/text()')[0]
		info.append(gifts)
		# 上次在线
		online_last = selector.xpath('//ul[@class="space_statistics"]/li[11]/span/text()')[0]
		info.append(str(online_last))
		# 开通时间
		opening_time = selector.xpath('//ul[@class="space_statistics"]/li[12]/span/text()')[0]
		info.append(opening_time)
		#开通业务数量
		yewu=selector.xpath('//div[@class="d-s-items"]/a')
		yewushuliang=len(yewu)
		info.append(yewushuliang)
		#个人信息页
		gerenxinxiye=selector.xpath('//div[@class="space_b_info_page newsc"]/a/@href')[0]
		privateInfoPage=gerenxinxiye
		#门诊时间
		try:
			time=soup.find_all("table",class_="fs")
			tab = time[0]
			time1=tab.find_all('tr')
			for tr in time1[1:8]:
				for td in tr.find_all('td')[1:]:
					if td.getText()!='':
						info.append(1)
					else:
						info.append(0)
		except:
			pass


	except:
		pass
		# print('craw failed, try again')
	return info,privateInfoPage



	#多线程
def craw(index, chunks_list, path_log_file):
	filepathread='D:/shuju3/data4.csv'
	doctor_link='D:/shuju3/doctorinfo4.csv'
	path_log_temp = 'D:/大三下Kämpfen!/Python/log_temp.txt'
	path_log = 'D:/大三下Kämpfen!/Python/log.txt'
	filepathwrite = open(doctor_link, 'a',encoding='gb18030',newline='')
	csv_write = csv.writer(filepathwrite,dialect='excel')
	url_list = chunks_list[index]
	jishu=0
	for i in url_list:
		eachDoctorPage=i[3]
		if eachDoctorPage=="javascript:void(0)":
			info=list()
			
			info.append(i[2])
			info.append(eachDoctorPage)
			info.append(i[0])
			info.append(i[4])
			info.append(i[1])
			info.append(i[5])
			csv_write.writerow(info)
		else:
			jishu=jishu+1
			alllink='https:'+str(eachDoctorPage)
			try:
				if jishu%3==0:
					time.sleep(6)
				elif jishu%10==0:
					time.sleep(20)
				else:
					time.sleep(4)
				htmltext=getHTMLText(alllink)
				info,privateInfoPage=get_team_info(htmltext)
				print(privateInfoPage)
				print(info)
				#价格页
				try:
					pricelink=alllink+"clinic/selectclinicservice"
					source=get_pricepage_source(pricelink)
					priceinfo=get_price_info(source)
					print(priceinfo)
					if priceinfo==[]:
						time.sleep(10)
						source=get_pricepage_source(pricelink)
						priceinfo=get_price_info(source)
						info=info+priceinfo
					else:
						info=info+priceinfo
				except:
					pass
				info.insert(1,eachDoctorPage)
				info.insert(2,i[0])
				info.insert(3,i[4])
				info.insert(4,i[1])
				info.insert(5,i[5])
				print(info)
				csv_write.writerow(info)
			except:
				pass

		# 回收垃圾
		del info
	del url_list
	gc.collect()


# 把所有的ulr分成n等份
def chunks(list, n):
	chunks_list = []
	len_list = len(list)
	step = math.ceil(len_list / n)
	for i in range(0, n):
		chunks_list.append(list[i*step:(i+1)*step])
	return chunks_list




def main():
	#读取链接列表
	filepathread='D:/shuju3/data4.csv'
	doctor_link='D:/shuju3/doctorinfo4.csv'
	path_log_temp = 'D:/大三下Kämpfen!/Python/log_temp.txt'
	path_log = 'D:/大三下Kämpfen!/Python/log.txt'
	filepathwrite = open(doctor_link, 'a',encoding='gb18030',newline='')
	csv_write = csv.writer(filepathwrite,dialect='excel')

	row=read_csv(filepathread)
	chunks_list = chunks(row, 2)
	thread_list = []
	 # 把url分成n等份，也即n个线程b
	for index in range(0, 2):
		thread = threading.Thread(target=craw, args=(index, chunks_list, path_log_temp))
		thread_list.append(thread)

		thread.start()
		
		
	for t in thread_list:
		t.join()

	




main()



