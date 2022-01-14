.. |icon| image:: /resource/icon/icon_pixel.png

.. role:: python(code)
    :language: python

.. figure:: /resource/image/splash.png

**News:** We have released an open call for collaborations following several recent usability improvements and a successful pilot project

**Quick links:** `Github <https://github.com/neuralmmo>`_ | `Discord <https://discord.gg/BkMmFUC>`_ | `Twitter <https://twitter.com/jsuarez5341>`_ | `NeurIPS 2021 <http://arxiv.org/abs/2110.07594>`_

|icon| Introduction
###################

Neural MMO is an open-source and computationally accessible research platform that simulates populations of agents in procedurally generated virtual worlds. We support basic foraging tasks involving a few agents for a couple of minutes, thousand-agent joint survival + exploration + combat over multiple hours, and everything between.

.. raw:: html

    <center>
      <video width=100% height="auto" nocontrols autoplay muted loop>
        <source src="_static/zoom.mp4" type="video/mp4">
        Your browser does not support this mp4.
      </video>
    </center>

|
Environments provide a standard PettingZoo API and support though our community `Discord <https://discord.gg/BkMmFUC>`_

.. code-block:: python

   from nmmo import Env

   env = Env(config=None) # Default environment. Keep reading for config options
   obs = env.reset()

   while True:
       actions = {} # Compute with your model
       obs, rewards, dones, infos = env.step(actions)

Our goal is to support a broad base of multiagent research that would be impractical or impossible to conduct on other environments. The project was most recently `published <http://arxiv.org/abs/2110.07594>`_ at NeurIPS 2021 (full list).

.. youtube:: hYYA8_wFF7Q
   :width: 100%

|
.. code-block:: text

  @proceedings{NEURIPS2021,
    author = {Joseph Suarez, Yilun Du, Clare Zhu, Igor Mordatch, Phillip Isola},
    booktitle = {Advances in Neural Information Processing Systems},
    title = {The Neural MMO Platform for Massively Multiagent Research},
    url = {http://arxiv.org/abs/2110.07594},
    volume = {33},
    year = {2021}
  }

In the presentation above, I coin the term **Foundation Policies**, analogous to **Foundation Models**, as a grounding motivation for investing in environment complexity and generality. A key contribution of Neural MMO is to do so efficiently and interpretably by adapting techniques from classic MMO development for deep learning.

The associated poster provides a high level overview of the workflow intended to support most research on the platform. For a more thorough walkthrough of features and usage, read on.

.. figure:: /resource/figure/web/NMMO_NeurIPS2021_Poster.jpg

|icon| Installation
###################

Official support: Ubuntu 20.04, WSL, and MacOS. Tested with Anaconda Python 3.9

.. code-block:: python
   :caption: Packaged installation
   
   # Install NMMO with baseline dependencies
   pip install nmmo[rllib]
   
   # Clone baselines repository. Optional but recommended: setup WanDB integration.
   git clone --depth=1 https://github.com/neuralmmo/baselines nmmo-baselines
   echo YOUR_WANDB_API_KEY > nmmo-baselines/wandb_api_key

   #Run a quick demo (download client below)
   python main.py demo

Download the latest client `here <https://github.com/neuralmmo/client/releases>`_ (WSL users: do this on your Windows host). Start the demo and run the executable for your platform in client/UnityClient/. After a few seconds, the demo console will show a connection message and the client will load the map.

**Required RLlib patch:** Add `custom_metrics[k] = filt; continue` after line 175 in your RLlib metrics file (usually ~/anaconda3/lib/python3.8/site-packages/ray/rllib/evaluation/metrics.py)

**Troubleshooting:** If you are training on GPU and get an IndexError error on self.device, set gpu_ids=[0] in ray/rllib/policy/torch_policy.py:150 (typically in ~/anaconda3/lib/python3.8/site-packages)

**Support:** Post in #support on the `[Discord] <https://discord.gg/BkMmFUC>`_. Seriously, do this. Do not raise Github issues for support. You will get a reply much faster (often instantly) on Discord.

You can also install headless or entirely from source (WanDB setup and RLlib patch still required)

.. code-block:: python
   :caption: Headless setup for training

   pip install nmmo[rllib]
   git clone --depth=1 https://github.com/neuralmmo/baselines nmmo-baselines
 
.. code-block:: python
   :caption: Setup from source for developers

   mkdir neural-mmo && cd neural-mmo

   git clone --depth=1 https://github.com/neuralmmo/environment
   git clone --depth=1 https://github.com/neuralmmo/baselines
   git clone --depth=1 https://github.com/neuralmmo/client
   
   cd environment && pip install -e .[rllib]

   python main.py demo
   ./client.sh

|icon| Creating Environments
############################

Neural MMO provides a base Config with Small, Medium, and Large presets and a set of game systems. Enable game systems by subclassing a preset. For example, the default config when unspecified is:

.. code-block:: python

  class DefaultConfig(nmmo.config.Medium, nmmo.config.AllGameSystems):
      pass

Maps will be generated upon environment instantiation according the the provided config and cached at PATH_MAPS for reuse. If you are actively tweaking TERRAIN_ generation parameters, remember to delete the old maps between runs or set FORCE_MAP_GENERATION=True.

.. figure:: /resource/image/map.png
   :caption: Enable image previews with TERRAIN_RENDER. Downscale from 128x128 px/tile by setting the MAP_PREVIEW_DOWNSCALE factor

   Example map from resource/maps/procedural-small/map1/map.png

Customize terrain generation and game balance by overriding preset and game system configuration parameters:

.. code-block:: python

  class ExampleCustomConfig(nmmo.config.Small, nmmo.config.Resource, nmmo.config.Progression):
      # Example core config customization
      NMOB                    = 512
      NENT                    = 128

      # Custom map storage location
      PATH_MAPS               = 'maps/custom'

      # Number of maps generated
      # EVALUATE ON HELD-OUT MAPS!
      # See baselines/config.py for an example
      NMAPS                   = 32

      # Terrain generation parameters
      TERRAIN_CENTER             = 512
      TERRAIN_WATER              = 0.40
      TERRAIN_GRASS              = 0.55

      # Progression system rebalancing
      PROGRESSION_BASE_XP_SCALE           = 10
      PROGRESSION_CONSTITUTION_XP_SCALE   = 2

The config docs provide a full list of parameters:

.. toctree::
  :maxdepth: 4

  nmmo.config

Not all game configurations lend themselves to balanced and interesting gameplay. We recommend spending some time watching the baseline agents and reviewing the game wiki's description of the vanilla mechanics. Once you're familiar, we encourage more creative modding beyond what the configs provide. Come chat on `Discord <https://discord.gg/BkMmFUC>`_ if you're doing something cool!

|icon| Rendering and Overlays
#############################

Your first call to env.render() will open a WebSocket server. Open the executable for your platform in client/UnityClient or, if you are on Unix, use the provided environment/client.sh script. You should see connection printouts and, after a few seconds, the map should render in the client (note that large maps require a good workstation).


.. figure:: /resource/image/ui.png

  You should see this view once the map loads

The on-screen instructions demonstrate how to pan and zoom in the environment. You can also click on agents to examine their skill levels. The in-game console (which you can toggle with the tilde key) give you access to a number of overlays.

.. image:: /resource/image/overlays.png

The counts (exploration) overlay is computed by splatting the agent's current position to a counts map. Most other overlays are computed analogously. However, you can also do more impressive things with a bit more compute. For example, the baselines repository provide the tileValues and entityValues overlays, which simulate an agent on every tile and computes the value function with respect to local tiles/entities. Note that some overlays, such as counts and skills, are well-defined for all models. Others, such as value function and attention, do not exist for scripted baselines.

See the User API for details on how to write your own overlays.

The server will take a few seconds to load the pretrained policy and connect to the client.

|icon| Demos
############

The baselines repository includes a number of runnable examples documented below


Minimal Example
***************

Simulates and renders a small environment inhabited by scripted agents. This example should be self-explanatory to those familiar with the standard OpenAI gym interface -- with a few exceptions. First, the environment itself computes actions for scripted agents. This is to enable easier usage with RLlib and will likely change once RLlib provides better support for scripted models. Second, the env.terminal() function returns additional logging information about the simulation. This will be explored in later examples

.. literalinclude:: ../../../../baselines/demos/minimal.py

Run the example script from /baselines:

.. code-block:: python

   python -m demos.minimal

Open the client executable for your platform (downloaded separately as per setup) to render the environment.

.. figure:: /resource/demos/minimal.png

This is the only example for which we will show boilerplate code. The full source for all examples is available in /baselines/demos

Rewards & Tasks
***************

By default, Neural MMO provides a reward signal of -1 for dying and 0 for everything else. You may override this reward function and have full access to game and player state in doing so. For example, to add an additional reward signal of 0.1 per player defeated:

.. literalinclude:: ../../../../baselines/demos/rewards_and_tasks_api.py
  :pyobject: PlayerKillRewardEnv

One drawback of such definitions is the potential for reward farming. For example, agents may learn to do nothing but fight other weaker agents, completely ignoring other interesting elements of the environment. At the same time, combat could be difficult to learn without a dedicated signal. Our task API resolves this problem by enabling you to set fixed milestones instead of repeatedly farmable rewards:

.. literalinclude:: ../../../../baselines/demos/rewards_and_tasks_api.py
  :pyobject: player_kills

.. literalinclude:: ../../../../baselines/demos/rewards_and_tasks_api.py
  :pyobject: PlayerKillTaskConfig

Agents will now receive a reward of 2 for defeating one and three players -- a strong incentive to score a kill and a weaker incentive to continue down the path of combat, which must then be balanced against other competing incentives. This reward will be added to the reward() method and also to the infos dict returned by step() for use with methods requiring per-task information.

.. code-block:: python

   python -m demos.rewards_and_tasks

.. code-block:: text

   Task Reward: 0.531, Tasks Complete: 0.266

Note that this API is considered somewhat of an advanced feature -- it provides access to full game state and requires users to peruse the associated source code to take full advantage.

Skill Rating
************

Absolute reward is a poor metric of performance in open-ended multiagent settings because environment difficulty is dependent on the skill of other agents. Skill ranking algorithms allow us to instead compute the relative performance of different policies within the same shared world.

OpenSkill wrapper for estimating rank from a series of scores from different policies:

.. literalinclude:: ../../../../baselines/demos/evaluate_sr.py
  :pyobject: rank

.. literalinclude:: ../../../../baselines/demos/evaluate_sr.py
  :pyobject: OpenSkillRating

The results of each environment simulation are treated as a single game, and several are required to obtain reasonable skill rating estimates. We therefore include a quick ray wrapper for running several environments in parallel:

.. literalinclude:: ../../../../baselines/demos/evaluate_sr.py
  :pyobject: parallel_simulations

We use a larger scale config to more closely match the baseline setting:

.. literalinclude:: ../../../../baselines/demos/evaluate_sr.py
  :pyobject: Config

|icon| Scripting and Classic AI
###############################

Neural MMO provides compact tensor observations that are difficult to integrate with scripted policies and change from version to version. We therefore provide a simple wrapper class that enables users to extract named attributes without direct dependence on the underlying structure of observations, documented here:

.. toctree::
  :maxdepth: 4

  nmmo.scripting

We will occasionally modify the set of available attributes. In these instances, we will publish upgrade scripts upon request. We will provide individual guidance via Discord in cases where larger changes are needed. 

baselines/scripted includes a set of scripted models and utilities. You may find these useful as references for creating your own models.


|icon| Baselines
################

Provides pretrained and scripted models with all associated training code for the latter. Demonstrates usage with `RLlib <https://docs.ray.io/en/master/rllib.html>`_ and `WanDB <https://wandb.ai>`_ for logging and visualization. Note that these are dependencies only of the basline and not of the core environment.

CLI
***

The main file for the baselines and demo project includes commands for training, evaluation, and rendering. To view documentation:

.. code-block:: python

  python main.py --help

.. code-block:: text

  NAME
      main.py --help - Neural MMO CLI powered by Google Fire

  SYNOPSIS
      main.py --help - COMMAND

  DESCRIPTION
      Main file for the RLlib demo included with Neural MMO.

      Usage:
         python main.py <COMMAND> --config=<CONFIG> --ARG1=<ARG1> ...

      The User API documents core env flags. Additional config options specific
      to this demo are available in projekt/config.py.

      The --config flag may be used to load an entire group of options at once.
      Select one of the defaults from projekt/config.py or write your own.

  COMMANDS
      COMMAND is one of the following:

       evaluate
         Evaluate a model against EVAL_AGENTS models

       generate
         Manually generate maps using the current --config setting

       render
         Start a WebSocket server that autoconnects to the 3D Unity client

       train
         Train a model using the current --config setting


Reevaluating/Reproducing the Baseline
************************
.. code-block:: python
  :caption: Training and evaluation through Ray Tune with WanDB logging

  python main.py evaluate --config=baselines.Medium --scale=Baseline
  python main.py train --config=baselines.Medium --scale=Baseline --RESTORE=None

  # The config/scale defaults already actually point to the baseline
  python main.py evaluate
  python main.py train --RESTORE=None


If a job crashes, you can resume training with `--RESUME=True --RESTORE=None`

Evaluation Methods
##################

Evaluation in open-ended massively multiagent settings is akin to that in the real world. Unlike in most single-agent and some multiagent environments, there is no absolute metric of performance. We therefore provide two evaluation options: *tournaments*, which measure relative performance against various opponents, and *self-contained* simulations, which measure qualitative behaviors.

Tournaments
***********

This evaluation mode is the default as of v1.5.2. Agents train against many copies of themselves but are evaluated against scripted opponents with different policies. These evaluation tournaments are run parallel to training, allowing you to monitor progress relative to scripted baselines in real time.

Self-Contained
**************

This is the classic evaluation setup used in older versions of Neural MMO measures policy quality according to a number of summary stats collected over the course of training. It suffers from a lack of ability to compare policies directly, but it is still well-suited to artificial life work targeting emergent behaviors in large populations. These statistics are automatically sent to WanDB.
