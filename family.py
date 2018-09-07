from random import randint
from simulation import *
import numpy as np
from stats import get_income
from stats import get_capital
from ages import check_death
from stats import *

id_count = 1

class Person:
	def __init__(self,gender, social_class, age, income, capital, marital_status):
		global id_count

		self.id = id_count
		self.social_class = social_class
		self.gender = gender
		self.age = age
		self.income = income
		self.husband_wife = 0
		self.children_id = []
		self.mother_id = 0
		self.father_id = 0
		self.children_status = 0
		self.marital_status = marital_status
		self.capital = capital
		id_count += 1

	def get_married(self, id):
		self.marital_status = 1
		self.husband_wife = id

	def assign_child(self, id):
		self.children_status = 1
		self.children_id.append(id)

	def assign_parents(self, father_id, mother_id):
		self.father_id = father_id
		self.mother_id = mother_id

	def set_social_class(self, new_class):
		self.social_class = new_class

	#def update_income(self):

	def update_capital(self,costs):
		self.capital += self.income
		self.capital -= costs

	def increment_age(self, increment):
		self.age += increment

	def pass_capital(self, cap, siblings):
		self.capital += (cap/siblings)

	def __repr__(self):
		return "<Person ID:%s, Gender:%s, Social Class:%s, Age:%s, Income:%s, Capital:%s, Husband/Wife ID:%s Children: %s Father: %s Mother: %s>" % (self.id, self.gender,
		self.social_class, self.age, self.income,self.capital, self.husband_wife, self.children_id, self.father_id, self.mother_id)

def create_partner(person):
	age = person.age

	if (person.gender == 0):
		partner_gender = 1
		partner_age = np.random.randint((age/2) + 7, age +7)
	else:
		partner_gender = 0
		partner_age = np.random.randint(age, age + 20)

	partner_social_class = person.social_class
	partner_income = get_income(partner_social_class)
	partner_capital = get_capital(partner_age, partner_social_class, partner_income)
	partner = Person(partner_gender, partner_social_class, partner_age, partner_income, partner_capital, 1)
	return partner

def create_parents(person):
	#Compute age, from random normal distribution
	social_class = person.social_class
	mu1 =  30
	sigma1 = 4

	mu2 = 35
	sigma2 = 4

	mother_age = int(np.random.normal(mu1, sigma1)) + person.age
	father_age = int(np.random.normal(mu2, sigma2)) + person.age

	mother_income = get_income(social_class)
	father_income = get_income(social_class)

	mother_capital = get_capital(mother_age, social_class, mother_income)
	father_capital = get_capital(father_age, social_class, father_income)
	mother = Person(1, social_class, mother_age, mother_income, mother_capital, 1)
	father = Person(0, social_class, father_age, father_income, father_capital, 1)

	mother.get_married(father.id)
	father.get_married(mother.id)

	mother.assign_child(person.id)
	father.assign_child(person.id)

	if(check_death(mother)):
		mother = 0
	if(check_death(father)):
		father = 0
	return mother, father

def get_children_status(mother, father):
	# Need to find statistic by age bins
	# https://www.cdc.gov/nchs/data/nhsr/nhsr051.pdf Tables
	# First get probability of bearing a child for men and women, and then then
	# probability of children by age.

	# MOTHER
	if(mother.age <= 19):
		m_prob = 0.067
	elif(mother.age <= 24 ):
		m_prob = 0.297
	elif(mother.age <= 29):
		m_prob = 0.549
	elif(mother.age <= 34):
		m_prob = 0.767
	elif(mother.age <= 39):
		m_prob = 0.829
	else:
		m_prob = 0.846

	# FATHER
	if(father.age <= 19):
		f_prob = 0.026
	elif(father.age <= 24 ):
		f_prob = 0.153
	elif(father.age <= 29):
		f_prob = 0.424
	elif(father.age <= 34):
		f_prob = 0.616
	elif(father.age <= 39):
		f_prob = 0.737
	else:
		f_prob = 0.764

	num1 =  np.random.rand()
	num2 =  np.random.rand()

	# Count children (may add later)
	if ((num1 <= m_prob) & (num2 <= f_prob)):
		return 1
	else:
		 return 0

def get_number_of_children(mother, father):
	# Need to find statistic by age bins
	# https://www.cdc.gov/nchs/data/nhsr/nhsr051.pdf Tables
	# Get number of children based on age,
	# First we get the probability of having children = (100 - P(not having children)),
	# then we multiply the probability of the number of children in each age by 100 and divide it by the above probability
	# That way we get the percent we want.

	# MOTHER
	if(mother.age <= 19):
		m_prob_1 = 0.806
		m_prob_2 = 0.179
		m_prob_3 = 0.015
		m_prob_4 = 0.0
		m_choice = np.random.choice([1,2,3,4], 1, p=[m_prob_1, m_prob_2, m_prob_3, m_prob_4])
	elif(mother.age <= 24 ):
		m_prob_1 = 0.589
		m_prob_2 = 0.303
		m_prob_3 = 0.081
		m_prob_4 = 0.027
		m_choice = np.random.choice([1,2,3,4], 1, p=[m_prob_1, m_prob_2, m_prob_3, m_prob_4])
	elif(mother.age <= 29):
		m_prob_1 = 0.355
		m_prob_2 = 0.379
		m_prob_3 = 0.195
		m_prob_4 = 0.071
		m_choice = np.random.choice([1,2,3,4], 1, p=[m_prob_1, m_prob_2, m_prob_3, m_prob_4])
	elif(mother.age <= 34):
		m_prob_1 = 0.287
		m_prob_2 = 0.368
		m_prob_3 = 0.229
		m_prob_4 = 0.116
		m_choice = np.random.choice([1,2,3,4], 1, p=[m_prob_1, m_prob_2, m_prob_3, m_prob_4])
	elif(mother.age <= 39):
		m_prob_1 = 0.222
		m_prob_2 = 0.388
		m_prob_3 = 0.226
		m_prob_4 = 0.164
		m_choice = np.random.choice([1,2,3,4], 1, p=[m_prob_1, m_prob_2, m_prob_3, m_prob_4])
	else:
		m_prob_1 = 0.177
		m_prob_2 = 0.414
		m_prob_3 = 0.239
		m_prob_4 = 0.170
		m_choice = np.random.choice([1,2,3,4], 1, p=[m_prob_1, m_prob_2, m_prob_3, m_prob_4])

	# FATHER
	if(father.age <= 19):
		f_prob_1 = 0.924
		f_prob_2 = 0.076
		f_prob_3 = 0.0
		f_prob_4 = 0.0
		f_choice = np.random.choice([1,2,3,4], 1, p=[f_prob_1, f_prob_2, f_prob_3, f_prob_4])
	elif(father.age <= 24 ):
		f_prob_1 = 0.752
		f_prob_2 = 0.176
		f_prob_3 = 0.046
		f_prob_4 = 0.026
		f_choice = np.random.choice([1,2,3,4], 1, p=[f_prob_1, f_prob_2, f_prob_3, f_prob_4])
	elif(father.age <= 29):
		f_prob_1 = 0.516
		f_prob_2 = 0.316
		f_prob_3 = 0.129
		f_prob_4 = 0.039
		f_choice = np.random.choice([1,2,3,4], 1, p=[f_prob_1, f_prob_2, f_prob_3, f_prob_4])
	elif(father.age <= 34):
		f_prob_1 = 0.344
		f_prob_2 = 0.383
		f_prob_3 = 0.183
		f_prob_4 = 0.09
		f_choice = np.random.choice([1,2,3,4], 1, p=[f_prob_1, f_prob_2, f_prob_3, f_prob_4])
	elif(father.age <= 39):
		f_prob_1 = 0.272
		f_prob_2 = 0.436
		f_prob_3 = 0.179
		f_prob_4 = 0.113
		f_choice = np.random.choice([1,2,3,4], 1, p=[f_prob_1, f_prob_2, f_prob_3, f_prob_4])
	else:
		f_prob_1 = 0.238
		f_prob_2 = 0.408
		f_prob_3 = 0.228
		f_prob_4 = 0.126
		f_choice = np.random.choice([1,2,3,4], 1, p=[f_prob_1, f_prob_2, f_prob_3, f_prob_4])

		no_of_children = int((f_choice + m_choice)/2)
		return no_of_children

def create_child(father, mother, age):
	father_age = father.age
	mother_age = mother.age

	#Create one child, may create more
	if(age):
		age = int((father_age + mother_age - int(np.random.normal(30, 4)) - int(np.random.normal(35, 4)))/2)
	if (age < 0):
		return 0
	social_class = max(father.social_class, mother.social_class)
	income = get_income(social_class)
	capital = get_capital(age, social_class, income)

	child = Person(np.random.randint(2), social_class, age, income, capital, 0)
	return child
