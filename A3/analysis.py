# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0.2
    return answerDiscount, answerNoise

def question3a():
    #how much agent values future rewards, high means future important
    answerDiscount = 0.1 #low so it goes for closest
    
    #how likely to follow the path, low noise means more likely to follow path
    answerNoise = 0 #risk of cliff
    
    #postive means it wants to live for longer
    answerLivingReward = 0 #encourage to finish task

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    answerDiscount = 0.1 #close reward
    answerNoise = 0.1 #avoid cliff
    answerLivingReward = 0 #encourage to finish task
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    answerDiscount = 0.5 #prefer higher reward
    answerNoise = 0 #risk cliff
    answerLivingReward = 0.1 #encourage to travel to better reward
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    answerDiscount = 0.5 #prefer higher reward
    answerNoise = 0.1 #avoid the cliff
    answerLivingReward = 0.1 #encourage to travel to better reward
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answerDiscount = 0 #to not be motivated by reward
    answerNoise = 0.5 #avoid cliff
    answerLivingReward = 0.3 #continue living
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question8():
    answerEpsilon = None
    answerLearningRate = None
    return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
