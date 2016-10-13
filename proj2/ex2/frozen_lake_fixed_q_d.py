import gym, random

discount = 0.99

env = gym.make('FrozenLake-v0')
observation = env.reset()

acc_reward = 0

# First step south
observation, reward, done, info = env.step(1)
acc_reward = reward

for t in range(1, 100):
    env.render()
    print(observation)
    # 0 = W
    # 1 = S
    # 2 = E
    # 3 = N
    if random.random() < 0.1:
        action = env.action_space.sample()
    else:
        action = 1
    observation, reward, done, info = env.step(action)
    
    acc_reward += reward * discount**t
    
    if done:
        print("Episode finished after {} timesteps".format(t+1))
        break
print(env.observation_space.n)

print("Accumulated reward:", acc_reward)
