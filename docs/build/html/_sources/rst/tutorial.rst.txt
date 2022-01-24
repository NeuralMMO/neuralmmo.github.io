.. |icon| image:: /resource/icon/icon_pixel.png

.. role:: python(code)
    :language: python

.. figure:: /resource/image/splash.png

The baselines repository includes a number of examples. We recommend that new users follow the installation guide first and then run each example while reading this walkthrough.

|icon| Minimal Example
######################

Simulates and renders a small environment inhabited by scripted agents. This example should be self-explanatory to those familiar with the standard OpenAI gym interface -- with a few exceptions. First, the environment itself computes actions for scripted agents. This is to enable easier usage with RLlib and will likely change once RLlib provides better support for scripted models. Second, the env.terminal() function returns additional logging information about the simulation. This will be explored in later examples

.. literalinclude:: ../../../../baselines/demos/minimal.py

Run the example script from /baselines:

.. code-block:: python

   python -m demos.minimal

Open the client executable for your platform (downloaded separately as per setup) to render the environment.

.. figure:: /resource/demos/minimal.png

This is the only example for which we will show boilerplate code. The full source for all examples is available in /baselines/demos

|icon| Config Classes
#####################

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

|icon| Scripted API
###################

Neural MMO provides compact tensor observations that are difficult to integrate with scripted policies and change from version to version. We therefore provide a simple wrapper class that enables users to extract named attributes without direct dependence on the underlying structure of observations, documented here:

.. toctree::
  :maxdepth: 4

  nmmo.scripting

As an example, we implement a simple scripted agent that jumps into lava upon spawning:

.. literalinclude:: ../../../../baselines/demos/scripting.py
  :pyobject: LavaAgent

We will occasionally modify the set of available attributes. In these instances, we will publish upgrade scripts upon request. We will provide individual guidance via Discord in cases where larger changes are needed. 

|icon| Rewards & Tasks
######################

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

|icon| Skill Rating
###################

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

A difference of 100 SR implies 99.7 percent confidence that the given policy is better than the opponent. Within around 20 simulations, the skill rating estimate is confident that the Combat policy is better than the Forage policy.

.. code-block:: python

   Meander: 1e-09   Forage: 3.1827   Combat: 12.730
   Meander: 1e-09   Forage: 6.3592   Combat: 24.626
   Meander: 1e-09   Forage: 9.5378   Combat: 35.717
   Meander: 1e-09   Forage: 12.716   Combat: 46.050
   Meander: 1e-09   Forage: 15.887   Combat: 55.679
   Meander: 1e-09   Forage: 19.037   Combat: 64.664
   Meander: 1e-09   Forage: 22.155   Combat: 73.066
   Meander: 1e-09   Forage: 25.229   Combat: 80.941
   Meander: 1e-09   Forage: 28.249   Combat: 88.340
   Meander: 1e-09   Forage: 31.207   Combat: 95.313
   Meander: 1e-09   Forage: 34.098   Combat: 101.90
   Meander: 1e-09   Forage: 36.917   Combat: 108.14
   Meander: 1e-09   Forage: 39.661   Combat: 114.06
   Meander: 1e-09   Forage: 42.330   Combat: 119.70
   Meander: 1e-09   Forage: 44.922   Combat: 125.08
   Meander: 1e-09   Forage: 47.439   Combat: 130.23
   Meander: 1e-09   Forage: 49.882   Combat: 135.15
   Meander: 1e-09   Forage: 52.252   Combat: 139.88
   Meander: 1e-09   Forage: 54.552   Combat: 144.42
   Meander: 1e-09   Forage: 56.784   Combat: 148.79

|icon| Rendering and Overlays
#############################

Neural MMO opens a WebSocket server upon the first call to env.render() which connects to the Unity3D client. The client loads game map data upon connection, which may take up to a minute (but typically only a few seconds if you open the client after launching the server). 


The Neural MMO client provides several overlays as tools to help users understand both how their agents are behaving and how they interpret the world. You can write your own using the overlay API:

.. literalinclude:: ../../../../baselines/demos/overlays.py
  :pyobject: Lifetime
  
Include custom overlays by subclassing the environment as follows:

.. literalinclude:: ../../../../baselines/demos/overlays.py
  :pyobject: LifetimeOverlayEnv
 
The overlay will be provided to the client automatically and available using the specified "lifetime" registry name. In this example, green regions correspond to areas traversed by longer-lived agents and could help indicate the quality of local resource distributions.

The client includes some default overlays, such as counts/exploration, which is computed by splatting the agent's current position to the map. You can do more impressive things with a bit more compute. For example, the baselines repository provide the tileValues and entityValues overlays, which simulate an agent on every tile and computes the value function with respect to local tiles/entities. Note that overlays making use of network internals are not defined for scripted models.

|icon| Training
###############

The default baseline was trained using 32 cores and 1 RTX 3080 for 3-4 days. This scale was chosen to represent what should be reasonably available to most academic labs, but is not required for meaningful research on the platform. This demo provides a config trainable on a 4 core, 1 GPU device in under 24 hours, surpassing random performance within the first hour of training (around 50 epochs) and a strong scripted baseline within 10 hours (around 400 epochs).

The environment config rewards agents for survival (-1 for death) and exploration (0.05 per tile from spawn) as follows:

.. literalinclude:: ../../../../baselines/demos/training.py
  :pyobject: SmallExploreEnv
 
.. literalinclude:: ../../../../baselines/demos/training.py
  :pyobject: SmallExploreConfig

This demo also provides scripted baseline evaluations

 .. code-block:: python

   python -m demos.training baselines

.. code-block:: text

   Average Scripted Forage Lifetime: 73.78125
   Average Scripted Meander Lifetime: 34.125
   Note that these are noisy estimates on one env

Train from scratch:

 .. code-block:: python

   python -m demos.training neural

We strongly recommend setting up WanDB as per the installation guide, as it will allow you to monitor training. Compare your results to ours in this `notebook <https://github.com/neuralmmo>`_.

Next Steps
##########

If you've made it this far, you're ready to use the platform in your own research. Join the Discord for support and consider our open call for research if applicable. We also recommend checking out the baselines to get an idea of what has been done so far.

