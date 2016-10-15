import gym, random

env = gym.make('FrozenLake-v0')
observation = env.reset()

for t in range(10000):
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
    if done:
        print("Episode finished after {} timesteps".format(t+1))
        break
