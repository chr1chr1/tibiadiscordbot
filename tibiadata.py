import requests


def get_deaths(user_input: str, prev: str) -> str:
    killer_name = user_input.split(', ')
    if user_input == 'femor':
        killer_name = ['orc warlord', 'orc leader']
    api_url = "https://api.tibiadata.com/v4/world/Havera"
    response = requests.get(api_url)
    world = response.json()
    if response.status_code != 200:
        return 'Error'

    res = ''
    for player in world['world']['online_players']:
        name = player['name']
        name = name.replace(' ', '%20')
        api_url = "https://api.tibiadata.com/v4/character/" + name
        response = requests.get(api_url)
        char = response.json()
        if 'deaths' in char['character']:
            for death in char['character']['deaths']:
                for killer in death['killers']:
                    if killer['name'].lower() in killer_name:
                        if death['time'] > prev:
                            res += char['character']['character']['name']+' '+death['time']+' '+death['reason']+'\n'
    return res
