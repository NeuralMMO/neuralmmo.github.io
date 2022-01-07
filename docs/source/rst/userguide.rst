.. |icon| image:: /resource/icon/icon_pixel.png

.. role:: python(code)
    :language: python

.. figure:: /resource/image/splash.png

|icon| Introduction
###################
`[Github] <https://github.com/jsuarez5341/neural-mmo>`_ | `[Discord] <https://discord.gg/BkMmFUC>`_ | `[Twitter] <https://twitter.com/jsuarez5341>`_

Neural MMO is an open-source and computationally accessible research platform that simulates populations of agents in procedurally generated virtual worlds. Environments are configurable for a variety of problems and scales -- from basic foraging tasks involving a few agents for a couple of minutes to joint survival, exploration, and combat over a couple of hours with a thousand agents.

.. raw:: html

    <center>
      <video width=100% height="auto" nocontrols autoplay muted loop>
        <source src="_static/zoom.mp4" type="video/mp4">
        Your browser does not support this mp4.
      </video>
    </center>

The platform provides a Python API for scripting agents and `RLlib <https://docs.ray.io/en/master/rllib.html>`_  + `WanDB <https://wandb.ai>`_ integrations for reinforcement learning, evaluation, and logging. An interactive 3D client provides futher visualization tools for debugging and showcasing agent policies. The guides below contain everything you need to get started. We also run a community `Discord <https://discord.gg/BkMmFUC>`_ for support, discussion, and dev updates. This is the best place to contact me.

.. figure:: /resource/figure/web/NMMO_NeurIPS2021_Poster.jpg

Neural MMO at NeurIPS 2021
**************************

Our latest `[publication] <http://arxiv.org/abs/2110.07594>`_ summarizing the platform's capabilities and baselines. In the associated presentation, I coin the term **Foundation Policies**, analogous to **Foundation Models**, as a grounding motivation for investing in environment complexity and generality. A key contribution of Neural MMO is to do so efficiently and interpretably by adapting techniques from classic MMO development for deep learning.

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

Citation to be updated upon the release of NeurIPS 2021 proceedings. See Updates for a full list of demos, publications, presentations, and patch notes.

Installation
************

Official support: Ubuntu 20.04, Windows 10 + WSL, and MacOS

.. code-block:: python
   :caption: Setup from source with baselines(Recommended). Windows + WSL Users: Install the server and baselines on WSL and the client on Windows.

   mkdir neural-mmo && cd neural-mmo

   git clone --depth=1 https://github.com/neuralmmo/environment
   git clone --depth=1 https://github.com/neuralmmo/baselines
   git clone --depth=1 https://github.com/neuralmmo/client
   
   cd environment && pip install -e .[rllib]

.. code-block:: python
   :caption: Headless setup

   pip install nmmo[rllib]
   git clone --depth=1 https://github.com/neuralmmo/baselines nmmo-baselines
   

**Required Baselines Configuration**
   - Edit baselines/config.py as per the instructions therein to match your hardware specs
   - Create a file wandb_api_key in baselines and paste in your WanDB API key. This new integration is now so important to logging and evaluation that we are requiring it by default. Do not commit this file.
   - Add `custom_metrics[k] = filt; continue` after line 175 in your RLlib metrics file (usually ~/anaconda3/lib/python3.8/site-packages/ray/rllib/evaluation/metrics.py). This is an RLlib limitation which we hope to resolve in the next version.

**Troubleshooting**
  - If you are training on GPU and get an IndexError error on self.device, set gpu_ids=[0] in ray/rllib/policy/torch_policy.py:150 (typically in ~/anaconda3/lib/python3.8/site-packages)
  - Most compatibility issues with the client and unsupported operating systems can be resolved by opening the project in the Unity Editor
  - If you want full commit history, clone without ``--depth=1`` (including in scripts/setup.sh for the client). This flag is only included to cut down on download time
  - The master branch will always contain the latest stable version. Each previous version release is archived in a separate branch. Dev branches are not nightly builds and may be flammable.

Problems? Post in #support on the `[Discord] <https://discord.gg/BkMmFUC>`_. Seriously, do this. Do not raise Github issues for support. You will get a reply much faster (often instantly) on Discord.

Baselines CLI
*************

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

       render
         Start a WebSocket server that autoconnects to the 3D Unity client

       train
         Train a model using the current --config setting

|icon| Environment Configuration
################################

Neural MMO provides a base Config with Small, Medium, and Large presets and a set of game systems. Enable game systems by subclassing a preset. For example, the default config when unspecified is:

.. code-block:: python

  class DefaultConfig(nmmo.config.Medium, nmmo.config.AllGameSystems):
      pass

Maps will be generated upon environment instantiation according the the provided config. Note that maps are cached by defaultHere are some examples:

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



A few important notes:
   - Maps are cached at PATH_MAPS for reuse. If you are actively tweaking TERRAIN_ generation parameters, you **will** forget to delete the old maps between runs. Set FORCE_MAP_GENERATION=True to avoid this.
   - Not all game configurations lend themselves to balanced and interesting gameplay. We recommend spending some time watching the baseline agents and reviewing the game wiki's description of the vanilla mechanics before diving too deep into custom configurations.

The environment is fully open-source, and we encourage more creative modding beyond what the configs provide. Come chat on `Discord <https://discord.gg/BkMmFUC>`_ if you're doing something cool!


|icon| Create Policies
######################

Scripted API
************

Neural MMO provides compact tensor observations that are difficult to integrate with scripted policies and change from version to version. We therefore provide a simple wrapper class that enables users to extract named attributes without direct dependence on the underlying structure of observations, documented here:

.. toctree::
  :maxdepth: 4

  nmmo.infra.scripting

We will occasionally modify the set of available attributes. In these instances, we will publish upgrade scripts upon request. We will provide individual guidance via Discord in cases where larger changes are needed.

Each Neural MMO release will include a set of `[scripted baselines] <https://github.com/NeuralMMO/baselines/blob/main/scripted/baselines.py>`_. You may find these useful as references for creating your own models. You are also free to leverage any of the utility classes included with these baselines, but do note that these are not part of the official API and may change from version to version.

RLlib Integration
*****************

The baseline model and associated training and evaluation code in projekt/rllib_wrapper.py demonstrate how to use RLlib with Neural MMO. Note that RLlib is not a hard dependency of the platform: Neural MMO provides an otherwise-standard Gym interface extended for multiagent. That said, all of our trained baselines rely on RLlib, and we strongly suggest using it unless you fancy writing your own segmented trajectory collectors, hierarchical observation/action processing, variable agent population batching, etc.

To re-evaluate or re-train the pretrained baseline:

.. code-block:: python
  :caption: Training and evaluation through Ray Tune with WanDB logging

  python main.py evaluate --config=CompetitionRound1
  python main.py train --config=CompetitionRound1 --RESTORE=None

If a job crashes, you can resume training with `--RESUME=True --RESTORE=None`

|icon| Evaluate Agents
######################

Evaluation in open-ended massively multiagent settings is akin to that in the real world. Unlike in most single-agent and some multiagent environments, there is no absolute metric of performance. We therefore provide two evaluation options: *tournaments*, which measure relative performance against various opponents, and *self-contained* simulations, which measure qualitative behaviors.

Tournaments
***********

This evaluation mode is the default as of v1.5.2 and is being used in the current `competition <https://www.aicrowd.com/challenges/the-neural-mmo-challenge>`_. Agents train against many copies of themselves but are evaluated against scripted opponents with different policies. As of this minor update, these evaluation tournaments are run parallel to training, allowing you to monitor progress relative to scripted baselines in real time. You can submit your agents to the live AICrowd `competition <https://www.aicrowd.com/challenges/the-neural-mmo-challenge>`_ for evaluation against other users. After the competition, we will integrate additional users' bots (provided we are able to obtain permission to do so) into the main repository.

Self-Contained
**************

This is the classic evaluation setup used in older versions of Neural MMO measures policy quality according to a number of summary stats collected over the course of training. It suffers from a lack of ability to compare policies directly, but it is still well-suited to artificial life work targeting emergent behaviors in large populations. These statistics are automatically sent to WanDB.

Evaluation Distribution
***********************

Neural MMO provides three sets of evaluation settings:

**Training Maps:** Evaluate on the same maps used for training. This is standard practice in reinforcement learning. *Enable by setting the GENERALIZE flag to False*

**Evaluation Maps:** Evaluate on a set of held-out maps drawn from the training map *distribution* generated using different random seeds. *This is the default setting*

**Transfer Maps:** Evaluate large-map models on small maps (hard) or small-map models on large maps (very hard). *Enable by setting the appropriate --config*

|icon| Rendering and Overlays
#############################

**v1.5.2-3:** Overlays are broken due to a Ray Tune bug. We're working on fixing this and have pushed the version regardless because of the importance of Ray Tune and WanDB evaluation. We're working on this. In the meanwhile, you can copy your checkpoint files over to a v1.5.1 install if needed. The models are compatible, and the v1.5.2 client should work fine too.

Rendering the environment requires launching both a server and a client. To launch the server:

.. code-block:: python

  python main.py render --config=CompetitionRound1

| **Linux/MacOS:** Launch *client.sh* in a separate shell or click the associated executable
| **Windows:** Launch neural-mmo-client/UnityClient/neural-mmo.exe from Windows 10

The server will take a few seconds to load the pretrained policy and connect to the client.

.. figure:: /resource/image/ui.png

  You should see this view once the map loads

The on-screen instructions demonstrate how to pan and zoom in the environment. You can also click on agents to examine their skill levels. The in-game console (which you can toggle with the tilde key) give you access to a number of overlays. Note that the LargeMaps config requires a good workstation to render and you should avoid zooming all the way out.

.. image:: /resource/image/overlays.png

The counts (exploration) overlay is computed by splatting the agent's current position to a counts map. Most other overlays are computed analogously. However, you can also do more impressive things with a bit more compute. For example, the tileValues and entityValues overlays simulate an agent on every tile and computes the value function with respect to local tiles/entities. Note that some overlays, such as counts and skills, are well-defined for all models. Others, such as value function and attention, do not exist for scripted baselines.

Writing your own overlays is simple. You can find the source code for general overlays (those computable by scripted baselines) in neural_mmo/forgetrinity/overlay.py. RLlib-specific overlays that require access to the trainer/model are included in projekt/rllib_wrapper.py. Details are also included in the User API.
