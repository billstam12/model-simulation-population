import random
from ages import *
from stats import *
from family import  *


def model(N):
    population = []
    while( len(population) < N ):
    	# Create a person, if it aged more than 18, run a probability of it being married, else just give his parents
    	# If he/she is create a partner for him/her and give them a child
    	# If it's a male the social class has chances of being lower, females on the other hand, tend to marry up
    	gender = np.random.randint(2)
    	social_class =  get_class()
    	age = get_age(gender)
    	marital_status = 0
    	partner = 0
    	if(age < 15):
    		inc = 0
    	else:
    		inc = get_income(social_class)
    	cap = get_capital(age, social_class, inc)
    	person = Person(gender, social_class, age, inc, cap, marital_status)
    	#print ( "Created person-id %d" % person.id)
    	marital_status = get_marital_status(gender,age)
    	if(marital_status == 1):
    		#Create another human being with different gender, if male then social class is same or lower,
    		#if female marry only to same class
    		partner = create_partner(person)
    		#Give parents to partner
    		partner_mother, partner_father = create_parents(partner)

    		if(partner_mother!=0):
    			partner.mother_id = partner_mother.id
    			population.append(partner_mother)
    		if(partner_father!=0):
    			partner.father_id = partner_father.id
    			population.append(partner_father)

    		#Marry Them
    		population.append(partner)
    		person.get_married(partner.id)
    		partner.get_married(person.id)

    		#Check for and give them Children
    		if(person.gender == 1):
    			m = person
    			f = partner
    		else:
    			m = partner
    			f = person
    		#m = mother, f = father of child
    		if(get_children_status(m, f)):
				no_of_children = get_number_of_children(m,f)
				if(no_of_children is None):
					no_of_children = 1
				for _ in range(no_of_children):
					child = create_child(person, partner, 1)
					if (child!=0):
						partner.assign_child(child.id)
						person.assign_child(child.id)
						child.assign_parents(f.id, m.id)
						population.append(child)

    	mother, father = create_parents(person)

    	population.append(person)
    	if(mother!=0):
    		person.mother_id = mother.id
    		population.append(mother)
    	if(father!=0):
    		person.father_id = father.id
    		population.append(father)

    return population
