.. |icon| image:: /resource/icon/icon_pixel.png

.. figure:: /resource/image/splash.png

|

Neural MMO provides a pettingzoo compliant environment API, an extensive configuration system, and support for agent scripting, OpenSkill evaluation, custom terrain generation, and overlay visualization. This section is intended as a reference -- the tutorials provide a much better starting point for most users.

|icon| Environment
##################

.. autoclass:: nmmo.Env
   :members:
   :noindex:

.. autoclass:: nmmo.Agent
   :members: __init__, __call__
   :noindex:

|icon| Config
#############

.. automodule:: nmmo.config
   :members: Config, Small, Medium, Large, Resource, Combat, Progression, NPC, SequentialLoader, TeamLoader
   :undoc-members:
   :noindex:

|icon| Ratings
##############

.. autoclass:: nmmo.OpenSkillRating
   :members:
   :noindex:

|icon| Scripting
################

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

|icon| Procedural Generation
############################

The default map generator is multioctave perlin noise that is itself seeded using perlin noise to create terrain of varying local frequency. Use the MAP_GENERATOR config argument to supply your own generator classes. We suggest subclassing the default and overriding the generate_map method. For procedural generation beyond maps, customize game system mechanics dynamically to modify mechanics per-environment.

.. autoclass:: nmmo.MapGenerator
   :members:
   :noindex:

.. autoclass:: nmmo.Terrain
   :members:
   :noindex:

|icon| Overlays
###############

For visualization, the Overlay API enables users to write custom 2D overlays to be rendered in the Unity3D client


.. autoclass:: nmmo.Overlay
   :members:
   :noindex:

.. autoclass:: nmmo.OverlayRegistry
   :members:
   :noindex:

|icon| Reference
################

The doctree below contains automatically generated documentation for the entire project. Most users will only need the more thoroughly documented user API above.

.. toctree::
   :maxdepth: 4

   ../autodoc/nmmo
