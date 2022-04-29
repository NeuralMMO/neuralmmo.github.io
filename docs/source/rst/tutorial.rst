.. |icon| image:: /resource/icon/icon_pixel.png

.. role:: python(code)
    :language: python

.. figure:: /resource/image/splash.png

|

The baselines repository includes a number of examples. We recommend that new users follow the installation guide first and then run each example while reading this walkthrough.

|icon| Minimal Example
######################

Simulates and renders a small environment inhabited by scripted agents. This example should be self-explanatory to those familiar with the standard OpenAI gym interface -- with a few exceptions. First, the environment itself computes actions for scripted agents. This is to enable easier usage with RLlib and will likely change once RLlib provides better support for scripted models. Second, the env.terminal() function returns additional logging information about the simulation. This will be explored in later examples

.. literalinclude:: ../../../../baselines/demos/minimal.py

Run the example script from /baselines:

.. code-block:: python

   python -m demos.minimal

Open the client executable for your platform (downloaded separately as per setup) to render the environment.

.. figure:: /resource/image/minimal.png

|

This is the only example for which we will show boilerplate code. The full source for all examples is available in /baselines/demos

|icon| Config Classes
#####################

Neural MMO provides a base Config with Small, Medium, and Large presets and a set of game systems. Enable game systems by subclassing a preset. For example, the default config when unspecified is:

.. code-block:: python

  class DefaultConfig(nmmo.config.Medium, nmmo.config.AllGameSystems):
      pass

Maps will be generated upon environment instantiation according the the provided config and cached at PATH_MAPS for reuse. If you are actively tweaking TERRAIN_ generation parameters, remember to delete the old maps between runs or set FORCE_MAP_GENERATION=True. Generate previews with --GENERATE_MAP_PREVIEWS.

.. figure:: /resource/image/map.png

|

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

.. literalinclude:: ../../../../baselines/demos/scripted.py
  :pyobject: LavaAgent

.. code-block:: python

   python -m demos.scripted

We will occasionally modify the set of available attributes. In these instances, we will publish upgrade scripts upon request. We will provide individual guidance via Discord in cases where larger changes are needed. 

|icon| Rewards & Tasks
######################

By default, Neural MMO provides a reward signal of -1 for dying and 0 for everything else. You may override this reward function and have full access to game and player state in doing so. For example, to add an additional reward signal of 0.1 per player defeated:

.. literalinclude:: ../../../../baselines/demos/rewards_and_tasks.py
  :pyobject: PlayerKillRewardEnv

One drawback of such definitions is the potential for reward farming. For example, agents may learn to do nothing but fight other weaker agents, completely ignoring other interesting elements of the environment. At the same time, combat could be difficult to learn without a dedicated signal. Our task API resolves this problem by enabling you to set fixed milestones instead of repeatedly farmable rewards:

.. literalinclude:: ../../../../baselines/demos/rewards_and_tasks.py
  :pyobject: player_kills

.. literalinclude:: ../../../../baselines/demos/rewards_and_tasks.py
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

.. code-block:: python

   python -m demos.evaluate_sr

A difference of 100 SR implies 99.7 percent confidence that the given policy is better than the opponent. By default, evaluation anchors Combat to 1500 SR as a baseline. Within around 10 simulations, the skill rating estimate is confident that the Forage baseline is better than the Meander baseline.

.. code-block:: python

   Meander: 990.44   Forage: 1009.5   Combat: 1500
   Meander: 982.45   Forage: 1017.5   Combat: 1500
   Meander: 975.69   Forage: 1024.2   Combat: 1500
   Meander: 969.91   Forage: 1030.0   Combat: 1500
   Meander: 964.90   Forage: 1035.0   Combat: 1500
   Meander: 960.49   Forage: 1039.4   Combat: 1500
   Meander: 956.58   Forage: 1043.3   Combat: 1500
   Meander: 953.07   Forage: 1046.8   Combat: 1500
   Meander: 949.89   Forage: 1050.0   Combat: 1500
   Meander: 946.99   Forage: 1052.9   Combat: 1500

|icon| Terrain Generation
#########################

Neural MMO provides a config hook for custom terrain generaton. Override the base class and single-map generation method:

.. literalinclude:: ../../../../baselines/demos/terrain_generation.py
  :pyobject: CustomMapGenerator

Note that the nmmo.Terrain class is populated with materials at runtime -- these properties are not available before instantiating a map generator. Finally, set the MAP_GENERATOR property to your custom class and run the demo:

.. literalinclude:: ../../../../baselines/demos/terrain_generation.py
  :pyobject: CustomTerrainGeneration

Run the demo:

.. code-block:: python

   python -m demos.terrain_generation

.. figure:: /resource/image/custom_map.png

Note that the PNG preview generator crops TERRAIN_BORDER tiles by default to omit the lava border.

.. figure:: /resource/image/custom_map_render.png

|

**Common Bugs**
  - Ensure that generated maps contain a TERRAIN_BORDER wide lava border. This is used to pad agent observations.
  - The spawn area must be unobstructed. Making the lava border too wide (e.g. off-by-one) will obstruct all spawn tiles.

|icon| Rendering and Overlays
#############################

Neural MMO opens a WebSocket server upon the first call to env.render() which connects to the Unity3D client. The client loads game map data upon connection, which may take up to a minute (but typically only a few seconds if you open the client after launching the server). 


The Neural MMO client provides several overlays as tools to help users understand both how their agents are behaving and how they interpret the world. You can write your own using the overlay API:

.. literalinclude:: ../../../../baselines/demos/overlays.py
  :pyobject: Lifetime
  
Include custom overlays by subclassing the environment as follows:

.. literalinclude:: ../../../../baselines/demos/overlays.py
  :pyobject: LifetimeOverlayEnv

.. code-block:: python

   python -m demos.overlays

The overlay will be provided to the client automatically and available using the specified "lifetime" console command. In this example, green regions correspond to areas traversed by longer-lived agents and could help indicate the quality of local resource distributions.

.. figure:: /resource/image/custom_overlay.png

|

The client includes some default overlays, such as counts/exploration, which is computed by splatting the agent's current position to the map. You can do more impressive things with a bit more compute. For example, the baselines repository provide the tileValues and entityValues overlays, which simulate an agent on every tile and computes the value function with respect to local tiles/entities. Note that overlays making use of network internals are not defined for scripted models.

|icon| Next Steps
#################

If you've made it this far, you're ready to use the platform in your own research. Join the Discord for support and consider our open call for research if applicable. We also recommend checking out the baselines to get an idea of what has been done so far.
