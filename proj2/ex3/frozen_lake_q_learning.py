import os, sys
import gym, random

sys.path.append(os.path.split(os.getcwd())[0])
from q_table import qTable

LEARNING_RATE = 0.1
DISCOUNT = 0.99

def epsilonGreedy(epsilon, env, obs, qtab):
    if random.random() < epsilon:
        action = env.action_space.sample()
    else:
        action = qtab.getMaxQAction(obs)
    return action

def main():
    env = gym.make('FrozenLake-v0')
    rewardWindow = [0 for _ in range(100)]
    qtab = qTable(env.observation_space.n, env.action_space.n)
    epsilon = 0.1
    for i_episode in range(8000):
        observation = env.reset()
        accumulatedReward = 0
        for t in range(10000):
            #Render enviorment
            #env.render()
            #Select action
            action = epsilonGreedy(epsilon, env, observation, qtab)
            #Perform action
            prevObs = observation
            observation, reward, done, info = env.step(action)
            accumulatedReward += reward
            #Update Q
            oldQ = qtab.getQ(prevObs, action)
            maxCurrQ = qtab.getMaxQ(observation)
            newQ = oldQ + LEARNING_RATE*(reward + DISCOUNT*maxCurrQ - oldQ)
            qtab.setQ(prevObs, action, newQ)
            #Check if episode is done
            if done:
                rewardWindow[i_episode % 100] = accumulatedReward
                break
        #Decrease exploration rate 
        epsilon *= 0.9995 # ends up at e = 0.002 after 8000 iterations
        windowAvg = 0
        for i in rewardWindow:
            windowAvg += i
        print(i_episode, " ", windowAvg)
        if windowAvg >= 78:
            break
    #print(epsilon)
    #print(qtab.table)

if __name__ == '__main__':
    main()
