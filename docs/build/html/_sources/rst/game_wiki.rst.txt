.. |icon| image:: /resource/icon/icon_pixel.png

.. role:: python(code)
    :language: python

.. figure:: /resource/image/splash.png

|

|icon| Overview
###############

Neural MMO is inspired by classic Massively Multiplayer Online Role-Playing Games. Most of the game systems are adapted from existing games, but they are not copied directly for two reasons. First, the mechanics of actual MMOs are substantially more complex and require dozens to hundreds of hours of investment in order to understand. As Neural MMO is primarily a research platform, we aim to keep it accessible for that purpose. Second, many common game mechanics result in complex and inefficient observation and action spaces. We have made the necessary adaptations to preserve as much environment expressivity as possible without compromising efficiency.

Glossary
********

A quick reference of standard game terms:
 - **Tick:** The simulation interval of the server; a timestep. With rendering enabled, the server targets 0.6s/tick.
 - **NPC:** Non-Player Character; any agent not controlled by a user. Sometimes called a *mob*
 - **Spawn:** Entering into the game, e.g. *players spawn with 10 health*
 - **RPG:** Role-Playing Game, e.g. a game in which the player takes on a particular role, usually one removed from modern reality, such as that of a knight or wizard. *MMO* is short for *MMORPG*, as most MMOs are also role-playing games.
 - **XP (exp):** Experience, a stat associated with progression systems to represent levels.

Features
********

Neural MMO includes the following game systems
 - **Terrain:** Procedurally generated maps with obstacles
 - **Resource:** Agents must forage for resources to survive
 - **Combat:** Agent can fight each other
 - **NPC:** Maps are inhabited by mobs of varying friendliness
 - **Progression:** Agents improve various abilities through usage
 - **Item:** Agents can acquire a number of items with distinct uses
 - **Equipment:** Agents can use armor, weapons, and tools
 - **Profession:** Agents can practice distinct jobs
 - **Exchange:** Agents can trade items on a global market

Each of these sytems may be configured or disabled individually (with some common sense dependencies). This wiki assumes the default configuration with all game systems enabled and does not provide constants (such as the amount of player health) because these are documented separately as part of the environment config.

Contributing
************

If you find errors or ambiguities in the documentation, please either submit a PR with the associated fixes or, if it is easier, simply point it out on the Discord. Numerical constants sometimes change as we balance the game mechanics: always double-check your config file when making important decisions.

|icon| IO 
#########

Encoding
********

By default, Neural MMO flattens the observation of each agent into a fixed-length array and accepts a multidiscrete action obtained by flattening the arguments of all actions. This makes the environment compatible with nearly any reinforcement learning library. The baselines repository includes subnetworks that unflatten, process, and reflatten observations and actions. This makes it possible to treat Neural MMO as a much simpler environment without any loss of expressivity. The information below is therefore mainly to enumerate agent capabilities.

Observation Space
*****************

Each agent observes a groups of entities comprising nearby tiles and agents, its own inventory, and the market. Continuous and discrete tensors of attributes parametrize each entity group. An extra variable *N* counts the number of entities per group.

.. code-block:: python
  :caption: Observation space of a single agent

  observation_space(agent_idx) = {
      'Tile': {
          'Continuous': ...,
          'Discrete': ...,
          'N': ...,
      },
      'Entity': {
          'Continuous': ...,
          'Discrete': ...,
          'N': ...,
      }, 
      'Item': {
          'Continuous': ...,
          'Discrete': ...,
          'N': ...,
      }, 
      'Market': {
          'Continuous': ...,
          'Discrete': ...,
          'N': ...,
      }, 
  }

The exact size of each tensor changes frequently from update to update. You can view the full gym space definition as below:

.. code-block:: python

  import nmmo
  env = nmmo.Env()
  print(env.observation_space(0))
      
Action Space
************

Each agent may take multiple actions per tick -- one from each category. Each action accepts arguments.

.. code-block:: python
  :caption: Action space of a single agent

  action_space(agent_idx) = {
      nmmo.action.Move: {
          nmmo.action.Direction: {
              nmmo.action.North,
              nmmo.action.South,
              nmmo.action.East,
              nmmo.action.West,
          },
      },
      nmmo.action.Attack: {
          nmmo.action.Style: {
              nmmo.action.Melee,
              nmmo.action.Range,
              nmmo.action.Mage,
          },
          nmmo.action.Target: {
              Entity Pointer,
          }
      },
      nmmo.action.Use: {
          nmmo.action.Item: {
              Inventory Pointer,
          },
      },
      nmmo.action.Sell: {
          nmmo.action.Item: {
              Inventory Pointer,
          },
          nmmo.action.Price: {
              Discrete Value,
          },
      },
      nmmo.action.Buy: {
          nmmo.action.Item: {
              Market Pointer,
          },
      },
      nmmo.action.Comm: {
          nmmo.action.Token: {
              Discrete Value,
          },
      },
  }

Pointer actions refer to a selection from the observation space. For example, to purchase an item, an agent should select the corresponding item from the observation space. This works by computing a similarity score against entity embeddings and is already handled by the baseline model.

You can view the formal gym space definition as below:

.. code-block:: python

  import nmmo
  env = nmmo.Env()
  print(env.action_space(0))
 
|icon| Game Systems
###################

Neural MMO uses a tile-based grid engine. This is a much less significant limitation on environment expressivity than some modern reinforcement learning practitioners would suggest: several classic MMOs supporting thousands of players, reasonably realistic economies, and diverse gameplay features also use this structure internally.

Neural MMO includes the following game systems
- **Terrain:** Procedurally generated maps with obstacles
- **Resource:** Agents must forage for resources to survive
- **Combat:** Agent can fight each other
- **NPC:** Maps are inhabited by mobs of varying friendliness
- **Progression:** Agents improve various abilities through usage
- **Items:** Agents can acquire a number of items with distinct uses
- **Equipment:** Agents can use armor, weapons, and tools
- **Profession:** Agents can practice distinct jobs
- **Exchange:** Agents can trade items on a global market


Each game system is individually toggleable and configurable, with a few common sense interdependencies. This wiki primarily addresses the default config with all game systems enabled as the impact of disabling any particular system is fairly obvious. We do, however, point out some important interactions. Also note that all numerical values stated below are configurable, and you should always check the base config for the latest values.

Base
****

The base environment with no game systems enabled provides empty, square maps
 - The terrain is made of grass that agents can walk on freely
 - Agents spawn with 100 health (irrelevant in the absence of other enabled systems)
 - Agents die upon stepping in lava

Terrain
*******

Procedurally generates maps with obstacles and resources.
 - Adds the stone tile type that blocks agent movement
 - Adds a default fractal noise generation algorithm
 - Adds an API for custom terrain generation
   
If the Resouce system is enabled:
 - Adds the foliage, scrub, and water tile types
 - The default generation algorithm will attempt to place foliage farther from water near the center of the map

If the Profession system is enabled:
 - Adds the fish, herb, ore rock, tree, and crystal tile types
 - The default generation algorithm will place individual fish and herbs randomly on water and grass tiles respectively
 - The default generation algorithm will place clusters of ore rock, tree, and crystal on grass tiles

Users can create different terrain by altering generation parameters in the config or by passing a custom generator.
   
The default generation algorithm is more sophisticated than typical Perlin noise -- it actually stretches the space of one Perlin fractal using a second Perlin fractal. It further attempts to scale spacial frequency to be higher at the edges of the map and lower at the center. This effect is not noticable in small maps but creates large deviations in local terrain structure in larger maps.

Resource
********

Agents must forage for food and water in order to survive. Foliage tiles containing food and water tiles containing ... well, water ... are added to the map. A foliage tile is consumed when an agent steps on it. Agents cannot step on water tiles but can drink by being adjacent. This does not deplete the tile.
 - Agents spawn with 100 food and 100 water
 - Food and water are depleted by 5 per tick
 - Agents above 50% food and water will slowly restore health 
 - Agents with 0 food take 5 damage per tick
 - Agents with 0 water take 5 damage per tick
 - These damage values stack

Consumed foliage tiles regenerate with a small probability each subsequent tick. This temporary unavailibility places a carrying capacity on local regions.

Combat
******

Agents gain access to melee, range, and mage attacks. These obey a rock-paper-scissors dominance relationship: melee beats range beats mage beats melee. Dominance is calculated using the attacker's chosen attack skill and the defender's main combat skill. Attacks inflict damage to the target according to the following formula: *damage = effectiveness multiplier * (attack score - defense score).

**Combat defaults are currently only correctly configured for all systems enabled. The base system information below will be accurate once this is fixed.**

In the base Combat system:
 - Attacks can inflict damage from 3 squares away
 - Attack score is equal to a flat base damage of 30
 - Defense score is equal to zero
 - Main combat skill is the one an agent has used the most
 - Effective damage multiplier is 1.5 for using the correct style (e.g. mage vs melee) and 1 otherwise

If the progression system is enabled
 - Base damage is decreased to 0
 - Attack score is increased by 5 for each level of the attacker's offensive skill
 - Defense is increased by 5 for each level of the defender's highest skill
 - Main combat skill is the one with the most experience

If the equipment system is enabled
 - Attack score is increased by the attacker's offensive equipment bonus (weapons, ammunition)
 - Defense score is increased by the defender's defensive bonus (armor, tools)
 - Attack score for a specific style is increased by 15 if wielding a weapon
 - Attack score is increased by 15 per weapon or ammunition level
 - Defense score is increased by 30 if wielding a tool
 - Defense score is increased by 10 per armor level

With all systems enabled:

.. code-block:: python

  offense = base damage + attacker level adjustment + attacker equipment adjustment
  defense = target level adjustment + target equipment adjustment
  raw_damage = effectiveness multiplier * offense * (15 / (15 + defense))
  final_damage = max(0, int(damage))

The attacker always has an advantage in that they can select the skill strong against the target's main skill. However, the defender can immediately retaliate in the same manner. Additionally, a combat style in which an agent has a higher level and better equipment may outperform one with only the effectiveness multiplier.

NPC
***

Adds NPCs (non-playable characters) to the environment

**Requires:** Combat system

In the base NPC system:
 - NPCs are controlled by one of three scripted AIs
 - Passive NPCs wander randomly and cannot attack
 - Neutral NPCs wander randomly but will attack aggressors and give chase using a Dijkstra's algorithm based pathing routine
 - Hostile NPCs will actively hunt down and attack other NPCs and players using the same pathing algorithm

If the Equipment system is enabled:
 - NPCs spawn with random armor piece

If the Profession system is enabled:
 - NPCs spawn with a random tool

If the Progression system is enabled:
 - NPCs will appear in varying levels
 - Any equipment dropped will be of level equal to the NPC's level

If the Exchange system is enabled:
 - NPCs spawn with gold equal to their level

Generally, Passive NPCs will spawn towards the edges of the map, Hostile NPCs spawn in the middle, and Neutral NPCs spawn somewhere between. The exact number and power distribution of NPCs varies by environment config.

Progression
***********

Adds a leveling system that enables agents to become better at things by doing them.

**Requires:** Combat or Profession system

In the base Progression system:
 - Levels range from 1 to 10
 - Agents spawn with all skills at level 1 (0 XP)
 - Level *x+1* requires 10*2^*x* XP

If the Combat system is enabled:
 - Agents are awarded 1 XP per attack

If the Item system is enabled:
 - All items except gold will appear in varying levels

If the Profession system is enabled
 - Agents are awarded 1 XP per ammunition resource gathered
 - Agents are awarded 5 XP per consumable resource gathered

Item
****

Agents gain an inventory that can hold 12 items. Which items are available is dependent upon which other systems are enabled.

**Requires:** Equipment or Profession system

If the Equipment system is enabled:
 - Adds armor and weapons

If the Profession system is enabled:
 - Adds consumables, tools, and ammunition

If the Exchange system is enabled:
 - Adds Gold

Equipment
*********

Agents gain access to an additional 5 inventory slots for equipped items: a hat, top, bottom, held item, and a stack of ammunition.

**Requires:** Combat and Item system

If the Progression system is enabled:
 - All items appear in level 1-10 variants. 
 - Agents can equip armor up to the level of their highest skill
 - Agents can equip weapons up to the level of the associated skill

If the Profession system is enabled:
 - Agents can equip ammunition and tools up to the level of the associated skill

Profession
**********

The Profession system adds 5 new gathering skills that provide supplies for exploration and combat. Unlike in the Resource system, materials gathered from the Profession system are added to the agent's inventory as items.

**Requires:** Item system

In the base progression system:
 - Prospecting, Carving, Alchemy: gather resources used as ammunition to enhance melee, range, and mage attacks
 - Fishing, Herbalism: gather resources that can be consumed to restore food, water, and health
 - There is a 2.5 percent chance to obtain a weapon while gathering ammunition
 - These drops are intentionally not for the same style as the gathered ammunition
 - Ore (Prospecting) can drop Wands
 - Trees (Carving) can drop Swords
 - Crystals (Alchemy) can drop Bows

Exchange
********

Agents gain access to an environment-wide market where they can buy items from and sell items to each other using gold.

**Requires:** Item and Equipment or Profession systems

In the base Exchange system:
 - Agents place sell offers on the market for one of their items at a particular price
 - The item is immediately removed from the seller's inventory
 - Other agents can immediately buy that item and receive it
 - If multiple agents attempt to buy the same item at the same time, the market will attempt to fulfill the request from another seller at a price no more than 10% higher.
 - Buy and sell actions are prioritized per-population based on each agent's entity ID. So if the first agent on a team sells an item, the second agent will have the first chance to buy it. Note that there are some edge cases here, and we would appreciate user feedback.

Agents only observe the current best offer for each item of each level. This prevents unbounded blowup of the observation and action spaces.

|icon| Skills
#############

Melee
*****

Weapon: Sword
Ammunition: Scrap
Strong against: Range
Weak against: Mage

Range
*****

Weapon: Bow
Ammunition: Shaving
Strong against: Mage
Weak against: Melee

Mage
****

Weapon: Wand
Ammunition: Shard
Strong against: Melee
Weak against: Range

Fishing
*******

Tool: Rod
Resource: Ration
Usage: Restores food and water

Herbalism
*********

Tool: Gloves
Resource: Poultice
Usage: Restores health

Prospecting
***********

Tool: Pickaxe
Resource: Scrap
Usage: Melee ammunition

Carving
*******

Tool: Chisel
Resource: Shaving
Usage: Range ammunition

Alchemy
*******

Tool: Arcane focus
Resource: Shard
Usage: Mage ammunition

|icon| Items 
############

Gold
****

Currency used on the market. Inherently valuable as the only medium of exchange.

Armor: Hat, Top, Bottom
***********************

Grants 10 defense per item level

Requires at least one skill greater than or equal to the item level to equip

Also referred to as helmet, chestplate, and platelegs

Weapon: Sword, Bow, Wand
************************

Grants a flat 15  plus 15 attack bonus per item level to the associated style (melee, range, mage)

Requires a pertinent skill level greater than or equal to the item level to equip

Tool: Rod, Gloves, Pickaxe, Chisel, Arcane Focus
************************************************

Grants a flat 30 defense regardless of item level

Requires a pertinent skill level (fishing, herbalism, prospecting, carving, alchemy) greater than or equal to the item level to equip

Enables an agent to collect a pertinent resource (ration, poultice, scrap, shaving, shard) at a level equal to the item level

Ration
******

Consume to restore 5 food and water per item level.

Requires at least one skill greater than or equal to the item level to use

Poultice
********

Consume to restore 5 health per item level.

Requires at least one skill greater than or equal to the item level to use
