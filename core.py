import random

max_question = 10
sick_range = list()
question_range = dict()


# set sick_range from nb_zone
# even if a sickness come from different zone
# TODO: only store id_sick in sick_range
def init_sickness_range():
    count = 0
    with open('maladies.txt') as sickness_input:
        for line in sickness_input:
            zone, id_sick, name, id_question = (item.strip() for item in line.split(';'))
            zone = zone.split(',')
            for z in zone:
                if z == nb_zone:
                    sick_range.append({'count': count, 'name': name, 'id_sick': id_sick, 'id_question': []})
                    for i in id_question.split(','):
                        sick_range[count]['id_question'].append(i)
                    count += 1


# set question_range from "zone" table
# # DEPRECATED
# def init_range_question():
#     with open('zones.txt') as zone_input:
#         for line in zone_input:
#             zone_id, name, q_list = (item.strip() for item in line.split(';'))
#             if zone_id == nb_zone:
#                 for el in q_list.split(','):
#                     question_range[el] = 1


# set question_range with all question that could be asked for the sickness in sick_range
def init_question_range():
    for sick in sick_range:
        for question in sick['id_question']:
            if question not in question_range:
                question_range[question] = 1
            else:
                question_range[question] += 1


# return a randomly selected question from question_range
def select_question():
    selected_question = 'q00'
    while selected_question not in question_range:
        rdm = random.randint(1, max_question)
        if rdm < 10:
            selected_question = 'q0' + str(rdm)
        else:
            selected_question = 'q' + str(rdm)
    return selected_question


# remove all question from question set if is_rm == True
# or only the asked question if is_rm == False
def update_question_range(is_rm, removed, question_set):
    if question_range[removed] > 1:
        question_range[removed] -= 1
    else:
        del question_range[removed]
        if removed in question_set:
            question_set.remove(removed)
    if is_rm:
        for question in question_set:
            if question_range[question] > 1:
                question_range[question] -= 1
            else:
                del question_range[question]


# remove from sick_range sickness having that question
def clear_sick_having(question_s):
    for item in sick_range:
        for elem in item['id_question']:
            if question_s in elem:
                update_question_range(True, question_s, item['id_question'])
                sick_range.remove(item)


# remove all sickness that don't have the question "question_s"
def clear_sick_not_having(question_s):
    for item in sick_range:
        is_it = False
        for elem in item['id_question']:
            if question_s in elem:
                is_it = True
        if not is_it:
            update_question_range(False, question_s, item['id_question'])
            sick_range.remove(item)


# ask selected question
# if answer is YES remove sickness from sick_range that don't have that question
# if answer is NO remove that question from question_range
def ask_question(s_q):
    with open('questions.txt') as questions_input:
        for line in questions_input:
            q_id, question = (item.strip() for item in line.split(';'))
            if q_id == s_q:
                print question
                answer = raw_input('yes/no\n')
                if answer.lower() == 'no':
                    clear_sick_having(s_q)
                elif answer.lower() == 'yes':
                    clear_sick_not_having(s_q)
                    return 1
    return 0


# rebuild sick_range and question_range from scratch
def reset_range():
    del sick_range[:]
    question_range.clear()
    init_sickness_range()
    init_question_range()


# ask questions until sick_range is has only one possible sickness
# as sickness are removed from sick_range only if answer is no
# if there is still more than one possibility, we assume the user wrongly answered
def select_sickness():
    while len(sick_range) != 1 and len(question_range) > 2:
        ask_question(select_question())
    if len(sick_range) == 1:
        print 'we assume that you have ' + sick_range[0]['name']
    else:
        print "We could not find your disease, lets try again!"
        reset_range()
        select_sickness()


# select ID zone (head/body...)
nb_zone = '2'
# set sick_range with possible sickness for that body part
init_sickness_range()
# set question_range ith possible questions for these sickness
init_question_range()
# check the question_range, ask a random question from it
# until sick_range has only one possibility
select_sickness()
