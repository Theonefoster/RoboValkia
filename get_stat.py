from get_stats import get_stats

def get_rank():
    player_to_find = "valkia"
    unique_str="image-player image-tiny"
    headers = {"User-Agent": "James 1.0"}

    r = requests.get("https://www.overbuff.com/heroes/pharah/rankings", headers=headers)

    page = r.text.lower()
    
    try:
        player_str_index = page.index(player_to_find)
        first_chunk_page = page[:player_str_index]
        rank = first_chunk_page.count(unique_str) + 1
        if rank == 1:
            output = "Valkia is currently Ranked #1 Pharah on Overbuff! PogChamp valkPog https://www.overbuff.com/heroes/pharah"
        else:
            output = "Valkia is currently Ranked #{rank} Pharah on Overbuff! https://www.overbuff.com/heroes/pharah".format(rank=rank)
    except ValueError:
        output = "Rank not found :("

    return output

def get_stat(original_stat):
    stat = original_stat
    
    if stat=="" or stat in ["rank", "pharah"]:
        output = get_rank()
    else:
        stat_types = {
            "Medals": ["medals", "medal"],
            "Time Played": ["timeplayed", "playtime", "time", "played"],
            "Win Rate": ["winrate", "winpercentage", "wins"],
            "On Fire": ["onfire", "fire"],
            "Eliminations": ["elims", "eliminations", "elim", "kills"],
            "Obj Kills": ["objectivekills", "objkills"],
            "Obj Time": ["objectivetime", "objtime"],
            "Damage": ["dmg", "damage", "damagedone"],
            "Deaths": ["deaths", "death"],
            "Weapon Acc": ["accuracy", "weaponaccuracy"],
            "Direct Hits": ["directs", "direct", "directhits", "directshots"],
            "Solo Kills": ["solokills", "solokill", "solos", "solo"],
            "Final Blows": ["finalblows", "finalblow", "finals", "final"],
            "Env Kills": ["environmentals", "envkills", "environmentalkills"],
            "Barrage Kills": ["ult", "barragekills", "ultkills"],
            "E:D Ratio": ["kd", "ed", "ratio", "e:d", "k:d"],
            "Voting Cards": ["cards", "votingcards", "votes"],
            "Gold Medals": ["golds", "gold"],
            "Silver Medals": ["silvers", "silver"],
            "Bronze Medals": ["bronzes", "bronze"],
            }
        stat = stat.lower().replace(" ", "")

        for stat_type in stat_types:
            if stat in stat_types[stat_type]:
                stat = stat_type
                break
        else:
            stat="notfound"

        if stat == "notfound":
            output = "No statistic named " + original_stat + " was found. Check this link for all of Valkia's Pharah statistics: https://www.overbuff.com/players/pc/Valkia/heroes/pharah"   
        else:
            stats = get_stats()
            
            if stat not in ["Win Rate", "E:D Ratio"]:
                # stat = stat + " per game"
                out_stat = stat + " per game"
            else:
                out_stat = stat
            
            output = "Valkia's " + out_stat + " with pharah is currently " + stats[stat] + ", according to https://www.overbuff.com/players/pc/Valkia/heroes/pharah"
            
    return output