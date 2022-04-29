.. |icon| image:: /resource/icon/icon_pixel.png

.. figure:: /resource/image/splash.png
|

Neural MMO provides standard environment configurations along with scripted models, baselines pretrained with `CleanRL <https://github.com/vwxyzjn/cleanrl>`_, and training/evaluation logs hosted by `WanDB <https://wandb.ai>`_. Check the latest baseline reports `here <https://wandb.ai/jsuarez/NeuralMMO/reportlist>`_.

Training is performed on a pool of procedurally generated maps. Evaluation is performed on separate held-out maps never seen during training. Approaches that modify these parameters, alter the reward function, or substantially modify the environment configuration are not directly comparable to the baselines below.

Publications including new models should clearly indicate training scale, domain knowledge assumptions, and any other significant changes to the default configuration. Ideally, they should also include a discussion of agent behavior and supporting training/evaluation plots, overlay figures, and/or other evidence specific to the associated work.


..
        Neural MMO provides standard environment configurations along with scripted models, baselines pretrained with  and training/evaluation logs hosted by `WanDB <https://wandb.ai>`_. Check the latest baseline reports `here <https://wandb.ai/jsuarez/NeuralMMO/reportlist>`_.

|icon| Training and Evaluation
##############################

We strongly recommend setting up WanDB as per the installation guide, as it will allow you to monitor training. Compare your results to ours in this `notebook <https://github.com/neuralmmo>`_.

.. code-block:: python

  # Train from scratch
  python main.py

  # Evaluate the baseline (specify RENDER=True in config/cleanrl.py
  python evaluate.py

  # Render -- specify RENDER=True in config/cleanrl.py and then:
  python evaluate.py


Reproducing the Baseline
########################

The default config uses only 4 cores to enable users on laptops to quickly run the pretrained models. We trained the baseline model on a GCE instance with a T4 GPU and 16 physical cores (n1-standard-32). Snapshots are provided for 160M steps (~12 hours) and 320M steps (~1 day). We expect most academic labs to have similar or better hardware physically available.

What Happened to RLlib?
#######################

We used `RLlib <https://docs.ray.io/en/master/rllib.html>`_ as our sole infrastructure backend prior to the latest v1.5.4 release. It is a powerful toolkit, but its steep learning curve made it unappealing to many of our potential users. As such, we have written a number of compatibility layers that enable Neural MMO to be used with CleanRL, and it should now be quite easy to use it with most other frameworks as well. Performance is not quite on par with RLlib yet, but we have nonetheless decided to focus on our CleanRL wrapper for now since it enables many more people to start using the platform quickly. We did not have time to properly test multiple integrations for v1.5.4 but will be revisiting RLlib support shortly after the v1.6 release. For now, you can use v1.5.3 if you want better models and are comfortable working with RLlib. The commands for using it are below.

.. code-block:: python

  # Default setting
  python main.py evaluate
  python main.py --RESTORE=False

  # Or explicitly specify a setting and scale
  python main.py evaluate --config=baselines.Medium --scale=Baseline
  python main.py train --config=baselines.Medium --scale=Baseline --RESTORE=None

Load your own checkpoints by setting RESTORE=True and RESTORE_ID to the hash suffix of your checkpoint path
