import gym
import gym_gazebo
import tensorflow as tf
import argparse
import copy
import sys

# Use algorithms from baselines
from baselines.acktr.acktr_cont import learn
from baselines.acktr.policies import GaussianMlpPolicy
from baselines.acktr.value_functions import NeuralNetValueFunction
from baselines.common import set_global_seeds


def train_setup(job_id, l, gam, t_per_batch, des_kl, num_t,  max_pathl,  step):
    env = gym.make('GazeboModularScara3DOF-v3')
    initial_observation = env.reset()
    print("Initial observation: ", initial_observation)
    env.render()

    seed=0
    set_global_seeds(seed)
    env.seed(seed)

    with tf.Session(config=tf.ConfigProto()) as session:
        ob_dim = env.observation_space.shape[0]
        ac_dim = env.action_space.shape[0]
        with tf.variable_scope("vf"):
            vf = NeuralNetValueFunction(ob_dim, ac_dim)
        with tf.variable_scope("pi"):
            policy = GaussianMlpPolicy(ob_dim, ac_dim)

        optim_metric = learn(env,
            policy=policy, vf=vf,
            gamma=gam,
            lam=l,
            timesteps_per_batch=t_per_batch,
            desired_kl=des_kl,
            num_timesteps=num_t,
            animate=False,
            save_model_with_prefix='ros1_acktr_H',
            restore_model_from_file='')

        if optim_metric > 0:
                optim_metric = optim_metric * (-1)
        else:
                optim_metric = abs(optim_metric)
        return optim_metric

def main(job_id, params):
    return train_setup(job_id, params['lam'], params['gamma'], params['timesteps_per_batch'], params['desired_kl'], params['num_timesteps'],  params['max_pathlength'],  params['stepsize'])