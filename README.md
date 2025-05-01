# sauna - WIP

Help find multiplayer games you and your friends have in common.

Your friends list must be made public, and friends have to make their games owned public as well.

## usage

After installing just run

`sauna`

Without installing run the package from inside the repo folder

`python3 -m ./sauna --output games.json`

## Steam API key

To register for a steam API key use this [link](https://steamcommunity.com/dev/apikey)

## Configuration

Inside this project directory is a **sauna.toml.example** file that holds a template config. Change it to **sauna.toml** and fill in your real credentials.

### config values

| config | value |
| -------- | -------- |
| owner    | Your Steam ID |
| steamkey | API Key |
| friends  | Array of Steam IDs, usernames or profile links |

### example config
```toml
owner = '12341234123412341'
steamkey = '12341234123412341234123412341234'
friends = [
    'john117',
    'https://steamcommunity.com/id/johnsprofile/',
    '34561125302721235',
]
```

## Installation

```
git clone <REPO URL>
cd sauna
pip install -e .
```

## How it works

This will make calls to the Steam API Web service where you can request information about different parts of steam's services.

1. identify all your games in your steam library. Then filter for only the multiplayer games.

2. sauna will make request to find all your friends on steam. Then it will filter the friends you have
identified in the sauna configuration file.

3. For each friend thats found a list of all their games will be populated.

4. Once all friends libraries are populated, it will populate a new list of only games that your group of
friends all own!