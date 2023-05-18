.. |icon| image:: /resource/icon.png

|

.. card::
   :img-background: /../_static/banner.png

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

|icon| Procedural Generation
############################

The default map generator is multioctave perlin noise that is itself seeded using perlin noise to create terrain of varying local frequency. Use the MAP_GENERATOR config argument to supply your own generator classes. We suggest subclassing the default and overriding the generate_map method. For procedural generation beyond maps, customize game system mechanics dynamically to modify mechanics per-environment.

.. autoclass:: nmmo.MapGenerator
   :members:
   :noindex:

.. autoclass:: nmmo.Terrain
   :members:
   :noindex: