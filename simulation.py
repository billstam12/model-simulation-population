import family
from stats import get_marital_status, get_income, plot_capital_to_class, gini_index
from ages import check_death
import numpy as np
import random

random.seed(1)
# This function is an SQL-like query for two people to get married
def marriage_query(person,partner):
    if(partner.marital_status == 0):
        if(partner.gender != person.gender):
            if(person.gender == 0):
                #if(partner.age in xrange((person.age/2) + 7, person.age + 8)):
                    if(partner.social_class <= person.social_class):
                        person_marital_status = get_marital_status(person.gender, person.age)
                        partner_marital_status = get_marital_status(partner.gender, partner.age)
                        if((person_marital_status) & (partner_marital_status)):
                            return 1
                    else:
                        return 0
                #else:
                #    return 0
            else:
                #if(partner.age in xrange((person.age) , person.age + 21)):
                    person_marital_status = get_marital_status(person.gender, person.age)
                    partner_marital_status = get_marital_status(partner.gender, partner.age)
                    if((person_marital_status) & (partner_marital_status)):
                        return 1
            #    else:
                    #return 0
        else:
            return 0
    else:
        return 0

# This function updates the people's classes after each iteration
def update_class(population):

    # Sort ascending based on capital
    population.sort(key=lambda x: x.capital)

    # Get classes
    T = len(population)
    l = int(0.2 * T)
    w = int(0.32 * T)
    lm = int(0.32 * T)
    um = int(0.15 * T)
    u = int(0.01 * T)

    # Set new social class
    for i, p in enumerate(population):
        if(i <= l):
            p.social_class = 1
        elif(i <= l+w):
            p.social_class = 2
        elif(i <= l+w+lm):
            p.social_class = 3
        elif(i <= l+w+lm+ um):
            p.social_class = 4
        else:
            p.social_class = 5
    return population

def run_simulation(population, years):
    for year in range(years):
        print len(population)
        for p in population:
            if(check_death(p) == 0):
                p.increment_age(1)
                # TODO:
                #Create a costs variable from data and initialize that too
                #Then adjust income and capital according to the already given data?! or make them interact?!
                #ADJUST Income

                if(p.age == 15):
                    p.income = get_income(p.social_class)
                else:
                    #p.update_income()
                    p.income += p.income * 0.01

                #ADJUST Capital
                costs = 0
                p.update_capital(0)
                #If not married, run probability of him getting get_married
                if(p.marital_status == 0):
                    #Find a potential marriage partner
                    partners = [partner for partner in population if(marriage_query(p,partner))]
                    if(partners):
                        prtnr = random.choice(partners)
                        prtnr.get_married(p)
                        p.get_married(prtnr)
                #If married  run probability of giving birth
                if((p.marital_status == 1)):
                    for person in population:
                        if(person.id == p.husband_wife):
                            if(person.gender == 0):
                                husband = person
                                wife = p
                            else:
                                wife = person
                                husband = p
                            child_status = family.get_children_status(wife, husband)
                            if(child_status == 1):
                                child = family.create_child(husband, wife, 0)
                                husband.assign_child(child.id)
                                wife.assign_child(child.id)
                                child.assign_parents(husband.id, wife.id)
                                population.append(child)
                            break
            else:
                #If that person has children, then pass its capital to his/her kids
                    children = [child for child in population if (child.id in p.children_id) ]
                    no_of_children = len(children)
                    for c in children:
                        c.pass_capital(p.capital, no_of_children)
                    population = [person for person in population if p.id != person.id]
        population = update_class( population)
    cap = plot_capital_to_class(population,len(population))
    print gini_index(np.array(cap))
