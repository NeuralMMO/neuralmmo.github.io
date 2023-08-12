.. |icon| image:: /resource/icon.png

|

.. card::
    :img-background: /../_static/banner.jpg

Feedback on our docs? Contribute changes and suggestions on `Discord <https://github.com/neuralmmo>`_.

.. dropdown:: NMMO Gameplay Narrative

    This Wiki is meant as a quick reference. To understand the game at a high-level, consider this narrative example:

    Our team of 8 agents spawns on the edge of a large square map. At this time, we are assigned a task to complete (see Tasks), with potential hostile teams just out of view to the left and right.
    
    Immediate strategic choices arise: rushing into the map center, attempting a quick elimination of nearby teams, or dispatching scouts to gauge the behavior of the nearby teams. This opening flurry of decision making, which encompasses the first 15-30 seconds of a 10-minute game, culminates in a strategic situation that sets the tone for the rest of the game.

    The subsequent gameplay phases in Neural MMO 2.0 now depend not only on the surviving agents, nearby resources and terrain, but also on our assigned task. Simple tasks, such as cutting down a tree, can be completed consistently regardless of initial conditions. For harder tasks, such as acquiring high-level equipment, we will have to play more passively if a required resource is far away or if we have lost several agents in the opening stage. But assuming good conditions, we can use the next few minutes to gain an advantage versus the competition. Agents can enhance their capabilities through practice in any of 8 different professions, each conferring unique offensive or defensive benefits. Task completion often requires specific skill levels, prompting agents to specialize and cooperate. For example:
      - If our task is to obtain level 5 arrows, it would make sense to have one agent practice carving to produce them while another capitalizes on the surplus of ammunition by training ranged combat.
      - We might assign another agent to practice herbalism and provide healing potions for the team. Provided we can keep this agent safe, it would also be a good candidate to hold the team's gold and attempt to buy items on the exchange.
      - This would allow us to invest heavily in equipping our range agent to fight powerful NPCs, which have a chance to drop the level 5 axe our carver will need to produce level 5 arrows.
      
    These are but a few possibilities, and ultimately, decisions are a matter of strategy and opportunism.

The Game Map
************

Each instance of Neural MMO contains an automatically generated tile-based game map of 128 x 128 tiles. Agents can not walk off the edges into the map.

Tiles are broadly categorized as follows:
  - *Passable* tiles can be walked on while *obstacle* tiles block movement
  - *Resource* tiles can be harvested while *non-resource* cannot

+-------------------+-----------------------------------+-------------+
| **Tile Type**     | *Passable*                        | *Obstacle*  |
+===================+===================================+=============+
| **Resource**      | Foliage, Ore, Tree, Crystal, Herb | Water, Fish |
+-------------------+---------------------+-------------+-------------+
| **Non-resource**  | Grass, Harvested Tile             | Stone       |
+-------------------+-----------------------------------+-------------+

*Resource* tiles may be harvested. *Passable* tiles are harvested by walking over them and *obstacle* tiles by walking next to them. The resource is then consumed from the tile. It will regenerate randomly over time on the same tile. The only exception is the Water tile, which provides unlimited resource.

Each Agent has a visibility of up to seven tiles in Chebyshev (L-inf) distance. In other words, an Agent can see a 15x15 square around itself.

.. dropdown:: About the tile generation algorithm
    
    The default tile generation algorithm is more sophisticated than typical Perlin noise -- it stretches the space of one Perlin fractal using a second Perlin fractal. It further attempts to scale spacial frequency to be higher at the edges of the map and lower at the center. This effect is not noticable in small maps but creates large deviations in local terrain structure in larger maps.
    
|icon| Survival
###############

Agents have health, food, and water. These are displayed overhead as green, gold, and blue bars respectively. Agents must stay full, hydrated, and healthy in order to survive. 

Losing and gaining resources:
  - Health, food, and water start at 100
  - Agents lose 5 food and 5 water per game tick
  - Agents lose 10 health per tick if out of food
  - Agents lose 10 health per tick if out of water
  - These values add - lose 20 health if out of food and water per tick
  - If above half food and half water, agents regain 10 health per tick

**Tick:** The gameplay consists of time units called “ticks.” When rendering, the game moves at 0.6s/tick.

Agents can replenish food and water. Walking on a foliage tile restores food to 100. The foliage tile then is harvested and will respawn at a random time in the same place. Walking adjacent to a water tile restores water to 100. Water tiles do not empty.

|icon| Competition Environment and Levels
*****************************************

At the start of a game, all agents on all teams spawn (enter the game) together around the perimeter of the map on the same tile. Agent teams are evenly dispersed around the perimeter. 

Non-Player Characters (NPCs) are any agent not controlled by a user; sometimes called a *mob*. NPCs are scattered across the entire map. They get stronger and more aggressive towards the center. NPCs are all individuals; they fight each other as well; and they are all controlled by basic scripts. Their aggression and strength levels are correlated, but otherwise are identical. 

Agents can occupy the same tile as other agents. There is no limit to number or type of agents on a single tile, including enemy agents and NPCs. 

**Time and Gameplay**
Each tick provides the opportunity for every Agent and NPC to do any, all or none of the following actions:

**Move 1 tile in any available direction**

- Agents cannot move off of the game map or into obstacle tiles like water and stone.
- As the game progresses, the action space becomes constrained as a fog encircles the board. Agents take increasing damage in tiles covered in fog, and all gradually move towards the center of the game space.

**Attack an Agent - either NPC or from another team**

- Attack can only be against one other Agent or NPC
- To attack, your Agent must be within three tiles of the opponent -- **within a 7x7 square around your Agent.**
 
**Inventory Management**

Inventory capacity is 12 items, including armor, weapon, tools, and consumables. Each item except ammunitions takes one inventory space. Ammunitions of the same type and level can be stacked infinitely in one inventory space. If an Agent's inventory is full, it cannot harvest or loot new items. To manage inventory, an Agent can:

- List an item in the Market, which remains on the inventory until sold
- Destroy an item to instantly make a space available
- Give an item to a team mate, which is **only permitted when standing on the same tile**

.. dropdown:: About the Observation Space

    Each agent's observation contains the current game tick, the agent's id, data from the nearby 15x15 visible tiles, data from up to 100 entities within its vision, data from its own inventory, and data from the global market listings.

.. code-block:: python
  :caption: Observation space of a single agent

  observation_space(agent_id) = {
        'ActionTargets': ...  # Action masks for the action space items
        'AgentId': Discrete(129),
        'CurrentTick': Discrete(1025),
        'Entity': Box(-32768, 32767, (100, 23), int16),
        'Inventory': Box(-32768, 32767, (12, 16), int16),
        'Market': Box(-32768, 32767, (1024, 16), int16),
        'Task': Box(-32770.0, 32770.0, (4096,), float16),  # Task embedding dimension
        'Tile': Box(-32768, 32767, (225, 3), int16)
    }

Levels
######
.. tab-set::

    .. tab-item:: Agent Levels

         - Levels range from 1 to 10
         - Agents spawn with all skills at level 1 and 0 XP
         - Level x+1 requires 10*2^(x-1)* XP. For example, to get to level 2, one needs 10 XP.
         - Agents are awarded 1 XP per attack
         - Agents are awarded 1 XP per ammunition resource gathered
         - Agents are awarded 5 XP per consumable resource gathered
 
    .. tab-item:: Items and Equipment Levels

         - All items appear in level 1-10 variants. 
         - Agents can equip armor up to the level of their highest skill
         - Agents can equip weapons up to the level of the associated skill
         - Agents can equip ammunition and tools up to the level of the associated skill

.. dropdown:: About the Action Space

   Each agent may take multiple actions per tick -- one from each category. Each action accepts a list of arguments. Each argument is a discrete variable. This can be either a standard index (i.e. 0-4 for direction) or a pointer to an entity (i.e. inventory item or agent).

.. code-block:: python
  :caption: Action space of a single agent

  action_space(agent_idx) = {
      nmmo.action.Move: {
          nmmo.action.Direction: {
              nmmo.action.North,
              nmmo.action.South,
              nmmo.action.East,
              nmmo.action.West,
              nmmo.action.Stay,
          },
      },
      nmmo.action.Attack: {
          nmmo.action.Style: {
              nmmo.action.Melee,
              nmmo.action.Range,
              nmmo.action.Mage,
          },
          nmmo.action.Target: {
              Discrete(101),  # config.PLAYER_N_OBS + 1 (no-action flag)
          }
      },
      nmmo.action.Use: {
          nmmo.action.InventoryItem: {
              Discrete(13),  # config.INVENTORY_N_OBS + 1 (no-action flag)
          },
      },
      nmmo.action.Destroy: {
          nmmo.action.InventoryItem: {
              Discrete(13),  # config.INVENTORY_N_OBS + 1 (no-action flag)
          },
      },
      nmmo.action.Give: {
          nmmo.action.InventoryItem: {
              Discrete(13),  # config.INVENTORY_N_OBS + 1 (no-action flag)
          },
          nmmo.action.Target: {
              Discrete(101),  # config.PLAYER_N_OBS + 1 (no-action flag)
          }
      },
      nmmo.action.GiveGold: {
          nmmo.action.Price: {
              Discrete(99),  # config.PRICE_N_OBS
          },
          nmmo.action.Target: {
              Discrete(101),  # config.PLAYER_N_OBS + 1 (no-action flag)
          }
      },
      nmmo.action.Sell: {
          nmmo.action.InventoryItem: {
              Discrete(13),  # config.INVENTORY_N_OBS + 1 (no-action flag)
          },
          nmmo.action.Price: {
              Discrete(99),  # config.PRICE_N_OBS
          },
      },
      nmmo.action.Buy: {
          nmmo.action.MarketItem: {
              Discrete(1025),  # config.MARKET_N_OBS + 1 (no-action flag)
          },
      },
      nmmo.action.Comm: {
          nmmo.action.Token: {
              Discrete(50),  # config.COMMUNICATION_NUM_TOKENS
          },
      },
  }

About Combat
************

Each agent can attack one opponent per game tick. In a given tick, multiple enemy agents can attack a single agent. Agents select from Melee, Range, and Mage style attacks. An agent's main combat skill is the one that they use the most / have the highest XP in. This is denoted by the hat they are wearing in the client.

Attack skills obey a rock-paper-scissors dominance relationship: 
 - Melee beats Range 
 - Range beats Mage 
 - Mage beats Melee

Attack range is 3 tiles for all styles. This is a 7 by 7 square centered on the attacker.

.. tab-set::

    .. tab-item:: Choosing attack style
    
        The attacker can select the combat skill strongest against the target's main skill. This increases attack damage by 50%. However, the defender can immediately retaliate in the same way. A strong agent with a higher level and better equipment can still beat a weaker agent, even if the weaker agent uses the attack style that multiplies damage. 

    .. tab-item:: Armor
    
        There are three pieces of armor: Hat, Top, Bottom. Armor requires at least one skill ≥ the item level to equip. Armor provides defense that increases with equipment level.

    .. tab-item:: Weapons and Tools
    
        Weapons require an associated fighting style skill level ≥ the item level to equip. Weapons boost attacks; higher level weapons provide more boost. Tools grant a flat defense regardless of item level.

**Damage** to health is determined based on several factors, including:
 - Fighting style
 - Combat skill level
 - Weapon level
 - Armor levels

.. code-block:: python

   def COMBAT_DAMAGE_FORMULA(self, offense, defense, multiplier):
      '''Damage formula'''
      return int(multiplier * (offense * (15 / (15 + defense))))


.. dropdown:: Example combat interaction

    Start:

    *Agent You:* 100 HP, poor armor and weapons

    *Agent Them:* 75 HP, good armor and weapons

    |

    Tick 1:

    You attack them. They lose 18 HP

    They attack you. You lose 27 HP

    |

    Tick 2:

    You attack them. They lose 18 HP

    They attack you. You lose 27 HP

    |

    Tick 3: 

    You attack them. They lose 18 HP

    They run

    |

    Tick 4: You chase and attack them. They lose 18 HP.

    They consume a potion to regain 50 HP and run some more.

    |

    This continues for some time, with your opponent running away, and you chasing them. 
    Eventually, you give up and let them go. Your HP is low, and they had to consume a potion. 

    Fortunately, this was only a training run, and you can now reconsider your strategy for the next round.

Professions, Tools, and Items
*****************************

There are 8 Professions that Agents can learn and level up in. Agents can improve their skills in multiple Professions, but will not be able to progress in all Professions. How Professions are distributed across Agent teams is a part of game strategy. 

For Skills Prospecting, Carving, and Alchemy, agents walk on the associated resource tile to harvest the resource. Agent receives a different quality/level of resource, depending **only** on agent levels/tools. The resource tile will respawn later in the same place. There is a 2.5 percent chance to obtain a weapon while gathering ammunition on a tile, the level of which is also determined by the tool level of the harvesting agent.

|

**Agents have an inventory that can hold 12 items.**

+----------------+-------------+---------+-----------------+------------+------------------+---------------------+
| **Item Type**  |*Profession* |*Tool*   |*Level up method*|*HP Effect* |*Food/Water Level*|*Market Buy/Sell*    |
+================+=============+=========+=================+============+==================+=====================+
|                | Mage        | Wand    | Hitting and     | \-HP level |                  | Wand                |
|                +-------------+---------+ damaging        | unless you |                  +---------------------+
|**Combat**      | Melee       | Spear   | NPCs and        | take no    |                  | Spear               |
|                +-------------+---------+ Enemies         | damage     |                  +---------------------+
|                | Range       | Bow     |                 |            |                  | Bow                 |
+----------------+-------------+---------+-----------------+------------+------------------+---------------------+
|                | Fishing     | Rod     | Level up        |            | \+Food & Water   | Ration              |
|**Gathering**   +-------------+---------+ via harvest     +------------+------------------+---------------------+
|                | Herbalism   | Gloves  | experience      | \+HP level |                  | Potion              |
+                +-------------+---------+                 +------------+                  +---------------------+
|                | Carving     | Axe     |                 |            |                  | Axe & Arrow         |
|                +-------------+---------+                 +            +                  +---------------------+
|                | Prospecting | Pickaxe |                 |            |                  | Pickaxe & Whetstone |
|                +-------------+---------+                 +            +                  +---------------------+
|                | Alchemy     | Chisel  |                 |            |                  | Chisel & Runes      |
+----------------+-------------+---------+-----------------+------------+------------------+---------------------+

|

**Tools**
  - All Tools provide a flat 30 defense regardless of item level
  - Tools need a relevant skill level (fishing, herbalism, prospecting, carving, alchemy) ≥ the item level to equip
  - Tools enable an agent to collect an associated resource (ration, potion, whetstone, arrow, runes) at a level equal to the tool level

**Rations**
  - Consume a ration to restore food and water level, which increase by 50 + 5*item level 
  - Requires at least one skill greater than or equal to the item level to use

    A rod helps harvesting higher-level rations. Alternatively, agents can buy rations in the market.
    
    For example, if agents buy a level 3 ration in the market, they can use it only when they have any skill level 3 or above. If they buy a ration with a level higher than any of their skills, they can store but cannot use it until a skill level = the ration level. 

**Potions**
  - Consume a potion to restore health level, which increases by 50 + 5*item level
  - Requires at least one skill greater than or equal to the glove level to use.
  
    A pair of gloves helps harvesting higher-level potions. Alternatively, agents can buy potions in the market.
  
    The same rules about skill and item levels apply to both potions and rations. 


|icon| Market
*************

Gold coins are the currency for buying and selling items in NMMO. Gold coins cannot be sub-divided. Agents set their own prices when selling items and receive gold when someone is willing to accept their price. Agents can gift to one another if they are standing on the same tile. 

Market interactions are as follows, which are similar to that of Craiglist:
 - Agents list one of their items at a desired price on the market via Sell action
 - When the sell action is processed, other agents can see the listings from the next tick
 - The item remains in the seller's inventory until sold or for 5 ticks, if not sold
 - Other agents can offer to buy the item via Buy action at the seller's price
 - If multiple agents attempt to buy the same item, the market will randomly select a single buyer

Agents have access to all the listings.

+--------------------------------------------------------------------------------------+
| **BUY and SELL with GOLD**                                                           |
+======================================================================================+
| **COMBAT items**                                                                     |
+--------------------+------------------------+--------------------+-------------------+
| *Tools*            | *Ammunitions*          | *Weapons*          | *Armors*          |
+--------------------+------------------------+--------------------+-------------------+
| AXE                | Wood ARROWS            | BOW                | HAT, TOP, BOTTOM  |
+--------------------+------------------------+--------------------+                   |
| PICKAXE            | Rock WHETSTONES        | SPEAR              |                   |
+--------------------+------------------------+--------------------+                   +
| CHISEL             | Magic RUNES            | WAND               |                   |
+--------------------+------------------------+--------------------+-------------------+
| **Health items**                                                                     |
+--------------------+-----------------------------------------------------------------+
| *Tools*            | *Consumables*                                                   |
+--------------------+-----------------------------------------------------------------+
| ROD                | HARVEST fish to produce RATION items (restore water and food)   |
+--------------------+-----------------------------------------------------------------+
| GLOVES             | HARVEST herbs to produce POTION items (restore health)          |
+--------------------+-----------------------------------------------------------------+

|icon| NPCs
************

**Characteristics**
 - NPCs are controlled by one of three scripted AIs
 - Passive NPCs wander randomly and cannot attack
 - Neutral NPCs wander randomly but will attack aggressors and give chase using a Dijkstra's algorithm based pathing routine
 - Hostile NPCs will actively hunt down and attack other NPCs and players using the same pathing algorithm
 - NPCs will appear in varying levels

**NPC Items**
 - NPCs spawn with random armor piece
 - NPCs spawn with a random tool
 - Any equipment dropped will be of level equal to the NPC's level
 - NPCs spawn with gold equal to their level

Generally, Passive NPCs will spawn towards the edges of the map, Hostile NPCs spawn in the middle, and Neutral NPCs spawn somewhere between.

|icon| Tasks
************

**About Tasks**
  - Goal is to accomplish specific tasks from the curriculum for points.
  - Tasks are randomly generated and assigned at the beginning of each round.
  - If a Team accomplishes a Task, they receive 1 point for the round. 
  - Each team receives different tasks from one another each round.
  - Difficulty of the tasks evens out, as all teams compete with each other 1024 rounds to determine the best teams overall in that group.
  - Based on the average scores, teams are placed in the next round of 1024 with other teams whose performance matches their own.

.. dropdown:: Sample tasks

    Inflict(damage_type, quantity) - 
      - Damage_type = 3 combat styles 
      - Quantity = 1-100 HP out of total 100 HP
      - Ex. Inflict 5 damage with melee

    |

    Defeat(npc/player, level)
      - npc/player = NPC or Player, Unit = 1
      - Level = 1-10
      - Defeat a level 5 npc

    |

    Achieve(skill, level)
      - Skill = 8 skills (Professions)
      - Level = 10
      - Ex: Achieve level 5 prospecting

    |

    Harvest(resource, level)
      - Resource = 5 resources
      - Level = 10 levels
      - Ex: collect a level 3 shard

    |

    Equip(type, level)
      - Type = Hat, Top, Bottom
      - Level = 10
      - Ex: equip a level 5 hat

    |

    Hoard(gold) - Accumulate a total of 20 gold as a team
      - Gold: Units of transaction ingots

    |

    AllMembersWithinRange(num_tiles) - All team members stay within the 5 x 5 tiles
      - Num_tiles: Variable starting with tile you’re on as 0

    |

    Defend(teammate) - Don’t let your 3rd teammate die
      - Teammate: Specific member of your team can’t die

    |

    Eliminate(team, direction) - Eliminate the team that spawns to your right
      - Direction: Left; Right

|icon| Tiles Quick Reference
******************************

+-----------+--------------+------------------------------------------+---------------+------------------------------------+
| **Tile**  | **Passible** | **Resource**                             | **Skill**     | **Note**                           |
+===========+==============+==========================================+===============+====================================+
| WATER     | No           | Maximize Agent's water level             |               | Stand next to WATER to drink       |
+-----------+--------------+------------------------------------------+---------------+------------------------------------+
| FISH      | No           | Yield RATION. Stand next to harvest.     | Fishing       | Equip ROD for high-level RATION    |
+-----------+--------------+------------------------------------------+---------------+------------------------------------+
| FOILAGE   | Yes          | Maximize Agent's food level              |               |                                    |
+-----------+--------------+------------------------------------------+---------------+------------------------------------+
| HERB      | Yes          | Yield POTION                             | Herbalism     | Equip GLOVES for high-level POTION |
+-----------+--------------+------------------------------------------+---------------+------------------------------------+
| TREE      | Yes          | Yield ARROW (Range ammunition)           | Carving       | Equip AXE for high-level           |
|           |              +------------------------------------------+               | ARROW and SPEAR                    |
|           |              | Seldom (2.5%) yield SPEAR (Melee weapon) |               |                                    |
+-----------+--------------+------------------------------------------+---------------+------------------------------------+
| ORE       | Yes          | Yield WHETSTONE (Melee ammunition)       | Prospecting   | Equip PICKAXE for high-level       |
|           |              +------------------------------------------+               | WHETSTONE and WAND                 |
|           |              | Seldom yield WAND (Mage weapon)          |               |                                    |
+-----------+--------------+------------------------------------------+---------------+------------------------------------+
| CRYSTAL   | Yes          | Yield RUNES (Mage ammunition)            | Alchemy       | Equip CHISEL for high-level        |
|           |              +------------------------------------------+               | RUNES and BOW                      |
|           |              | Seldom yield BOW (Range weapon)          |               |                                    |
+-----------+--------------+------------------------------------------+---------------+------------------------------------+
| STONE     | No           |                                          |               |                                    |
+-----------+--------------+------------------------------------------+---------------+------------------------------------+

