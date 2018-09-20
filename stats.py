import random
import numpy as np
import scipy as sp
import pandas as pd
import scipy.stats as stats
import csv
import os

np.random.seed(1)

def get_class():
	xk = np.arange(5)
	pk = (0.2, 0.32, 0.32, 0.15, 0.01)
	custm = stats.rv_discrete(name='custm', values=(xk, pk))
	return  custm.rvs() + 1

def get_income2():

	df = (pd.read_csv("data/cps_00005.csv"))
	df = df[df["INCTOT"] != 99999999]
	df = df[df["INCTOT"] >= 0]
	df = df[df["INCTOT"] != 99999998]
	df = df[df["FTOTVAL"] >=0]
	df['CLASS'] = pd.cut(df['FTOTVAL'], [-1, 16000, 30000, 75000, 350000,999999999], labels = ['l', 'w', 'lm', 'um', 'u'])
	labels = ["{0} - {1}".format(i, i + 15) for i in range(15, 90, 15)]
	df['GROUPS'] = pd.cut(df.AGE, range(15, 105, 15), right=False, labels=labels)

	df["SEX"] = df["SEX"].map({1:"M", 2:"F"})
	from sklearn.utils import shuffle
	from sklearn.metrics import mean_squared_error, r2_score

	df = shuffle(df)
	df = df[["AGE","SEX","CLASS","INCTOT"]]
	df.to_csv("data/my_data.csv")

	from sklearn.preprocessing import LabelEncoder

	lb_make = LabelEncoder()
	df['SEX'] = lb_make.fit_transform(df['SEX'])
	df['GROUPS'] = lb_make.fit_transform(df['GROUPS'])
	df['CLASS'] = lb_make.fit_transform(df['CLASS'])

	X = df[["AGE","SEX","CLASS"]]
	y = df[["INCTOT"]]

	# Split the data into training/testing sets
	t = int(len(X)*0.66)
	X = np.array(X)
	y = np.array(y)
	y = np.ravel(y)
	X_train = X[:t]
	X_test  = X[t:]

	y_train = y[:t]
	y_test = y[t:]
	#Both the C and e value will be quite large, as we don't want to penalize
	#results that aren't too far from the target as we are talking about money.
	#regr = MLPRegressor(hidden_layer_sizes=(30,30), activation='relu', solver='adam', alpha=10000, batch_size='auto', learning_rate='adaptive', learning_rate_init=0.01, power_t=0.5, max_iter=1000, shuffle=True, random_state=None, tol=0.0001, verbose=True, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08)

	from sklearn.linear_model import LinearRegression
	from sklearn import neighbors
	from sklearn.neural_network import MLPRegressor
	from sklearn.model_selection import cross_val_score
	from sklearn.ensemble import RandomForestRegressor
	from sklearn.metrics import explained_variance_score, mean_absolute_error, r2_score

	#regr = LinearRegression() 0.06 variance
	#regr = neighbors.KNeighborsRegressor(49, weights="distance",p=4, algorithm="kd-tree") 0.45 variance
	regr = RandomForestRegressor(verbose =True)
	regr.fit(X_train, y_train)
	preds = regr.predict(X_test)

	print explained_variance_score(y_test, preds)
	print mean_absolute_error(y_test, preds)
	print r2_score(y_test, preds)



def get_income(social_class):
	#Got classes from https://en.wikipedia.org/wiki/Household_income_in_the_United_States  Social_Class
	#lower_class = 1 (14-20%) , working_class =  2 (20 -52%), lower_middle_class = 3 (52-84%), upper_middle_class= 4 (84-99%), upper_class = 5 (99-100%)

	if(social_class == 1):
		inc = np.random.uniform(-4367.355, 22702.328)
	elif(social_class == 2):
		inc = np.random.normal(24582.61, 17385.96)
	elif(social_class == 3):
		inc = np.random.normal(42932.44, 32864.41)
	elif(social_class == 4):
		inc = np.random.normal(81311.41, 72562.80)
	else:
		inc = np.random.gamma(1/0.720821, 1/0.000002367471)

	return inc
	# ro.r.source("income.R")
	# ro.r('''source("income.R")''')

	# inc = ro.globalenv['income']

	# x = inc(18,2,3)
	# return x
def get_marital_status(gender, age):
	if(gender == 0):
		if(age <15):
			prob = 0
		elif(age <= 19):
			prob = 0.015
		elif(age <= 24):
			prob = 0.13
		elif(age <= 29):
			prob = 0.389
		elif(age <= 34):
			prob = 0.65
		elif(age <= 39):
			prob = 0.775
		elif(age <= 44):
			prob = 0.816
		elif(age <= 49):
			prob = 0.83
		elif(age <= 54):
			prob = 0.875
		elif(age <= 59):
			prob = 0.921
		elif(age <= 64):
			prob = 0.949
		else:
			prob = 0.956
	else:
		if(age < 15):
			prob = 0
		elif(age <= 19):
			prob = 0.028
		elif(age <= 24):
			prob = 0.226
		elif(age <= 29):
			prob = 0.537
		elif(age <= 34):
			prob = 0.737
		elif(age <= 39):
			prob = 0.836
		elif(age <= 44):
			prob = 0.869
		elif(age <= 49):
			prob = 0.885
		elif(age <= 54):
			prob = 0.90
		elif(age <= 59):
			prob = 0.929
		elif(age <= 64):
			prob = 0.955
		else:
			prob = 0.96
	num =  np.random.rand()
	if (num <= prob):
		return 1
	else:
		return 0


def get_capital(age, social_class, income):
	#https://www.whitecoatinvestor.com/your-capital-to-income-ratio/
	if(age <= 25):
		capital = income * 0.1
	elif(age <= 30):
		if(social_class in [1,2]):
			capital = income * 0.45
		elif(social_class in [3,4]):
			capital = income * 0.5
		else:
			capital = income * 0.6
	elif(age <= 35):
		if(social_class in [1,2]):
			capital = income
		elif(social_class in [3,4]):
			capital = income * 1.25
		else:
			capital = income * 1.4
	elif(age <= 40):
		if(social_class in [1,2]):
			capital = income * 1.6
		elif(social_class in [3,4]):
			capital = income * 2
		else:
			capital = income * 2.4
	elif(age <=45):
		if(social_class in [1,2]):
			capital = income * 2.5
		elif(social_class in [3,4]):
			capital = income * 3.1
		else:
			capital = income * 3.7
	elif(age <= 50):
		if(social_class in [1,2]):
			capital = income * 3.5
		elif(social_class in [3,4]):
			capital = income * 4.5
		else:
			capital = income * 5.2
	elif(age <= 55):
		if(social_class in [1,2]):
			capital = income * 4.8
		elif(social_class in [3,4]):
			capital = income * 6.1
		else:
			capital = income * 7.1
	elif(age <= 60):
		if(social_class in [1,2]):
			capital = income * 6.5
		elif(social_class in [3,4]):
			capital = income * 8.1
		else:
			capital = income * 9.4
	else:
		if(social_class in [1,2]):
			capital = income * 8.2
		elif(social_class in [3,4]):
			capital = income * 10
		else:
			capital = income * 12
	return capital
def plot_capital_to_class(population, N):
    # Check the capital to social class distribution
    capital = []
    total_cap = 0
    class_size = [0] * 5
    class_cap = [0] * 5
    tot_inc = 0
    class_inc = [0] *5
    for p in population:
        capital.append(p.capital)
    	total_cap += p.capital
        tot_inc +=p.income
    	class_size[p.social_class-1] += 1
    	class_cap[p.social_class-1] += p.capital
        class_inc[p.social_class-1] +=p.income

    class_inc = np.array(class_inc)
    print "Income:"
    print  (class_inc/tot_inc) *100
    class_cap = np.array(class_cap)
    print "Capital:"
    arr = (class_cap/total_cap)*100
    print  arr

    class_size = np.array(class_size)
    print "Population:"
    pop = (class_size/float(N))*100
    print pop

    print "Capital:Population ratio"
    print (arr/pop)
    import matplotlib.pyplot as plt

    ind = np.arange(5)

    plt.bar(ind, arr, align= 'center', width = 0.5)
    plt.xticks(ind,("Lower Class", "Working Class", "Lower Middle Class", "Upper Middle Class", "Upper class") )
    plt.ylabel("Capital")
    plt.title("Capital distribution per social class (Simulation)")
    plt.tight_layout()
    plt.ylim(0.0,60.0)
    plt.show()

    return capital

def gini_index(capital):
    capital = capital.flatten()
    if np.amin(capital) < 0:
        # Values cannot be negative:
        capital -= np.amin(capital)
    # Values cannot be 0:
    capital += 0.0000001
    # Values must be sorted:
    capital = np.sort(capital)
    # Index per array element:
    index = np.arange(1,capital.shape[0]+1)
    # Number of array elements:
    n = capital.shape[0]
    # Gini coefficient:
    return ((np.sum((2 * index - n  - 1) * capital)) / (n * np.sum(capital)))
