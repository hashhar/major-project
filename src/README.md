# osim-rl

## What?

[OpenSim](https://github.com/opensim-org/opensim-core) is a biomechanical physics environment for musculoskeletal simulations. Biomechanical community designed a range of musculoskeletal models compatible with this environment. These models can be, for example, fit to clinical data to understand underlying causes of injuries using inverse kinematics and inverse dynamics.

For many of these models there are controllers designed for forward simulations of movement, however they are often finely tuned for the model and data. Advancements in reinforcement learning may allow building more robust controllers which can in turn provide another tool for validating the models. Moreover they could help visualize, for example, kinematics of patients after surgeries.

![ARM environment](https://github.com/kidzik/osim-rl/blob/master/demo/arm.gif)
![HUMAN environment](https://github.com/kidzik/osim-rl/blob/master/demo/stand.gif)

## Objective

The objective of this challenge is to model the motor control unit in human brain. Your task to control 16 muscles in a muscloskeletal model so that the model can move forward as fast as possible.

## Installation

Requires OpenSim 4.0 - https://github.com/opensim-org/opensim-core . You can either install it from source (https://github.com/opensim-org/opensim-core/releases/tag/v4.0.0_alpha) or use conda builds as presented below.

**Requires Anaconda2**, you can get it from here https://www.continuum.io/downloads choosing version 2.7.
Below we assume that Anaconda is installed.

For the moment we only support 64-bit architecture (32-bit coming soon) on either Windows, Linux or Mac OSX. On Windows open a command prompt and type:
    
    conda create -n opensim-rl -c kidzik opensim git
    activate opensim-rl

on Linux/OSX run:

    conda create -n opensim-rl -c kidzik opensim git
    source activate opensim-rl

Then on any system you can install the RL environment with

    pip install git+https://github.com/kidzik/osim-rl.git
    
If the command `python -c "import opensim"` runs smoothly you are done! If you encounter this error

    ImportError: /home/deepart/anaconda2/envs/opensim-rl/lib/python2.7/site-packages/opensim/../../../libSimTKcommon.so.3.6: symbol _ZTVNSt7__cxx1119basic_istringstreamIcSt11char_traitsIcESaIcEEE, version GLIBCXX_3.4.21 not defined in file libstdc++.so.6 with link time reference
    
Try `conda install libgcc`

## Basic usage

To run 200 steps of environment enter `python` interpreter and run:

    from osim.env import GaitEnv

    env = GaitEnv(visualize=True)
    observation = env.reset()
    for i in range(500):
        observation, reward, done, info = env.step(env.action_space.sample())

The goal is to construct a controler, i.e. a function from the state space to action space, to maximize the total reward. Suppose you trained a neural network mapping observations (the current state of the model) to actions (muscles activations), i.e. you have a function `action = my_controler(observation)`, then 

    # ...
    total_reward = 0.0
    for i in range(500):
        # make a step given by the controler and record the state and the reward
        observation, reward, done, info = env.step(my_controler(observation)) 
        total_reward += reward
    
    # Your reward is
    print("Total reward %f" % total_reward)

## Training in keras-rl

Below we present how to train a basic controller using keras-rl. First you need to install extra packages

    conda install keras
    pip install git+https://github.com/matthiasplappert/keras-rl.git
    git clone https://github.com/stanfordnmbl/osim-rl
    
`keras-rl` is an excelent package compatible with OpenAi, which allows you to quickly build your first models!

Go to `scripts` subdirectory from this repository
    
    cd osim-rl/scripts

There are two scripts:
* `example.py` for training (and testing) an agent using DDPG algorithm. 
* `submit.py` for submitting the result to crowdAI.org

### Training

    python example.py --visualize --train --model sample
    
### Test

and for the gait example (walk as far as possible):

    python example.py --visualize --test --model sample

### Submitting

After having trained your model you can submit it using the following script

    python submit.py --model sample

This script will interact with an environment on the crowdAI.org server.

### Details

These two scripts should be enough to get you started. Soon we will provide more details regarding the `example.py` script.

## Credits

Stanford NMBL group & Stanford Mobilize Center. For details please contact @kidzik
