import sys, os
import gym, random
import matplotlib.pyplot as plt

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
    env = gym.make('Taxi-v1')
    rewardWindow = [0 for _ in range(100)]
    qtab = qTable(env.observation_space.n, env.action_space.n)
    epsilon = 0.1
    ep = []
    rew = []
    for i_episode in range(8000):
        observation = env.reset()
        action = epsilonGreedy(epsilon, env, observation, qtab)
        accumulatedReward = 0
        for t in range(100):
            #Render enviorment
            #env.render()
            #Perform action
            prevObs = observation
            observation, reward, done, info = env.step(action)
            accumulatedReward += reward
            #Select action
            prevAct = action
            action = epsilonGreedy(epsilon, env, observation, qtab)
            #Update Q
            oldQ = qtab.getQ(prevObs, prevAct)
            actQ = qtab.getQ(observation, action)
            newQ = oldQ + LEARNING_RATE*(reward + DISCOUNT*actQ - oldQ)
            qtab.setQ(prevObs, prevAct, newQ)
            #Check if episode is done
            if done:
                rewardWindow[i_episode % 100] = accumulatedReward
                ep.append(i_episode)
                rew.append(accumulatedReward)
                break
        #Decrease exploration rate 
        epsilon *= 0.9995
        windowAvg = 0
        for i in rewardWindow:
            windowAvg += i
        print(i_episode, " ", windowAvg, end='\r')
        if windowAvg >= 970:
            break
    plt.plot(ep, rew)
    plt.xlabel('episode')
    plt.ylabel('reward')
    plt.title('Taxi SARSA')
    plt.grid(True)
    plt.savefig("sarsa.png")
    plt.show()

if __name__ == '__main__':
    main()
