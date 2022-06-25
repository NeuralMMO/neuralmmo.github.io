.. |icon| image:: /resource/icon/icon_pixel.png

.. figure:: /resource/image/splash.png
|

Neural MMO provides standard environment configurations along with scripted models, baselines pretrained with `CleanRL <https://github.com/vwxyzjn/cleanrl>`_, and training/evaluation logs hosted by `WanDB <https://wandb.ai>`_. Check the latest baseline reports `here <https://wandb.ai/jsuarez/NeuralMMO/reportlist>`_ and older RLlib baselines `here <https://wandb.ai/jsuarez/NeuralMMO-Old/reportlist>`_.

|icon| Training and Evaluation
##############################

To evaluate the latest baseline's SR (skill rating) verses scripted opponents:

.. code-block:: python
  :caption: Evaluate the latest baseline

  python evaluate.py

  # Render the baseline (client launched separately, see Installation)
  python evaluate.py render

The baseline was trained on single Titan Xp GPU with 32 cores for 3 days. Performance is stable after 500M agent steps, equal to approximately 9 years of gameplay or 2.5 days of training. We strongly recommend setting up WanDB as per the installation guide, as it will allow you to monitor dozens of useful training and evaluation statistics.

.. code-block:: python
  :caption: Reproduce the baseline from scratch

  python main.py

  # Check that your install is working with a couple cores
  python main.py debug

Your latest checkpoint will be saved to model.pt. Note that the default config specifies 1B agent steps. You can kill jobs early once SR is stable ("Agent" in the WanDB logs). The scripted combat baseline is fixed to 1500 SR. Exceeding this threshold means your agent is better than the scripted combat baseline, according to average performance across a variety of tasks including exploration, foraging, and combat.

|icon| Emulation + CleanRL
##########################

Our main file is adapted from a minimal single-file PPO implementation from `CleanRL <https://github.com/vwxyzjn/cleanrl>`_ built for single-agent learning on Atari with flat observations and discrete actions. Neural MMO has large agent populations and heirarchical IO (observation + action) spaces. v1.5.4+ includes emulation layers that make Neural MMO look as simple as Atari from the perspective of RL frameworks (i.e. CleanRL).

There are a number of associated features, including padding and flattening the observations (they're unpacked directly within the neural net), flattening the action space (to a single multi-discrete space, reconstructed in the environment), and splitting multiagent environments into a list of single-agent environments. The main file for our baselines enables these features with `nmmo.integrations.cleanrl_vec_envs`, which accepts a list env configs as its sole parameter.

The only major limitation compared to the previous RLlib trainer is that the env must have a fixed number of agents. Introducing a variable agent population results in a variable batch size in which the average trajectory is 90 percent padding. This results in instability during training, even when masking the loss (because of a much smaller effective batch size). Creating sufficiently large, constant-size batches without padding would require a complete rewrite of CleanRL and would not be efficient if the core design of CleanRL were maintained. Instead, we respawn agents during training and randomize the number of agents per training environment. This mitigates curriculum issues associated with training on a fixed-size population.

|icon| Reporting Your Results
#############################

Training is performed on a pool of procedurally generated maps. Evaluation is performed on separate held-out maps never seen during training. Approaches that modify these parameters, alter the reward function, or substantially modify the environment configuration are not directly comparable to the baselines below.

Publications including new models should clearly indicate training scale, domain knowledge assumptions, and any other significant changes to the default configuration. Ideally, they should also include a discussion of agent behavior and supporting training/evaluation plots, overlay figures, and/or other evidence specific to the associated work.


What Happened to RLlib?
#######################

We used `RLlib <https://docs.ray.io/en/master/rllib.html>`_ as our sole infrastructure backend prior to v1.5.4. It is a powerful toolkit, but its steep learning curve made it unappealing to many of our potential users. As such, we have written a number of compatibility layers that enable Neural MMO to be used with CleanRL, and it should now be quite easy to use it with most other frameworks as well. Performance is not quite on par with RLlib yet, but we have nonetheless decided to focus on our CleanRL wrapper for now since it enables many more people to start using the platform quickly. We did not have time to properly test multiple integrations for v1.5.4 but will be revisiting RLlib support shortly after the v1.6 release. For now, you can use v1.5.3 if you want better models and are comfortable working with RLlib. The commands for using it are below.

.. code-block:: python

  # Default setting
  python main.py evaluate
  python main.py --RESTORE=False

  # Or explicitly specify a setting and scale
  python main.py evaluate --config=baselines.Medium --scale=Baseline
  python main.py train --config=baselines.Medium --scale=Baseline --RESTORE=None

Load your own checkpoints by setting RESTORE=True and RESTORE_ID to the hash suffix of your checkpoint path
