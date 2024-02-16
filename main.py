import csv
import itertools
import random

def optimalGroup(v, e, groups, considering, person1):
    optimal = 0
    og = considering[0]
    current = 0
    for g in considering:
        for person2 in groups[g]:
            score = e[v.index(person1)][v.index(person2)]
            if score >= 4:
                current += score*2
            elif score <= 0:
                score -= 10
            elif score <= 2:
                current -= score*4
        if current >= optimal:
            optimal = current
            og = g
    return og

def createGroups(v,e):
    n = (len(v)+3)//4   #number of rooms/groups
    groups = [[] for x in range(n)]
    remaining = v.copy()
    random.shuffle(remaining)
    while len(remaining) > 0:
        person = remaining[0]
        remaining.remove(person)
        considering = []
        for g in range(len(groups)):
            if groups[g] is None or len(groups[g]) < 4:  #if group is not full, consider it
                considering.append(g)
        g = optimalGroup(v, e, groups, considering, person)
        if groups[g] is None:
            groups[g] = [person]
        else:
            tmp = groups[g]
            tmp.append(person)
            groups[g] = tmp
    return groups
    #ensure optimal



def scoregroups(groups, v, e):
    score = 0
    for group in groups:
        one = v.index(group[0])
        two = v.index(group[1])
        three = v.index(group[2])
        four = v.index(group[3])
        op1 = e[one][two] + e[three][four]
        op2 = e[three][two] + e[one][four]
        op3 = e[one][three] + e[two][four]
        #if 3/2 + 1/4 greater than 1/2 + 3/4 and 1/3 + 2/4, swap two and four
        if op2 > op1 and op2 > op3:
            tmp = two
            two = four
            four = tmp
            tmp = group[1]
            group[1] = group[3]
            group[3] = tmp
        #if 1/3 + 2/4 greater than 1/2 + 3/4 and 3/2 + 1/4, swap two and three
        elif op3 > op1 and op3> op2:
            tmp = three
            three = two
            two = tmp
            tmp = group[2]
            group[2] = group[1]
            group[1] = tmp
        #1/2
        p1 = e[one][two]*2
        #3/4
        p2 = e[three][four]*2
        score += p1+p2+(op1+op2+op3-max(op1,op2,op3))
    
    #if score == 91: print(groups)

    return score


if __name__ == "__main__":
    #create vertices
    v = []
    e = []
    with open('test.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        lines = 0
        for line in csvFile:
            if lines == 0:
                for i in range(1, len(line)):
                    v.append(line[i])
                    e.append([0 for x in range(1,len(line))])
            else:
                for i in range(1, len(line)):
                    e[lines-1][i-1] = int(line[i])

            lines += 1


    scores = dict()

    for i in range(1000):
        group = createGroups(v,e)
        score = scoregroups(group, v, e)
        if score in scores:
            tmp = scores.get(score)
            tmp.append(group)
            scores[score] = tmp
        else:
            scores[score] = [group]

    scores = dict(sorted(scores.items(),reverse=True))
    top = 0
    for score in scores:
        if top >= 3: break

        if len(scores.get(score)) > 3:
            print('score:', score)
            for group in scores.get(score):
                print('\t', group)
                top += 1
                if top >= 5: break
            top += len(scores.get(score))
        else:
            print(str(score) + ":", scores.get(score))
            top += 1