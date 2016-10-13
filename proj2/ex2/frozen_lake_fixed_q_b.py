import gym, random

env = gym.make('FrozenLake-v0')
observation = env.reset()

action = 1
for t in range(10000):
    env.render()
    print(observation)
    # 0 = W
    # 1 = S
    # 2 = E
    # 3 = N
    observation, reward, done, info = env.step(action)
    if done:
        print("Episode finished after {} timesteps".format(t+1))
        break
print(env.observation_space.n)
