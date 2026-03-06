import json
#main themes to choose from
themes_to_load = ["default","light","sunset","nordic","forest"]

def load_theme(path="settings.json", theme_to_load="default"):
    #decide on which theme to load and load it
    with open(path, "r") as f:
        data = json.load(f)
    return data.get(theme_to_load, data)

def get_all_colours():
    #loads ind.txt and reads from it
    with open("ind.txt","r") as file:
        data = file.readlines()
    ind = int(data[0])
    #load and assign colours to different themes, return all colours as a list
    THEME = load_theme(theme_to_load=themes_to_load[ind])
    WHITE = tuple(THEME["1"])
    BLACK = tuple(THEME["2"])
    BROWN = tuple(THEME["3"])
    GREEN = tuple(THEME["4"])
    GREY = tuple(THEME["5"])
    TEAL = tuple(THEME["6"])
    background = tuple(THEME["background"])
    box_colour = tuple(THEME["box_colour"])
    YELLOW = tuple(THEME["yellow"])
    CYAN = tuple(THEME["cyan"])
    NAVY = tuple(THEME["navy"])
    RED = tuple(THEME["red"])
    return [WHITE,BLACK,BROWN,GREEN,GREY,TEAL,background,box_colour,YELLOW,CYAN,NAVY,RED]

