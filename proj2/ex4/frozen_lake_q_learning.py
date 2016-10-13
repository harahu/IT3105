import gym, random

from ..qtable import qTable

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
    env.monitor.start('/tmp/frozenlake-experiment-1')
    rewardWindow = [0 for _ in range(100)]
    qtab = qTable(env.observation_space.n, env.action_space.n)
    epsilon = 1
    for i_episode in range(8000):
        observation = env.reset()
        accumulatedReward = 0
        for t in range(100):
            #Render enviorment
            env.render()
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
                rewardWindow[i_episode % 99] = accumulatedReward
                break
        #Decrease exploration rate 
        epsilon *= 0.998
        windowAvg = 0
        for i in rewardWindow:
            windowAvg += i
        print(i_episode, " ", windowAvg)
        #if windowAvg >= 78:
            #break
    env.monitor.close()
    print(epsilon)
    print(qtab.table)

if __name__ == '__main__':
    main()
