.. |icon| image:: /resource/icon/icon_pixel.png

.. role:: python(code)
    :language: python

.. figure:: /resource/image/splash.png

|

..
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
   python main.py render #--NUM_GPUS=0 if no CUDA

Download the latest client `here <https://github.com/neuralmmo/client/releases>`_ (WSL users: do this on your Windows host). Start the demo and run the executable for your platform in client/UnityClient/. After a few seconds, the demo console will show a connection message and the client will load the map. The on-screen instructions demonstrate how to pan and zoom. You can also click on agents to examine their skill levels. The in-game console (which you can toggle with tab) gives you access to a number of overlay visualiztions.

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
   
   cd environment && pip install -e .[all]

   python main.py render
   ./client.sh

|icon| Gallary
##############

Rendered Map and UI
*******************

.. figure:: /resource/image/rendered_map.png

.. figure:: /resource/image/stats.png

| 

Overlays
********

.. figure:: /resource/image/overlays.png

| 

.. _collaborations:

|icon| Call for Collaborations
##############################

We are launching an open call for research on the platform in early February. Check back soon for news!