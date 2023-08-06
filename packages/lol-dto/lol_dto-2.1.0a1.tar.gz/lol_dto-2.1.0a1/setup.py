# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lol_dto',
 'lol_dto.classes',
 'lol_dto.classes.game',
 'lol_dto.classes.sources',
 'lol_dto.names_helper',
 'lol_dto.utilities']

package_data = \
{'': ['*']}

extras_require = \
{'names': ['lol-id-tools>=2.0.0,<3.0.0']}

setup_kwargs = {
    'name': 'lol-dto',
    'version': '2.1.0a1',
    'description': 'A unified representation of League of Legends-related information',
    'long_description': '# LoL Game DTO\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA unified Data Transfer Object for League of Legends games. Currently developed by Tolki.\n\n## 2.0 note and JSON serialization\n\nVersion 2.0 moved the implementation from `TypedDict` to `dataclass`, which means the syntax changed and is not\nbackwards compatible.\n\n`dataclasses.asdict()` can be used to get the object as a dictionary, and then saved as a JSON.\n\nFields can be omitted when not supplied to make the object lighter. This is particularly useful for Snapshots objects.\n\n## Motivation\n\nLeague of Legends game information can come in many forms. The most popular source is Riot’s API and in particular its\n[MATCH-V5](https://developer.riotgames.com/apis#match-v5/) endpoint, which defines its own MatchDto\nand MatchTimelineDto objects. While other sources of information could follow Riot’s data format, requiring\nmultiple objects to represent a single game and being constrained by Riot’s data format is inconvenient.\n\nThis is why creating a unique, community-driven representation of League of Legends game data will help communication\nand teamwork in open source projects. Improving the data structure will also make the data more accessible to new\ndevelopers, and will make existing libraries easier to maintain.\n\n### Constraints\n\n- Retain all the information present in the Riot API\n\n- Allow for external information, like role, to be added to the object\n\n- Be compatible across a wide variety of programming languages\n\n### General philosophy\n\n- We try to adhere to the [Google JSON Style Guide](https://google.github.io/styleguide/jsoncstyleguide.xml?showone=Property_Name_Format#Property_Name_Format)\n- Information is as close as possible to the objects it refers to\n  - Player-specific information is directly under `player` objects\n  - Team-wide information is directly under `team` objects\n- Information is not duplicated\n  - `winner` is only defined once in the `game` object\n- Field names are coherent and comply with modern LoL nomenclature\n  - Every field that is an identifier ends with `id`\n  - Fields like `cs` or `monstersKilled` use current game vocabulary (as of June 2020)\n  - All durations from the game start are expressed in seconds\n\n#### `null`\n\nThe `null` value should only be used for unknown information. The best practice is to not have unknown fields in\nthe object to keep it as light as possible.\n\n## `lol_dto`\n\nThis repository hosts a `python` reference implementation in the form of a `dataclass`.\n\nA `dataclass` does not enforce type constraints but will raise linter warnings and allows IDEs to autocomplete field names.\n\nAnother module focused on transforming `MatchDto` and `MatchTimelineDto` to a `LolGame` can\n[be found here](https://github.com/mrtolkien/riot_transmute). Its\n[unit tests](https://github.com/mrtolkien/riot_transmute/blob/master/tests/test_riot_transmute.py)\nand [JSON examples](https://github.com/mrtolkien/riot_transmute/tree/master/json_examples)\nare useful sources to better understand the data structure.\n\n### LolGame DTO overview\n\n```ascii\ngame: dict\n├── sources: dict\n├── teams: dict\n|   ├── uniqueIdentifiers: dict\n│   ├── bans: list\n│   ├── monstersKills: list\n│   ├── buildingsKills: list\n│   └── players: list\n│       ├── uniqueIdentifiers: dict\n│       ├── endOfGameStats: dict\n│       │   └── items: list\n│       ├── summonersSpells: list\n│       ├── runes: list\n│       ├── snapshots: list\n│       ├── itemsEvents: list\n│       ├── wardsEvents: list\n│       └── skillsLevelUpEvents: list\n├── kills: list\n├── picksBans: list\n└── pauses: list\n```\n\n### Game\n\n- `sources` represents unique identifiers for this game for a given data source\n  - `"riotLolApi": { "gameId": 4409190456, "platformId": "KR" }`\n- `teams` has properties equal to `\'BLUE\'` and `\'RED\'`\n- `kills` are present directly at the root of the `game` object as they refer to multiple players through\n  `killerId`, `victimId`, and `assistingParticipantsIds`\n  - We have to rely on the arbitrary `participantId` given by the Riot API because:\n    - Relying on `championId` makes it incompatible with blind pick\n    - Relying on `inGameName` does not work for `MatchTimeline` objects from the Riot API\n- `picksBans` represents the full picks and bans and is mostly used for esports games\n\n### Team\n\n- `bans` is a simple list of `id` of champions banned by the team.\n- `monsterKills` and `buildingKills` are at the `team` level because they are team-wide\n  - They both define their own `BuildingKillEvent` and `MonsterKillEvent` DTOs that are very different from Riot’s API\n- `players` are simply in a list because no unique key arises\n  - `roles` are not guaranteed to be defined and unique\n\n### Player\n\n- `id` refers to Riot API’s `participantId` and is unfortunately necessary to be able to link different objects coming\n  from it\n- `uniqueIdentifiers` is similar to `game[\'sources\']` in that it represents a unique identifier for the player in the\n  specified data source\n  - `"riotLolApi": { "accountId": "3VcaXNMW8jq3adCqG0k0RPBaxoNL08NFXH_h4_2sKI_iEKw", "platformId": "KR" }`\n- `endOfGameStats` represents statistics that are only available at the end of the game, including end of game `items`\n  as well as `kills`, `totalDamageDealtToChampions`, ...\n- `snapshots` is a list of timestamped information about the player, mostly `gold` and `position` at given timestamps\n- `itemsEvents` are item-related events from players (buying, selling, undoing, destroying)\n- `wardsEvents` are ward-related events from players (placing, destroying)\n- `skillsLevelUpEvents` are skills level up events from players\n\n## Contributing\n\nCurrently wanted contribution are:\n\n- Feedback about the data structure and field names\n- Implementation of the data structure in other programming languages\n- C/Rust/... functions to cast Riot API objects to this LolGame DTO as multiple languages can bind to them\n',
    'author': 'mrtolkien',
    'author_email': 'gary.mialaret+pypi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
