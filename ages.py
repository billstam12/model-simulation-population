import pandas as pd
import numpy as np
import random

def get_age_percents():
	ages = pd.read_csv("data/ages.csv")
	ages_df = pd.DataFrame(ages)
	starting_columns = ["Total", "0 - 4", "5 - 9", "10 - 14", "15 - 19", "20 - 24", "25 - 29", "30 - 34", "35 - 39", "40 - 44", "45 - 49"
	, "50 - 54", "55 - 59", "60 - 64", "65 - 69", "70 - 74", "75 - 79", "80 - 84", "85 - 89", "90 - 94", "95 - 99", "100 +"]
	final_columns = ["Total", "0 - 9", "10 - 19", "20 - 29", "30 - 39", "40 - 49", "50 - 59", "60 - 69", "70 - 79", "80 - 89", "90 - 99", "100 +"]

	# ages_1 = ages_df["Value"].loc[(ages_df["Age"].isin(starting_columns[5:7])) & (ages_df["Sex"] == "Male")]
	# print ages_1

	ages_m = []
	ages_f = []
	t = 0
	for i in range(1,11):
		ages_m .append(sum(ages_df["Value"].loc[(ages_df["Age"].isin(starting_columns[i+t:i+t+2])) & (ages_df["Sex"] == "Male")]))
		ages_f .append(sum(ages_df["Value"].loc[(ages_df["Age"].isin(starting_columns[i+t:i+t+2])) & (ages_df["Sex"] == "Female")]))

		t = t + 1

	total_m = sum(ages_df["Value"].loc[(ages_df["Age"] == "Total") & (ages_df["Sex"] == "Male")])
	hundred_m = sum(ages_df["Value"].loc[(ages_df["Age"] == "100 +") & (ages_df["Sex"] == "Male")])

	total_f = sum(ages_df["Value"].loc[(ages_df["Age"] == "Total") & (ages_df["Sex"] == "Female")])
	hundred_f = sum(ages_df["Value"].loc[(ages_df["Age"] == "100 +") & (ages_df["Sex"] == "Female")])

	ages_m .append(hundred_m)

	ages_f .append(hundred_f)

	#Get percents of ages
	import numpy as np
	ages_m = np.array(ages_m)
	ages_f = np.array(ages_f)

	ages_m_percent = (ages_m/total_m)*100
	ages_f_percent = (ages_f/total_f)*100

	ages_m_percent = ["%.2f"%item for item in ages_m_percent ]
	ages_f_percent = ["%.2f"%item for item in ages_f_percent ]


	return ages_m_percent, ages_f_percent

def get_age(gender):
	m_p, f_p = get_age_percents()
	prev = 0
	if gender == 0:
		for i, x in enumerate(m_p):
			m_p[i] = prev + float(x)
			prev = m_p[i]

		r_n = np.random.randint(101)
		if r_n < m_p[0]:
			age = np.random.randint(10)
		elif r_n < m_p[1]:
			age = np.random.randint(10,20)
		elif r_n < m_p[2]:
			age = np.random.randint(20,30)		elif r_n < m_p[3]:
			age = np.random.randint(30,40)
		elif r_n < m_p[4]:
			age = np.random.randint(40,50)
		elif r_n < m_p[5]:
			age = np.random.randint(50,60)
		elif r_n < m_p[6]:
			age = np.random.randint(60,70)
		elif r_n < m_p[7]:
			age = np.random.randint(70,80)
		elif r_n < m_p[8]:
			age = np.random.randint(80,90)
		elif r_n < m_p[9]:
			age = np.random.randint(90,99)
		else:
			age = 100
	elif gender == 1:
		for i, x in enumerate(f_p):
			f_p[i] = prev + float(x)
			prev = f_p[i]

		r_n = np.random.randint(101)
		if r_n < f_p[0]:
			age = np.random.randint(10)
		elif r_n < f_p[1]:
			age = np.random.randint(10,20)
		elif r_n < f_p[2]:
			age = np.random.randint(20,30)
		elif r_n < f_p[3]:
			age = np.random.randint(30,40)
		elif r_n < f_p[4]:
			age = np.random.randint(40,50)
		elif r_n < f_p[5]:
			age = np.random.randint(50,60)
		elif r_n < f_p[6]:
			age = np.random.randint(60,70)
		elif r_n < f_p[7]:
			age = np.random.randint(70,80)
		elif r_n < f_p[8]:
			age = np.random.randint(80,90)
		elif r_n < f_p[9]:
			age = np.random.randint(90,99)
		else:
			age = 100
	return age

def check_death(person):
	if (person.age>=100):
		return 1

	indexes = [[0,1], [1,4], [5,14], [15,24], [25,34], [45,54] , [55,64], [65,74], [75,84], [85,100]]
	am_percent = [0.00565, 0.000228, 0.00012, 0.000524, 0.000823, 0.001508, 0.003584, 0.008929, 0.0238, 0.0667, 0.167]
	fm_percent = [0.0044, 0.000186, 0.000096, 0.00024, 0.0004, 0.0009, 0.00238, 0.00561, 0.01538, 0.04762, 0.1429]

	range = 0
	for index, rng in enumerate(indexes):
		if((person.age >= rng[0]) & (person.age <= rng[1])):
			range = index
	if(person.gender == 0):
		prob =  float(am_percent[range])
	else:
		prob =  float(fm_percent[range])

	num =  np.random.rand()
	if (num <= prob):
		return 1
	else:
		return 0
