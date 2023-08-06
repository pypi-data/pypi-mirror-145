# NclustEnv

NclustEnv is a python toolkit that implements several environments for n-clustering and other functionalities, 
along with some default datasets and configurations. 

The motivation behind *NclustEnv* is providing quality general environments for training and benchmarking RL-based 
solutions to n-clustering.

*NclustEnv* was implemented using [NclustGen](https://github.com/PedroCotovio/nclustgen/) as the generator for 
online training, and [Gym](https://github.com/openai/gym).

*NclustEnv's* architecture focuses on an abstract class (base) that contains the core logic and API and is, consequently, 
the only part that cannot be customized.

* **The state abstraction:** *NclustEnv* separates all environment logic into a separate class *State*; this class can 
be inherited for minor modification or re-implemented for significant changes. It receives actions from the main 
class and actuates them in the graph. It is also is responsible for sampling the space and requesting a new episode 
upon a reset command. Currently, there are two implemented states, the *State* and the *Offline State* classes. 
Intuitively the *State* class handles all online environments, while the *Offline State* class is used in offline 
environments.
* **The space abstraction:** *NclustEnv* also implements its observation space *DGLHeteroGraphSpace*, which can sample 
graph configurations from a distribution used with *NclustGen* for dataset creation.
* **The metric abstraction:** The *base* class implements the linear assignment function and all other core logic 
necessary to estimate the reward and send it to the agent. However, it takes a function as a parameter so that other 
reward functions might be used. This function should return the distance between all permutations of hidden and found 
clusters. The only assumption made about the metric is that it is a distance metric; hence, the objective is to 
minimize it. *NclustEnv* currently implements **Jaccard Distance**.
* **The action abstraction:** This abstraction implements a simple action container. When an action reaches the 
environment is parsed through the *Action* class. This class should implement two properties: *action*
that contains the discrete action to take and *parameters* containing the vector of parameters for that action 
index. The *base* class takes a pointer to this action class as a parameter. Nonetheless, it is not advised that 
this action is re-implemented. Instead, to modify its behaviour, it should be inherited.

![Diagram exemplifying NclustEnv's architecture](diagNclustEnv.png)

## Installation

This tool can be installed from PyPI:

```sh
pip install nclustenv
```

## Getting started

Here are the basics, for more information check the docstrings in each class.

```python

## Use Biclustering Environment

import nclustenv

# Initialize Environment

configs = {}

env = nclustenv.make('BiclusterEnv-v0', **configs)

# Get obs space
env.observation_space

# Get action space
env.action_space

# Get state class
state = env.state

# Step in environment

obs, reward, done, info = env.step(env.action_space.sample())

# Render environment

env.render()

```

Currently four environments are implemented:

 * 'BiclusterEnv-v0';
 * 'TriclusterEnv-v0';
 * 'OfflineBiclusterEnv-v0';
 * 'OfflineTriclusterEnv-v0;


## License
[GPLv3](LICENSE)


