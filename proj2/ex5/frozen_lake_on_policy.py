import os, sys
import gym, random
import matplotlib.pyplot as plt
import json

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
    
    # Excercise 5 specific (load qTable from ex3)
    ex3qtab = qTable(env.observation_space.n, env.action_space.n)
    f = open("ex3qtable.json", 'r').read()
    ex3qtab.table = json.loads(f)
    epsilon = 0.1
    ep = []
    rew = []
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
            currQ = qtab.getQ(observation, ex3qtab.getMaxQAction(observation)) # ex5 specific
            newQ = oldQ + LEARNING_RATE*(reward + DISCOUNT*currQ - oldQ)
            qtab.setQ(prevObs, action, newQ)
            #Check if episode is done
            if done:
                rewardWindow[i_episode % 100] = accumulatedReward
                ep.append(i_episode)
                break
        #Decrease exploration rate 
        epsilon *= 0.9995 # ends up at e = 0.002 after 8000 iterations
        windowAvg = 0
        for i in rewardWindow:
            windowAvg += i
        rew.append(windowAvg/100)
        print(i_episode, " ", windowAvg, end='\r')
        if windowAvg >= 78:
            break
    plt.plot(ep, rew)
    plt.xlabel('episode')
    plt.ylabel('reward')
    plt.title('Frozen Lake on policy')
    plt.grid(True)
    plt.savefig("op.png")
    plt.show()

if __name__ == '__main__':
    main()
