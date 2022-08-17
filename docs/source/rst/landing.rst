.. |icon| image:: /resource/icon/icon_pixel.png

.. role:: python(code)
    :language: python

.. raw:: html

    <center>
      <video width=100% height="auto" nocontrols autoplay muted loop>
        <source src="_static/zoom.mp4" type="video/mp4">
        Your browser does not support this mp4.
      </video>
    </center>

|

..
  **News:** We have released an open call for collaborations following several recent usability improvements and a successful pilot project

**Quick links:** `Github <https://github.com/neuralmmo>`_ | `Baselines <https://wandb.ai/jsuarez/NeuralMMO/reportlist>`_ | `NeurIPS 2021 Paper <https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/44f683a84163b3523afe57c2e008bc8c-Abstract-round1.html>`_ | `Discord <https://discord.gg/BkMmFUC>`_ | `Twitter <https://twitter.com/jsuarez5341>`_

`NeurIPS 2022 Competition: <https://www.aicrowd.com/challenges/neurips-2022-the-neural-mmo-challenge>`_ Train teams of agents to compete in a battle royale verses other participants with $20,000 in prizes sponsored by Parametrix.AI and cloud credits sponsored by AWS.

|icon| Introduction
###################

Neural MMO is an open-source and computationally accessible research platform that simulates populations of agents in procedurally generated virtual worlds. We support basic foraging tasks involving a few agents for a couple of minutes, thousand-agent joint survival + exploration + combat over multiple hours, and everything between. Our goal is to support a broad base of multiagent research that would be impractical or impossible to conduct on other environments.

.. code-block:: python

   from nmmo import Env

   env = Env(config=None) # Default environment. Keep reading for config options
   obs = env.reset()

   while True:
       actions = {} # Compute with your model
       obs, rewards, dones, infos = env.step(actions)

Environments provide a standard PettingZoo API. Join our community Discord and post in `#support <https://discord.gg/GhDQT4zKKW>`_ for help (do not raise Github issues for support). See the quick links above for source code, baselines, latest publications, social media, and news!

.. youtube:: hYYA8_wFF7Q
   :width: 100%

|
.. code-block:: text

  @inproceedings{NEURIPS DATASETS AND BENCHMARKS2021_44f683a8,
    author = {Suarez, Joseph and Du, Yilun and Zhu, Clare and Mordatch, Igor and Isola, Phillip},
    booktitle = {Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks},
    editor = {J. Vanschoren and S. Yeung},
    pages = {},
    title = {The Neural MMO Platform for Massively Multiagent Research},
    url = {https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/44f683a84163b3523afe57c2e008bc8c-Paper-round1.pdf},
    volume = {1},
    year = {2021}
  }

In the presentation above, I coin the term **Foundation Policies**, analogous to **Foundation Models**, as a grounding motivation for investing in environment complexity and generality. A key contribution of Neural MMO is to do so efficiently and interpretably by adapting techniques from classic MMO development for deep learning.

The associated poster provides a high level overview of the workflow intended to support most research on the platform. For a more thorough walkthrough of features and usage, read on.

.. figure:: /resource/figure/web/NMMO_NeurIPS2021_Poster.jpg

|

|icon| Installation
###################

Official support: Ubuntu 20.04, WSL, and MacOS. Tested with Anaconda Python 3.9

.. code-block:: python
   :caption: Packaged installation
   
   # Install NMMO with baseline dependencies (quotes for mac compatibility).
   pip install "nmmo[cleanrl]"
   
   # Clone baselines repository. Optional but recommended: setup WanDB integration.
   git clone https://github.com/neuralmmo/baselines nmmo-baselines
   echo YOUR_WANDB_API_KEY > nmmo-baselines/wandb_api_key

   #Run a quick demo (download client below)
   python -m demos.minimal

Download the latest client `here <https://github.com/neuralmmo/client/releases>`_ (WSL users: do this on your Windows host). Start the demo and run the executable for your platform in client/UnityClient/. After a few seconds, the demo console will show a connection message and the client will load the map. The on-screen instructions demonstrate how to pan and zoom. You can also click on agents to examine their skill levels. The in-game console (which you can toggle with tab) gives you access to a number of overlay visualiztions.

.. code-block:: python
   :caption: Setup from source for developers (slow without --depth=1)

   mkdir neural-mmo && cd neural-mmo

   git clone https://github.com/neuralmmo/environment
   git clone https://github.com/neuralmmo/baselines
   git clone https://github.com/neuralmmo/client
   
   echo YOUR_WANDB_API_KEY > baselines/wandb_api_key
   cd environment && pip install -e .[all]

|icon| Gallery
##############

Perspective and UI
******************

.. figure:: /resource/image/minimal.png

| 

Overlays
********

.. figure:: /resource/image/overlays.png

| 

Multiscale Terrain Generation
*****************************

.. figure:: /resource/image/large_map.png

|

Overhead Render
***************

.. figure:: /resource/image/rendered_map.png

| 

.. _collaborations:

|icon| Call for Collaborations
##############################

Following the platform's `publication <https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/44f683a84163b3523afe57c2e008bc8c-Abstract-round1.html>`_ in NeurIPS 2021, we are excited to announce an open call for collaborations!

Eligibility *(at least one of)*
   - You are affiliated with an academic lab (professor/PhD student/postdoc)
   - You have previously published in a relevent area (RL, PCG, etc)
   - You are a corporate researcher with substantial freedom to publish
   - You have a substantial engineering background and want to help with core development

Excepting prospective developers, your objectives should include first-author publication at a reputable venue. We (Joseph Suarez and Phillip Isola, MIT) would be included in the least important author slots. Compared to working independently, we can offer:

Benefits:
   - Extended support and custom features
   - Project-specific guidance, having developed the platform
   - An invitation to our monthly group meetings
   - Scoop insurance (we avoid duplicate projects)
   - Introductions to other practitioners in our community

Contact me via Discord or email (in the publication) if you are interested.
