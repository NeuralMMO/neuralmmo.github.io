.. |icon| image:: /resource/icon.png

|icon| v2.0
###########

.. card::
   :img-background: /../_static/banner.png

|icon| v1.6
###########

.. figure:: /resource/1-6/client.png
.. figure:: /resource/1-6/overlays.png
.. figure:: /resource/1-6/large_map.png
.. figure:: /resource/1-6/overhead.png

.. dropdown:: Materials

   Competition: `NeurIPS 2022 <https://www.aicrowd.com/challenges/neurips-2022-the-neural-mmo-challenge>`_

   The Economy Update -- largest to date!
      - 150+ items: 16 unique items are available in level 1-10 variants
      - Rebalanced Combat: rock-paper-scissors interaction between styles, simpler and more balanced damage formula
      - 5 new skills: Fishing, Hunting, Prospecting, Carving, and Alchemy focus on gathering items used for survival and in combat
      - Weapons and Tools: All 5 new skills and the 3 combat skills have unique weapons and tools to boost their efficacy
      - Trade: Buy and sell items on a global market
      - Expanded game wiki with full details

|icon| v1.5
###########

.. figure:: /resource/1-5/1-5_env.png

.. dropdown:: Materials

   Competitions
      - `IJCAI 2022 <https://www.aicrowd.com/challenges/ijcai-2022-the-neural-mmo-challenge>`_
      - `AICrowd 2021 <https://www.aicrowd.com/challenges/the-neural-mmo-challenge>`_

   Videos
      - `Neural MMO v1.5.3 NeurIPS 2021 <https://www.youtube.com/watch?v=hYYA8_wFF7Q>`_
      - `Neural MMO v1.5 Trailer <https://youtu.be/d1mj8yzjr-w>`_

   Poster
   :download:`[Poster] </resource/1-5/neurips_poster.pdf>` `The Neural MMO Platform for Massively Multiagent Research <http://arxiv.org/abs/2110.07594>`_ (NeurIPS 2021) (v1.5.3)

   Presentations
      - `The IJCAI 2022 Neural MMO Challenge <https://docs.google.com/presentation/d/1PJ8a8nFMfZ0AoiM25VoXQ__uzovrjlODIlqFSjQuCOk/edit?usp=sharing>`_ (IJCAI 2022) (1.5.1)
      - `[Slides] <https://docs.google.com/presentation/d/1CCYZNBWV6u_EW0h_NeL_BnJzBx_sMv--Q8P4TACM3Bs/edit?usp=sharing>`_ `[Video] <https://www.youtube.com/watch?v=9V6EvSEMREg>`_ Neural MMO: Building a Massively Multiagent Research Platform with Ray and RLlib (Ray Summit 2021, Online) (v1.5.0)
      - `[Slides] <https://docs.google.com/presentation/d/1HYdoe3btw1USWaufBO1yuqFIOg-XW8E2wX0vZal0LtY/edit?usp=sharing>`_ Neural MMO: A Saga in Deep Reinforcement Learning (English Week 2021, IUT Vannes) (v1.5.0)

   **v1.5.5:** Better Baselines
      - Slightly exceeds performance of the scripted combat model with CleanRL
      - Training takes 1 GPU, 32 cores, and <3 days
      - Includes checkpoints and training code

   **v1.5.4:** CleanRL Integration
      - Emulation layer that makes Neural MMO look like a simpler environment:
         - Multiagent -> N single-agent environments
         - Flat observations and actions
         - Fixed horizons
      - Single-file CleanRL baseline using the above wrappers
      - Evaluation tools

   **v1.5.3:** PettingZoo Integration

   **v1.5.2:** Ray Tune and WanDB Integrations
      - Trinity:
         - Added support for simulations with both scripted and trained agents
         - Added ability to name scripted agents based on their policy
      - Embyr:
         - Minor aesthetic changes to prefer a flat-shaded style
         - Broke some overlay features :/ RLlib bug under construction
      - Projekt
         - Replaced Bokeh dashboard with WanDB integration
         - Wrapped RLlib trainers in Ray Tune to enable parallel evaluation during training
         - Added Skill Rating (SR) metric for direct comparison to scripted baselines
         - Changed batching mode to agent steps, yielding a large policy improvement

   **v1.5.1:** Competition Build
      - Blade:
         - Modularized configs to enable dynamic environment customization
         - Reworked terrain generation to create more diverse terrain
         - Increased default map and population size
         - Added competition configs and baselines
      - Trinity: Formal API for scripted agents using the same observation interface as learned models
      - Embyr: Culled vertices and recalculated normals to improve terrain smoothness and performance

   **v1.5:** Large maps, Dashboard, Scripted Baselines
      - Blade: Full rework to support large environments and scripted players/NPCs
         - Map representation
            - Terrain generation for large maps
            - Environment caching to enable fast resets
            - Tiles are now limited to one occupying agent
            - Reworked tile material enum and properties
         - NPCs
            - Passive: Meanders around the map
            - Neutral: Meanders around the map until attacked, then fights back
            - Hostile: Actively hunts and attacks players and other NPCs
            - Level ranges and spawning locations are configurable for all NPC types
            - Navigation based on A* search
         - Scripted Baselines
            - Extension of the NPC AI module to support scripted player policies
            - Fixed-horizon food/water min-max search with Dijkstra's algorithm and dynamic programming backends
            - Intentional exploration capabilities enable broad coverage of large and small maps
         - Equipment
            - NPCs spawn with chestplates/platelegs of a level appropriate for their skills
            - Players/NPCs wearing equipment drop it upon death
            - Players automatically equip any items better than their current items
            - Equipment provides a large bonus to defense
            - Reworked combat formulas to account for this new system
      - Trinity: New home for non-neural-specific infrastructure and tools
         - Serialized observations
            - Maintains a flat tensor representation of the environment state
            - This representation is kept synchronous with the game state representation
            - Each entity (Player/Tile) is represented as discrete and continuous vectors
            - Observations are computed by slicing from tensor representations without traversing game objects
            - Discrete values are flat-indexed for ease of use in embedding layers
         - Evaluation
            - Runs the given model on multiple maps and aggregates data for the dashboard
            - Outputs a tabular summary of the results for baselines and publications
            - Usable on training maps, held-out evaluation maps (default), and transfer maps
         - Dashboard
            - Environment log function records customizable data for customizable plot types whenever an agent dies
            - Data is aggregated during training and at the end of evaluation
            - Bokeh dashboard is built using the aggregated data for the specified plot types
            - Dashboard is rendered in an interactive browser session
      - Ethyr: Simplified attribute processing
         - The Trinity additions flatten the bottom layer of the observation hierarchy
         - This removes a slow loop and significant complexity from IO embedding/unembed modules
         - We have standardized on the Recurrent baseline architecture for this release
      - Embyr: Full rework to support large environments and scripted players/NPCs
         - Map representation
            - All terrain representation code has been rewritten using the performant Unity Entity Component System
            - Tiles are loaded into and welded together in chunks
            - Lava/water assets have been replaced with more performant variants
         - Visuals
            - Tile textures are now configurable with the hifi (default)/medfi/lofi command
            - Attack animations have been replaced with more distinctive and aesthetic assets
            - A graphical bug causing sharp normals in some tile models has been fixed
            - UI and console retouched to match the new website theme
      - Projekt: Demo code for evaluation, overlays and logging
         - Unified command-line utility for map generation, training, evaluation, visualization, and rendering
         - Experiment config for canonical large/small baseline tasks
         - Single-file ~400 line RLlib wrapper/demo
         - Non-RLlib specific code has been moved to Trinity
         - Improved overall code cohesion and quality

|icon| v1.4
###########

.. figure:: /resource/1-4/1-4_env.png

.. dropdown:: Materials

   ICML 2020 LAOW Workshop :download:`[Poster] </resource/1-4/icml2020_poster.pdf>` :download:`[Paper] </resource/1-4/icml2020_paper.pdf>` Ingredients for Massively Multiagent Artificial Intelligence Research

   RLlib Support and Overlays
      - Blade: Minor API changes have been made for compatibility with Gym and RLlib
         - Exposed the registerOverlay() and getValStim() methods for writing custom overlays
         - Environment reset method now returns only obs instead of (obs, rewards, dones, infos)
         - Environment obs and dones are now both dictionaries keyed by agent ids rather than agent game objects
         - The IO modules from v1.3 now delegates batching to the user, e.g. RLlib. As such, several potential sources of error have been removed
         - A bug allowing agents to use melee combat from farther away than intended has been fixed
         - Minor range and damage balancing has been performed across all three combat styles
      - Trinity: This module has been temporarily shelved
         - Now hosts the Twisted server code for interfacing with the client
         - Core functionality has been ported to RLlib in collaboration with the developers
         - We are working with the RLlib developers to add additional features essential to the long-term scalability of Neural MMO
         - The Trinity/Ascend namespace will likely be revived in later infrastructure expansions. For now, the stability of RLlib makes delegating infrastructure pragmatic to enable us to focus on environment development, baseline models, and research
      - Ethyr: Proper NN building blocks for complex worlds
         - Streamlined IO, memory, and attention modules for use in building PyTorch policies
         - A high-quality pretrained baseline reproducible at the scale of a single desktop
      - Embyr: Overlay shaders for visualizing learned policies
         - Pressing tab now brings up an in-game console
         - A help menu lists several shader options for visualizing exploration, attention, and learned value functions
         - Shaders are rendered over the environment in real-time with partial transparency
         - It is no longer necessary to start the client and server in a particular order
         - The client no longer needs to be relaunched when the server restarts
         - Agents now turn smoothly towards their direction of movement and targeted adversaries
         - A graphical bug causing some agent attacks to render at ground level has been fixed
         - Moved twistedserver.py into the main neural-mmo repository to better separate client and server
         - Confirmed working on Ubuntu, MacOS, and Windows + WSL
      - /projekt: Demo code fully rewritten for RLlib
         - The new demo is much shorter, approximately 250 lines of code
         - State-of-the-art LSTM + self-attention based policy trained with distributed PPO
         - Batched GPU evaluation for real-time rendering
         - Trains in a few hours on a reasonably good desktop (5 rollout worker cores, 1 underutilized GTX 1080Ti GPU)
         - To avoid introducing RLlib into the base environment as a hard dependency, we provide a small wrapper class over Realm using RLlib's environment types
         - Attempted to migrate from a pip requirements.txt to Poetry for streamlined dependency management, but Poetry is still too buggy at the present.
         - We have migrated configuration to Google Fire for improved command line argument parsing

|icon| v1.3
###########

.. dropdown:: Materials

   AAMAS 2020 `[Extended Abstract] <http://ifaamas.org/Proceedings/aamas2020/pdfs/p2020.pdf>`_ `[arXiv Full Paper] <https://arxiv.org/abs/2001.12004>`_ `[Demo] <https://youtu.be/DkHopV1RSxw>`_ `[Presentation] <https://underline.io/lecture/167-neural-mmo-v1.3-a-massively-multiagent-game-environment-for-training-and-evaluating-neural-networks>`_ Neural MMO v1.3: A Massively Multiagent Game Environment for Training and Evaluating Neural Networks 

   OxAI VR & AI Virtual Seminar in NeosVR: `[Slides] <https://docs.google.com/presentation/d/1GLrvm9ShqDz5whoC0_LUhu0uxnefTQksuE9qc1hXfjg/edit?usp=sharing>`_ `[Presentation] <https://youtu.be/8iPTrzhB9Yk?t=312>`_ Neural MMO v1.3 Pre-release

   `Update Slides <https://docs.google.com/presentation/d/1tqm_Do9ph-duqqAlx3r9lI5Nbfb9yUfNEtXk1Qo4zSw/edit?usp=sharing>`_ Neural MMO v1.3 

   Prebuilt IO Libraries
      - Blade: We have improved and streamlined the previously unstable and difficult to use IO libraries and migrated them here. The new API provides framework-agnostic IO.inputs and IO.outputs functions that handle all batching, normalization, serialization. Combined with the prebuilt IO networks in Ethyr, these enable seamless interactions with an otherwise complex structured underlying environment interface. We have made corresponding extensions to the OpenAI Gym API to support variable length actions and arguments, as well as to better signal episode boundaries (e.g. agent deaths). The Quickstart guide has been updated to cover this new functionality as part of the core API.
      - Trinity: Official support for sharding environment observations across multiple remote servers; performance and logging improvements.
      - Ethyr: A Pytorch library for dynamically assembling hierarchical attention networks for processing NMMO IO spaces. We provide a few default attention modules, but users are also free to use their own building blocks -- our library can handle any well defined PyTorch network. We have taken care to separate this PyTorch specific functionality from the core IO libraries in Blade: users should find it straightforward to extend our approach to TensorFlow and other deep learning frameworks.
      - Embyr: Agents now display additional information overhead, such as when they are immune to attacks or when they have been frozen in place.
      - A reasonable 8-population baseline model trained on 12 (old) CPU cores in a day.
      - Improved and expanded official documentation
      - New tutorials covering distributed computation and the IO API
      - The Discord has grown to 80+! Join for active development updates, the quickest support, and community discussions.

|icon| v1.2
###########

.. figure:: /resource/1-2/1-2_env.png

.. dropdown:: Materials

   `Update Slides <https://docs.google.com/presentation/d/1G9fjYS6j8vZMfzCbB90T6ZmdyixTrQJQwZbs8l9HBVo/edit?usp=sharing>`_ Neural MMO v1.2 

   Unity Client and Skilling
      - Blade: Skilling/professions. This persistent progression system comprises Hunting, Fishing (gathering skills) and Constitution, Melee, Range, Mage (combat skills). Skills are improved through usage: agents that spend a lot of time gathering resources will become able to gather and store more resources at a time. Agents that spend a lot of time fighting will be able to inflict and take more damage. Additional bug fixes and enhancements.
      - Trinity: Major new infrastructure API: Ascend -- a generalization of Trinity. Whereas v1.1 Trinity implemented cluster, server, and node layer APIs with persistence, synchronous/asynchronous, etc... Ascend implements a single infrastructure "layer" object with all the same features and more. Trinity is still around and functions identically -- it has just been reimplemented in ~10 lines of Ascend. Additional bug fixes and features; notable: moved environment out of Trinity.
      - Ethyr: Streamlined and simplified IO api. Experience manager classes have been redesigned around v1.2 preferred environment placement, which places the environment server side and only communicates serialized observations and actions -- not full rollouts. Expect further changes in the next update -- IO is the single most technically complex aspect of this project and has the largest impact on performance.
      - Embyr: Focus of this update. Full client rewrite in Unity3D with improved visuals, UI, and controls. The new client makes visualizing policies and tracking down bugs substantially easier. As the environment progresses towards a more complete MMO, development entirely in THREE.js was impractical. This update will also speed up environment development by easing integration into the front end.
      - Baseline model is improved but still weak. This is largely a compute issue. I expect the final model to be relatively efficient to train, but I'm currently low on processing power for running parallel experiments. I'll be regaining cluster access soon.
      - Official documentation has been updated accordingly
      - 20+ people have joined the Discord. I've started posting frequent dev updates and thoughts here.

|icon| v1.1
###########

.. dropdown:: Materials

   `Update Slides <https://docs.google.com/presentation/d/1EXvluWaaReb2_s5L28dOWqyxf6-fvAbtMcBbaMr-Aow/edit?usp=sharing>`_ Neural MMO v1.1 

   Infrastructure and API rework, official documentation and Discord
      - Blade: Merge Native and VecEnv environment API. New API is closer to Gym
      - Trinity: featherweight CPU + GPU infrastructure built on top of Ray and engineered for maximum flexibility. The differences between Rapid style training, tiered MPI gradient aggregation, and even the v1.0 CPU infrastructure are all minor usage details under Trinity.
      - Ethyr: New IO api makes it easy to interact with the complex input and output spaces of the environment. Also includes a killer rollout manager with inbuilt batching and serialization for communication across hardware.
      - Official github.io documentation and API reference
      - Official Discord
      - End to end training source. There is also a pretrained model, but it's just a weak single population foraging baseline around 2.5x of random reward. I'm currently between cluster access -- once I get my hands on some better hardware, I'll retune hyperparameters for the new demo model.

|icon| v1.0
###########

.. |red| image:: /resource/1-0/red.png
.. |blue| image:: /resource/1-0/blue.png
.. |green| image:: /resource/1-0/green.png
.. |fuchsia| image:: /resource/1-0/fuchsia.png
.. |orange| image:: /resource/1-0/orange.png
.. |mint| image:: /resource/1-0/mint.png
.. |purple| image:: /resource/1-0/purple.png
.. |spring| image:: /resource/1-0/spring.png
.. |yellow| image:: /resource/1-0/yellow.png
.. |cyan| image:: /resource/1-0/cyan.png
.. |magenta| image:: /resource/1-0/magenta.png
.. |sky| image:: /resource/1-0/sky.png

|red| |blue| |green| |fuchsia| |orange| |mint| |purple| |spring| |yellow| |cyan| |magenta| |sky|

.. figure:: /resource/1-0/1-0_env.png

.. dropdown:: Materials

   `[OpenAI Blog 2019] <https://openai.com/research/neural-mmo>`_ `[arXiv 2019] <https://arxiv.org/abs/1903.00784>`_ `[Demo] <https://s3-us-west-2.amazonaws.com/openai-assets/neural-mmo/neural_mmo_client_demo.mp4>`_ Neural MMO: A Massively Multiagent Game Environment for Training and Evaluating Intelligent Agents

   `Ideology <https://docs.google.com/document/d/1_76rYTPtPysSh2_cFFz3Mfso-9VL3_tF5ziaIZ8qmS8/edit?usp=sharing>`_ (Two-pager, whiskey material)

   `Style Guide <https://docs.google.com/presentation/d/1m0A65nZCFIQTJm70klQigsX08MRkWcLYea85u83MaZA/edit?usp=sharing>`_ (Website and figure theme)

   This release was developed during a 6-month internship at **OpenAI** spring-summer 2018 with continuing collaboration into the fall. **Phillip Isola* and **Igor Mordatch** advised the project and **Yilun Du** assisted with experiments. Version 1.0 is registered to **OpenAI** and is available under the MIT license. The THREE.js client was developed independently as a collaboration between myself and **Clare Zhu**. It is registered to us jointly and is available under the MIT license.

   Initial public release
      - Blade: Base environment with foraging and combat
      - Embyr: THREE.js web client
      - Trinity: CPU based distributed training infrastructure
      - Ethyr: Contrib library of research utilities
      - Basic project-level documentation
      - End to end training source and a pretrained model

|icon| v0.x
###########

.. figure:: /resource/0-x/0-2_env.png

.. figure:: /resource/0-x/0-1_env.jpg

.. dropdown:: Materials

   `Demo <https://youtu.be/tCo8CPHVtUE>`_ Neural MMO Pre-1.0

   **v0.x:** I started Neural MMO as an independent side project on September 4, 2017. 
      - Personal-scale private side project and early prototyping