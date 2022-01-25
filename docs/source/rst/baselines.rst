.. |icon| image:: /resource/icon/icon_pixel.png

.. figure:: /resource/image/splash.png
|

Neural MMO provides standard environment configurations along with scripted models, baselines pretrained with `RLlib <https://docs.ray.io/en/master/rllib.html>`_, and training/evaluation logs hosted by `WanDB <https://wandb.ai>`_. Check the latest baseline reports `here <https://wandb.ai/jsuarez/NeuralMMO/reportlist>`_.

|icon| CLI
##########

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


Reproduce/Reevaluate
####################

Training is performed on a pool of procedurally generated maps. Evaluation is performed on separate held-out maps never seen during training. Approaches that modify these parameters, alter the reward function, or substantially modify the environment configuration are not directly comparable to the baselines below.

Publications including new models should clearly indicate training scale, domain knowledge assumptions, and any other significant changes to the default configuration. Ideally, they should also include a discussion of agent behavior and supporting training/evaluation plots, overlay figures, and/or other evidence specific to the associated work.

Use the commands below to reproduce the associated baseline. The default scale file expects a 32 core machine and one GPU (we use an RTX 3080), which can process around 7 years of simulated agent data per day of training. This setting was chosen as a midpoint reasonably available to most academic labs and serious independent researchers -- comparable machines can be built for significantly less than $10,000 or rented for a few dollars per hour. Training takes 3-4 days and most behaviors emerge within the first 24 hours.

.. code-block:: python

  # Default setting
  python main.py evaluate
  python main.py --RESTORE=False

  # Or explicitly specify a setting and scale
  python main.py evaluate --config=baselines.Medium --scale=Baseline
  python main.py train --config=baselines.Medium --scale=Baseline --RESTORE=None

Load your own checkpoints by setting RESTORE=True and RESTORE_ID to the hash suffix of your checkpoint path
