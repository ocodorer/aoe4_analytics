import json
import os

def snake_to_camel_case_id(snake_case_id:str) -> str:
    return "".join(x.capitalize() for x in snake_case_id.lower().split("_"))

def normalize(string, civilization):
    string = "".join(x.capitalize() for x in string.lower().split("_"))  + "-" + civilization
    return string.lower()

def print_ids():
    all_ids = []
    registered_events = json.load(open("GameEvents.json", "r"))
    game_ids = list(set([i["action"] for i in registered_events]))
    for file in ["DimTechnology.json", "DimUpgrade.json", "DimUnit.json", "DimBuilding.json"]:
        technologies = json.load(open(file, "r"))
        t_keys = [t["AttributeName"] for t in technologies]
        for t_key in t_keys:
            if t_key == "upgrade_tech_university_biology_improved_mon":
                print(t_key)
            for gid in game_ids:
                # if snake_to_camel_case_id(e["action"].lower()) == t["AttributeName"].lower():
                normalized_a = normalize(gid)
                normalized_b =  normalize(t_key)
                #print(normalized_a, normalized_b)
                if normalized_a == normalized_b:
                    all_ids.append({"data":t_key, "game":gid, "a":normalized_a, "b":normalized_b})
                    # game_ids.remove(gid)
                    # t_keys.remove(t_key)
                    break
            
    # 
    # for i in game_ids:
    #    all_ids[i] = ""
    for gid in game_ids:
        normalized_a = normalize(gid)
        normalized_b =  None
        all_ids.append({"data":None, "game": gid, "a":normalized_a, "b":normalized_b})
    for t_key in t_keys:
        normalized_a = None
        normalized_b =  normalize(t_key)
        all_ids.append({"data":t_key, "game": None, "a":normalized_a, "b":normalized_b})
    json.dump(all_ids, open("map_ab.json", "w"), indent=1)


    complete = []
    all = []
    for row in all_ids:
        all.append(row["data"])
        if row["data"] is not None and row["game"] is not None:
            complete.append(all.append(row["data"]))
    for row in all:
        if row not in complete:
            print(row)

# print_ids()
#upgradetechuniversitybiologyimprovedmon
#upgradetechuniversitybiologyimprovedmon
#upgradetechuniversitybiologyimprovedmon 