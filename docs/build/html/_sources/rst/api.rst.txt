.. |icon| image:: /resource/icon/icon_pixel.png

.. figure:: /resource/image/splash.png

|icon| User API
###############

Neural MMO provides a pettingzoo compliant environment API, a agent base class, and a deep configuration system

Environment
-----------

.. autoclass:: nmmo.Env
   :members:
   :noindex:

.. autoclass:: nmmo.Agent
   :members: __init__, __call__
   :noindex:

Config
------

.. automodule:: nmmo.config
   :members: Config, Small, Medium, Large, Resource, Combat, Progression, NPC, SequentialLoader, TeamLoader
   :undoc-members:
   :noindex:

Ratings
-------

.. autoclass:: nmmo.OpenSkillRating
   :members:
   :noindex:

Scripting
---------

To support scripted models, we provide a small wrapper class for extracting meaningful attributes from observation tensors. We also expose static definitions of the environment's materials and observation/action spaces. The core environment ships with a random example agent; more are available in the accompanying baselines repository.

.. automodule:: nmmo.scripting
   :members:
   :noindex:

.. autoclass:: nmmo.Serialized
   :members:
   :undoc-members:
   :noindex:

.. automodule:: nmmo.action
   :members:
   :undoc-members:
   :noindex:

.. automodule:: nmmo.material
   :members: Lava, Water, Grass, Scrub, Forest, Stone, Orerock, All, Impassible, Habitable
   :noindex:

.. automodule:: nmmo.agent
   :members: Random
   :noindex:

Procedural Generation
---------------------

The default map generator is multioctave perlin noise that is itself seeded using perlin noise to create terrain of varying local frequency. Use the MAP_GENERATOR config argument to supply your own generator classes. We suggest subclassing the default and overriding the generate_map method. For procedural generation beyond maps, customize game system mechanics dynamically to modify mechanics per-environment.

.. automodule:: nmmo.terrain
   :members:
   :noindex:


Overlays
--------

For visualization, the Overlay API enables users to write custom 2D overlays to be rendered in the Unity3D client


.. autoclass:: nmmo.Overlay
   :members:
   :noindex:

.. autoclass:: nmmo.OverlayRegistry
   :members:
   :noindex:

|icon| Developer API
####################

The doctree below contains automatically generated documentation for the entire project. This is not intended for typical users but is a useful reference for Neural MMO developers and contributors.

.. toctree::
   :maxdepth: 4

   ../autodoc/nmmo
