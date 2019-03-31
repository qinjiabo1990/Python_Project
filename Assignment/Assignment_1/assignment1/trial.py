"""
def judgement(x):
    while x != 1 and x != 2 and x !=3:
        print('wrong')
        x = input ('your answer: ')
    return x
"""

"""

import partners
potential_partners = partners.Partners()
 
gender='1'
sexual_pref='2'
height='1'
height_pref='2'
persionality_score=22

if gender == '1':
    gender_list = 'male'
elif gender == '2':
    gender_list = 'female'
elif gender == '3':
    gender_list = 'other'

if sexual_pref == '1':
    sexual_pref_list = 'male'
elif sexual_pref == '2':
    sexual_pref_list = 'female'
elif sexual_pref == '3':
    sexual_pref_list = 'other'

if height == '1':
    height_list = 'tall'
elif height == '2':
    height_list = 'medium'
elif height == '3':
    height_list = 'short'

if height_pref == '1':
    height_pref_list = 'tall'
elif height_pref == '2':
    height_pref_list = 'medium'
elif height_pref == '3':
    height_pref_list = 'short'

result=(gender_list, sexual_pref_list, height_list, height_pref_list, persionality_score)

closest_score = float("inf")
while potential_partners.available() :
    if  (result[1] == potential_partners.get_gender()
        and result[0] == potential_partners.get_sexual_pref()):
        if abs(result[4] - potential_partners.get_personality_score()) < closest_score:
            closest_score = abs(result[4] - potential_partners.get_personality_score())
            if  (result[3] == potential_partners.get_height()
                 and result[2] == potential_partners.get_height_pref()):
                print (potential_partners.get_name())
"""
import partners

def physical_characteristics_question(question, answer1, answer2, answer3, answer):
    print(question)
    print('1)', answer1,
          '\n2)', answer2,
          '\n3)', answer3)
    answer = input('Please enter your answer: ')
    while answer != '1' and answer != '2' and answer !='3':
        print('Your input is invalid')
        answer = input ('Please enter your answer: ')
    return answer






def personality_question(question, answer):
    print(question)
    print('1) Yes'
          '\n2) Most of the time'
          '\n3) Neutral'
          '\n4) Some times'
          '\n5) No')
    answer = input('Please enter your answer: ')
    while answer != '1' and answer != '2' and answer !='3' and answer !='4' and answer != '5':
        print('Your input is invalid')
        answer = input ('Please enter your answer: ')
    return answer


def match(gender, sexual_pref, height, height_pref, personality_score):
    potential_partners = partners.Partners()
    if gender == 1:
        gender_list = 'male'
    elif gender == 2:
        gender_list = 'female'
    elif gender == 3:
        gender_list = 'other'

    if sexual_pref == 1:
        sexual_pref_list = 'male'
    elif sexual_pref == 2:
        sexual_pref_list = 'female'
    elif sexual_pref == 3:
        sexual_pref_list = 'other'

    if height == 1:
        height_list = 'tall'
    elif height == 2:
        height_list = 'medium'
    elif height == 3:
        height_list = 'short'

    if height_pref == 1:
        height_pref_list = 'tall'
    elif height_pref == 2:
        height_pref_list = 'medium'
    elif height_pref == 3:
        height_pref_list = 'short'
    result=(gender_list, sexual_pref_list, height_list, height_pref_list, personality_score)
    closest_score = float("inf")
    while potential_partners.available() :
        if  (result[1] == potential_partners.get_gender()
             and result[0] == potential_partners.get_sexual_pref()):
            if abs(result[4] - potential_partners.get_personality_score()) < closest_score:
                closest_score = abs(result[4] - potential_partners.get_personality_score())
                if  (result[3] == potential_partners.get_height()
                     and result[2] == potential_partners.get_height_pref()):
                    print (potential_partners.get_name())


                    
#personal details
#Gender
gender_int=int(physical_characteristics_question('what is your gender?', 'male', 'female', 'other', 'gender'))
print('\n')

#sexual preference
sexual_pref_int=int(physical_characteristics_question('what is your sexual preference?', 'male', 'female', 'other', 'sexual_pref'))
print('\n')

#height
height_int=int(physical_characteristics_question('what is your height?', 'tall', 'medium', 'short', 'height'))
print('\n')

#height_preference
height_pref_int=int(physical_characteristics_question('what height do you prefer your partner to be?', 'tall', 'medium', 'short', 'height_pref'))
print('\n')



#introduction
introduction_int=int(personality_question('Do you find it easy to introduce yourself to ohter people?', 'introduction'))
print('\n')

#conversation
conversations_int=int(personality_question('Do you usually initiate conversations?', 'conversations'))
print('\n')

#curiousity
curiousity_int=int(personality_question('Do you often do something out of sheer curiosity?', 'curiousity'))
print('\n')

#communication
communication_int=int(personality_question('Do you prefer being out with a large group of friends rather than \nspending time on your own?', 'communication'))
print('\n')

personality_score = (introduction_int + conversations_int + curiousity_int + communication_int) * 2


match(gender_int, sexual_pref_int, height_int, height_pref_int, personality_score)















        
