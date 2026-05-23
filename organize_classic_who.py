from pathlib import Path
import os, shutil, re, argparse, logging

COLLECTION   = Path("/media/madmaxlgndklr/classic_who1/Doctor Who - The Complete Classic 26 Seasons Collection + Extras")
SHOW_DEST    = Path("/media/madmaxlgndklr/classic_who1/Doctor Who (1963)")
MOVIE_DEST   = Path("/media/madmaxlgndklr/classic_who1/Movies")
SEASON1_FLAT = COLLECTION / "Doctor Who Season 1"
TV_MOVIE_DIR = COLLECTION / "Doctor Who - SXXEXX (156) - Television Movie"

SPECIALS = [
    {
        "title": "An Unearthly Child (Unaired Pilot)",
        "folder": "Doctor Who - S01E00 (000) - Unaired Pilot.avi",
        "episode_source": "loose",
        "episodes": [(0, 1, "An Unearthly Child (Unaired Pilot)", False)],
        "se_entries": [],
    },
    {
        "title": "Shada",
        "folder": "Doctor Who - S17E06 (---) - Shada - Parts 1-6 - Unfinished Serial",
        "episode_source": "serial",
        "episodes": [
            (0, 2, "Shada Part One", False),
            (0, 3, "Shada Part Two", False),
            (0, 4, "Shada Part Three", False),
            (0, 5, "Shada Part Four", False),
            (0, 6, "Shada Part Five", False),
            (0, 7, "Shada Part Six", False),
        ],
        "se_entries": [],
    },
]

SERIALS = [
    # TV Movie — goes to Movies library
    {
        "title": "Doctor Who (1996)",
        "folder": None,
        "episode_source": "tv_movie",
        "episodes": [(0, 0, "Doctor Who (1996)", False)],
        "se_entries": [],
    },
    # --- SEASON 1 ---
    {
        "title": "An Unearthly Child",
        "folder": None,
        "episode_source": "season1_flat",
        "episodes": [
            (1, 1,  "An Unearthly Child", False),
            (1, 2,  "The Cave of Skulls", False),
            (1, 3,  "The Forest of Fear", False),
            (1, 4,  "The Firemaker", False),
        ],
        "se_entries": [],
    },
    {
        "title": "The Daleks",
        "folder": None,
        "episode_source": "season1_flat",
        "episodes": [
            (1, 5,  "The Dead Planet", False),
            (1, 6,  "The Survivors", False),
            (1, 7,  "The Escape", False),
            (1, 8,  "The Ambush", False),
            (1, 9,  "The Expedition", False),
            (1, 10, "The Ordeal", False),
            (1, 11, "The Rescue", False),
        ],
        "se_entries": [],
    },
    {
        "title": "The Edge of Destruction",
        "folder": "Doctor Who - S01E03 (003) - The Edge of Destruction - Parts 1-2",
        "episode_source": "season1_flat",
        "episodes": [
            (1, 12, "The Edge of Destruction", False),
            (1, 13, "The Brink of Disaster", False),
        ],
        "se_entries": [],
    },
    {
        "title": "Marco Polo",
        "folder": "Doctor Who - S01E04 (004) - Marco Polo - Parts 1-7",
        "episode_source": "season1_flat",
        "episodes": [
            (1, 14, "The Roof of the World", True),
            (1, 15, "The Singing Sands", True),
            (1, 16, "Five Hundred Eyes", True),
            (1, 17, "The Wall of Lies", True),
            (1, 18, "Rider from Shang-Tu", True),
            (1, 19, "Mighty Kublai Khan", True),
            (1, 20, "Assassin at Peking", True),
        ],
        "se_entries": [],
    },
    {
        "title": "The Keys of Marinus",
        "folder": "Doctor Who - S01E05 (005) - The Keys of Marinus - Parts 1-6",
        "episode_source": "season1_flat",
        "episodes": [
            (1, 21, "The Sea of Death", False),
            (1, 22, "The Velvet Web", False),
            (1, 23, "The Screaming Jungle", False),
            (1, 24, "The Snows of Terror", False),
            (1, 25, "Sentence of Death", False),
            (1, 26, "The Keys of Marinus", False),
        ],
        "se_entries": [],
    },
    {
        "title": "The Aztecs",
        "folder": "Doctor Who - S01E06 (006) - The Aztecs - Parts 1-4",
        "episode_source": "serial",
        "episodes": [
            (1, 27, "The Temple of Evil", False),
            (1, 28, "The Warriors of Death", False),
            (1, 29, "The Bride of Sacrifice", False),
            (1, 30, "The Day of Darkness", False),
        ],
        "se_entries": [],
    },
    {
        "title": "The Sensorites",
        "folder": "Doctor Who - S01E07 (007) - The Sensorites - Parts 1-6",
        "episode_source": "serial",
        "episodes": [
            (1, 31, "Strangers in Space", False),
            (1, 32, "The Unwilling Warriors", False),
            (1, 33, "Hidden Danger", False),
            (1, 34, "A Race Against Death", False),
            (1, 35, "Kidnap", False),
            (1, 36, "A Desperate Venture", False),
        ],
        "se_entries": [],
    },
    {
        "title": "The Reign of Terror",
        "folder": "Doctor Who - S01E08 (008) - The Reign of Terror - Parts 1-6",
        "episode_source": "serial",
        "episodes": [
            (1, 37, "A Land of Fear", False),
            (1, 38, "Guests of Madame Guillotine", False),
            (1, 39, "A Change of Identity", False),
            (1, 40, "The Tyrant of France", False),
            (1, 41, "A Bargain of Necessity", True),
            (1, 42, "Prisoners of Conciergerie", True),
        ],
        "se_entries": [],
    },
    # --- SEASON 2 ---
    {"title":"Planet of Giants","folder":"Doctor Who - S02E01 (009) - Planet of Giants - Parts 1-3","episode_source":"serial","episodes":[(2,1,"Planet of Giants",False),(2,2,"Dangerous Journey",False),(2,3,"Crisis",False)],"se_entries":[]},
    {"title":"The Dalek Invasion of Earth","folder":"Doctor Who - S02E02 (010) - The Dalek Invasion of Earth - Parts 1-6","episode_source":"serial","episodes":[(2,4,"World's End",False),(2,5,"The Daleks",False),(2,6,"Day of Reckoning",False),(2,7,"The End of Tomorrow",False),(2,8,"The Waking Ally",False),(2,9,"Flashpoint",False)],"se_entries":[]},
    {"title":"The Rescue","folder":"Doctor Who - S02E03 (011) - The Rescue - Parts 1-2","episode_source":"serial","episodes":[(2,10,"The Powerful Enemy",False),(2,11,"Desperate Measures",False)],"se_entries":[]},
    {"title":"The Romans","folder":"Doctor Who - S02E04 (012) - The Romans - Parts 1-4","episode_source":"serial","episodes":[(2,12,"The Slave Traders",False),(2,13,"All Roads Lead to Rome",False),(2,14,"Conspiracy",False),(2,15,"Inferno",False)],"se_entries":[]},
    {"title":"The Web Planet","folder":"Doctor Who - S02E05 (013) - The Web Planet - Parts 1-6","episode_source":"serial","episodes":[(2,16,"The Web Planet",False),(2,17,"The Zarbi",False),(2,18,"Escape to Danger",False),(2,19,"Crater of Needles",False),(2,20,"Invasion",False),(2,21,"The Centre",False)],"se_entries":[]},
    {"title":"The Crusade","folder":"Doctor Who - S02E06 (014) - The Crusade - Parts 1-4","episode_source":"serial","episodes":[(2,22,"The Lion",False),(2,23,"The Knight of Jaffa",True),(2,24,"The Wheel of Fortune",False),(2,25,"The Warlords",True)],"se_entries":[]},
    {"title":"The Space Museum","folder":"Doctor Who - S02E07 (015) - The Space Museum - Parts 1-4","episode_source":"serial","episodes":[(2,26,"The Space Museum",False),(2,27,"The Dimensions of Time",False),(2,28,"The Search",False),(2,29,"The Final Phase",False)],"se_entries":[]},
    {"title":"The Chase","folder":"Doctor Who - S02E08 (016) - The Chase - Parts 1-6","episode_source":"serial","episodes":[(2,30,"The Executioners",False),(2,31,"The Death of Time",False),(2,32,"Flight Through Eternity",False),(2,33,"Journey into Terror",False),(2,34,"The Death of Doctor Who",False),(2,35,"The Planet of Decision",False)],"se_entries":[]},
    {"title":"The Time Meddler","folder":"Doctor Who - S02E09 (017) - The Time Meddler - Parts 1-4","episode_source":"serial","episodes":[(2,36,"The Watcher",False),(2,37,"The Meddling Monk",False),(2,38,"A Battle of Wits",False),(2,39,"Checkmate",False)],"se_entries":[]},
    # --- SEASON 3 ---
    {"title":"Galaxy 4","folder":"Doctor Who - S03E01 (018) - Galaxy 4 - Parts 1-4","episode_source":"serial","episodes":[(3,1,"Four Hundred Dawns",True),(3,2,"Trap of Steel",True),(3,3,"Air Lock",False),(3,4,"The Exploding Planet",True)],"se_entries":[]},
    {"title":"Mission to the Unknown","folder":"Doctor Who - S03E02 (019) - Mission to the Unknown - Parts 1-1","episode_source":"serial","episodes":[(3,5,"Mission to the Unknown",True)],"se_entries":[]},
    {"title":"The Myth Makers","folder":"Doctor Who - S03E03 (020) - The Myth Makers - Parts 1-4","episode_source":"serial","episodes":[(3,6,"Temple of Secrets",True),(3,7,"Small Prophet Quick Return",True),(3,8,"Death of a Spy",True),(3,9,"Horse of Destruction",True)],"se_entries":[]},
    {"title":"The Daleks Master Plan","folder":"Doctor Who - S03E04 (021) - The Daleks’ Master Plan - Parts 1-12","episode_source":"serial","episodes":[(3,10,"The Nightmare Begins",True),(3,11,"Day of Armageddon",False),(3,12,"Devil's Planet",True),(3,13,"The Traitors",True),(3,14,"Counter Plot",False),(3,15,"Coronas of the Sun",True),(3,16,"The Feast of Steven",False),(3,17,"Volcano",True),(3,18,"Golden Death",True),(3,19,"Escape Switch",True),(3,20,"The Abandoned Planet",True),(3,21,"Destruction of Time",True)],"se_entries":[]},
    {"title":"The Massacre of St Bartholomew's Eve","folder":"Doctor Who - S03E05 (022) - The Massacre of St Bartholomew’s Eve - Parts 1-4","episode_source":"serial","episodes":[(3,22,"War of God",True),(3,23,"The Sea Beggar",True),(3,24,"Priest of Death",True),(3,25,"Bell of Doom",True)],"se_entries":[]},
    {"title":"The Ark","folder":"Doctor Who - S03E06 (023) - The Ark - Parts 1-4","episode_source":"serial","episodes":[(3,26,"The Steel Sky",False),(3,27,"The Plague",False),(3,28,"The Return",False),(3,29,"The Bomb",False)],"se_entries":[]},
    {"title":"The Celestial Toymaker","folder":"Doctor Who - S03E07 (024) - The Celestial Toymaker - Parts 1-4","episode_source":"serial","episodes":[(3,30,"The Celestial Toyroom",True),(3,31,"The Hall of Dolls",True),(3,32,"The Dancing Floor",True),(3,33,"The Final Test",False)],"se_entries":[]},
    {"title":"The Gunfighters","folder":"Doctor Who - S03E08 (025) - The Gunfighters - Parts 1-4","episode_source":"serial","episodes":[(3,34,"A Holiday for the Doctor",False),(3,35,"Don't Shoot the Pianist",False),(3,36,"Johnny Ringo",False),(3,37,"The O.K. Corral",False)],"se_entries":[]},
    {"title":"The Savages","folder":"Doctor Who - S03E09 (026) - The Savages - Parts 1-4","episode_source":"serial","episodes":[(3,38,"The Savages Part One",True),(3,39,"The Savages Part Two",True),(3,40,"The Savages Part Three",True),(3,41,"The Savages Part Four",True)],"se_entries":[]},
    {"title":"The War Machines","folder":"Doctor Who - S03E10 (027) - The War Machines - Parts 1-4","episode_source":"serial","episodes":[(3,42,"The War Machines Part One",False),(3,43,"The War Machines Part Two",False),(3,44,"The War Machines Part Three",False),(3,45,"The War Machines Part Four",False)],"se_entries":[]},
    # --- SEASON 4 ---
    {"title":"The Smugglers","folder":"Doctor Who - S04E01 (028) - The Smugglers - Parts 1-4","episode_source":"serial","episodes":[(4,1,"The Smugglers Part One",True),(4,2,"The Smugglers Part Two",True),(4,3,"The Smugglers Part Three",True),(4,4,"The Smugglers Part Four",True)],"se_entries":[]},
    {"title":"The Tenth Planet","folder":"Doctor Who - S04E02 (029) - The Tenth Planet - Parts 1-4","episode_source":"serial","episodes":[(4,5,"The Tenth Planet Part One",False),(4,6,"The Tenth Planet Part Two",False),(4,7,"The Tenth Planet Part Three",False),(4,8,"The Tenth Planet Part Four",True)],"se_entries":[]},
    {"title":"The Power of the Daleks","folder":"Doctor Who - S04E03 (030) - The Power of the Daleks - Parts 1-6","episode_source":"serial","episodes":[(4,9,"The Power of the Daleks Part One",True),(4,10,"The Power of the Daleks Part Two",True),(4,11,"The Power of the Daleks Part Three",True),(4,12,"The Power of the Daleks Part Four",True),(4,13,"The Power of the Daleks Part Five",True),(4,14,"The Power of the Daleks Part Six",True)],"se_entries":[]},
    {"title":"The Highlanders","folder":"Doctor Who - S04E04 (031) - The Highlanders - Parts 1-4","episode_source":"serial","episodes":[(4,15,"The Highlanders Part One",True),(4,16,"The Highlanders Part Two",True),(4,17,"The Highlanders Part Three",True),(4,18,"The Highlanders Part Four",True)],"se_entries":[]},
    {"title":"The Underwater Menace","folder":"Doctor Who - S04E05 (032) - The Underwater Menace - Parts 1-4","episode_source":"serial","episodes":[(4,19,"The Underwater Menace Part One",True),(4,20,"The Underwater Menace Part Two",True),(4,21,"The Underwater Menace Part Three",False),(4,22,"The Underwater Menace Part Four",False)],"se_entries":[]},
    {"title":"The Moonbase","folder":"Doctor Who - S04E06 (033) - The Moonbase - Parts 1-4","episode_source":"serial","episodes":[(4,23,"The Moonbase Part One",True),(4,24,"The Moonbase Part Two",False),(4,25,"The Moonbase Part Three",True),(4,26,"The Moonbase Part Four",False)],"se_entries":[]},
    {"title":"The Macra Terror","folder":"Doctor Who - S04E07 (034) - The Macra Terror - Parts 1-4","episode_source":"serial","episodes":[(4,27,"The Macra Terror Part One",True),(4,28,"The Macra Terror Part Two",True),(4,29,"The Macra Terror Part Three",True),(4,30,"The Macra Terror Part Four",True)],"se_entries":[]},
    {"title":"The Faceless Ones","folder":"Doctor Who - S04E08 (035) - The Faceless Ones - Parts 1-6","episode_source":"serial","episodes":[(4,31,"The Faceless Ones Part One",False),(4,32,"The Faceless Ones Part Two",True),(4,33,"The Faceless Ones Part Three",True),(4,34,"The Faceless Ones Part Four",True),(4,35,"The Faceless Ones Part Five",True),(4,36,"The Faceless Ones Part Six",False)],"se_entries":[]},
    {"title":"The Evil of the Daleks","folder":"Doctor Who - S04E09 (036) - The Evil of the Daleks - Parts 1-7","episode_source":"serial","episodes":[(4,37,"The Evil of the Daleks Part One",True),(4,38,"The Evil of the Daleks Part Two",False),(4,39,"The Evil of the Daleks Part Three",True),(4,40,"The Evil of the Daleks Part Four",True),(4,41,"The Evil of the Daleks Part Five",True),(4,42,"The Evil of the Daleks Part Six",True),(4,43,"The Evil of the Daleks Part Seven",True)],"se_entries":[]},
    # --- SEASON 5 ---
    {"title":"The Tomb of the Cybermen","folder":"Doctor Who - S05E01 (037) - The Tomb of the Cybermen - Parts 1-4","episode_source":"serial","episodes":[(5,1,"The Tomb of the Cybermen Part One",False),(5,2,"The Tomb of the Cybermen Part Two",False),(5,3,"The Tomb of the Cybermen Part Three",False),(5,4,"The Tomb of the Cybermen Part Four",False)],"se_entries":[]},
    {"title":"The Abominable Snowmen","folder":"Doctor Who - S05E02 (038) - The Abominable Snowmen - Parts 1-6","episode_source":"serial","episodes":[(5,5,"The Abominable Snowmen Part One",True),(5,6,"The Abominable Snowmen Part Two",False),(5,7,"The Abominable Snowmen Part Three",True),(5,8,"The Abominable Snowmen Part Four",True),(5,9,"The Abominable Snowmen Part Five",True),(5,10,"The Abominable Snowmen Part Six",True)],"se_entries":[]},
    {"title":"The Ice Warriors","folder":"Doctor Who - S05E03 (039) - The Ice Warriors - Parts 1-6","episode_source":"serial","episodes":[(5,11,"The Ice Warriors Part One",False),(5,12,"The Ice Warriors Part Two",True),(5,13,"The Ice Warriors Part Three",True),(5,14,"The Ice Warriors Part Four",False),(5,15,"The Ice Warriors Part Five",False),(5,16,"The Ice Warriors Part Six",False)],"se_entries":[]},
    {"title":"The Enemy of the World","folder":"Doctor Who - S05E04 (040) - The Enemy of the World - Parts 1-6","episode_source":"serial","episodes":[(5,17,"The Enemy of the World Part One",False),(5,18,"The Enemy of the World Part Two",False),(5,19,"The Enemy of the World Part Three",False),(5,20,"The Enemy of the World Part Four",False),(5,21,"The Enemy of the World Part Five",False),(5,22,"The Enemy of the World Part Six",False)],"se_entries":[]},
    {"title":"The Web of Fear","folder":"Doctor Who - S05E05 (041) - The Web of Fear - Parts 1-6","episode_source":"serial","episodes":[(5,23,"The Web of Fear Part One",False),(5,24,"The Web of Fear Part Two",True),(5,25,"The Web of Fear Part Three",False),(5,26,"The Web of Fear Part Four",False),(5,27,"The Web of Fear Part Five",False),(5,28,"The Web of Fear Part Six",False)],"se_entries":[]},
    {"title":"Fury from the Deep","folder":"Doctor Who - S05E06 (042) - Fury from the Deep - Parts 1-6","episode_source":"serial","episodes":[(5,29,"Fury from the Deep Part One",True),(5,30,"Fury from the Deep Part Two",True),(5,31,"Fury from the Deep Part Three",True),(5,32,"Fury from the Deep Part Four",True),(5,33,"Fury from the Deep Part Five",True),(5,34,"Fury from the Deep Part Six",True)],"se_entries":[]},
    {"title":"The Wheel in Space","folder":"Doctor Who - S05E07 (043) - The Wheel in Space - Parts 1-6","episode_source":"serial","episodes":[(5,35,"The Wheel in Space Part One",True),(5,36,"The Wheel in Space Part Two",True),(5,37,"The Wheel in Space Part Three",False),(5,38,"The Wheel in Space Part Four",True),(5,39,"The Wheel in Space Part Five",True),(5,40,"The Wheel in Space Part Six",False)],"se_entries":[]},
    # --- SEASON 6 ---
    {"title":"The Dominators","folder":"Doctor Who - S06E01 (044) - The Dominators - Parts 1-5","episode_source":"serial","episodes":[(6,1,"The Dominators Part One",False),(6,2,"The Dominators Part Two",False),(6,3,"The Dominators Part Three",False),(6,4,"The Dominators Part Four",False),(6,5,"The Dominators Part Five",False)],"se_entries":[]},
    {"title":"The Mind Robber","folder":"Doctor Who - S06E02 (045) - The Mind Robber - Parts 1-5","episode_source":"serial","episodes":[(6,6,"The Mind Robber Part One",False),(6,7,"The Mind Robber Part Two",False),(6,8,"The Mind Robber Part Three",False),(6,9,"The Mind Robber Part Four",False),(6,10,"The Mind Robber Part Five",False)],"se_entries":[]},
    {"title":"The Invasion","folder":"Doctor Who - S06E03 (046) - The Invasion - Parts 1-8","episode_source":"serial","episodes":[(6,11,"The Invasion Part One",True),(6,12,"The Invasion Part Two",False),(6,13,"The Invasion Part Three",False),(6,14,"The Invasion Part Four",False),(6,15,"The Invasion Part Five",False),(6,16,"The Invasion Part Six",False),(6,17,"The Invasion Part Seven",True),(6,18,"The Invasion Part Eight",False)],"se_entries":[]},
    {"title":"The Krotons","folder":"Doctor Who - S06E04 (047) - The Krotons - Parts 1-4","episode_source":"serial","episodes":[(6,19,"The Krotons Part One",False),(6,20,"The Krotons Part Two",False),(6,21,"The Krotons Part Three",False),(6,22,"The Krotons Part Four",False)],"se_entries":[]},
    {"title":"The Seeds of Death","folder":"Doctor Who - S06E05 (048) - The Seeds of Death - Parts 1-6","episode_source":"serial","episodes":[(6,23,"The Seeds of Death Part One",False),(6,24,"The Seeds of Death Part Two",False),(6,25,"The Seeds of Death Part Three",False),(6,26,"The Seeds of Death Part Four",False),(6,27,"The Seeds of Death Part Five",False),(6,28,"The Seeds of Death Part Six",False)],"se_entries":[]},
    {"title":"The Space Pirates","folder":"Doctor Who - S06E06 (049) - The Space Pirates - Parts 1-6","episode_source":"serial","episodes":[(6,29,"The Space Pirates Part One",True),(6,30,"The Space Pirates Part Two",False),(6,31,"The Space Pirates Part Three",True),(6,32,"The Space Pirates Part Four",True),(6,33,"The Space Pirates Part Five",True),(6,34,"The Space Pirates Part Six",True)],"se_entries":[]},
    {"title":"The War Games","folder":"Doctor Who - S06E07 (050) - The War Games - Parts 1-10","episode_source":"serial","episodes":[(6,35,"The War Games Part One",False),(6,36,"The War Games Part Two",False),(6,37,"The War Games Part Three",False),(6,38,"The War Games Part Four",False),(6,39,"The War Games Part Five",False),(6,40,"The War Games Part Six",False),(6,41,"The War Games Part Seven",False),(6,42,"The War Games Part Eight",False),(6,43,"The War Games Part Nine",False),(6,44,"The War Games Part Ten",False)],"se_entries":[]},
    # --- SEASON 7 ---
    {"title":"Spearhead from Space","folder":"Doctor Who - S07E01 (051) - Spearhead from Space - Parts 1-4","episode_source":"serial","episodes":[(7,1,"Spearhead from Space Part One",False),(7,2,"Spearhead from Space Part Two",False),(7,3,"Spearhead from Space Part Three",False),(7,4,"Spearhead from Space Part Four",False)],"se_entries":[]},
    {"title":"Doctor Who and the Silurians","folder":"Doctor Who - S07E02 (052) - Doctor Who and the Silurians - Parts 1-7","episode_source":"serial","episodes":[(7,5,"Doctor Who and the Silurians Part One",False),(7,6,"Doctor Who and the Silurians Part Two",False),(7,7,"Doctor Who and the Silurians Part Three",False),(7,8,"Doctor Who and the Silurians Part Four",False),(7,9,"Doctor Who and the Silurians Part Five",False),(7,10,"Doctor Who and the Silurians Part Six",False),(7,11,"Doctor Who and the Silurians Part Seven",False)],"se_entries":[]},
    {"title":"The Ambassadors of Death","folder":"Doctor Who - S07E03 (053) - The Ambassadors of Death - Parts 1-7","episode_source":"serial","episodes":[(7,12,"The Ambassadors of Death Part One",False),(7,13,"The Ambassadors of Death Part Two",False),(7,14,"The Ambassadors of Death Part Three",False),(7,15,"The Ambassadors of Death Part Four",False),(7,16,"The Ambassadors of Death Part Five",False),(7,17,"The Ambassadors of Death Part Six",False),(7,18,"The Ambassadors of Death Part Seven",False)],"se_entries":[]},
    {"title":"Inferno","folder":"Doctor Who - S07E04 (054) - Inferno - Parts 1-7","episode_source":"serial","episodes":[(7,19,"Inferno Part One",False),(7,20,"Inferno Part Two",False),(7,21,"Inferno Part Three",False),(7,22,"Inferno Part Four",False),(7,23,"Inferno Part Five",False),(7,24,"Inferno Part Six",False),(7,25,"Inferno Part Seven",False)],"se_entries":[]},
    # --- SEASON 8 ---
    {"title":"Terror of the Autons","folder":"Doctor Who - S08E01 (055) - Terror of the Autons - Parts 1-4","episode_source":"serial","episodes":[(8,1,"Terror of the Autons Part One",False),(8,2,"Terror of the Autons Part Two",False),(8,3,"Terror of the Autons Part Three",False),(8,4,"Terror of the Autons Part Four",False)],"se_entries":[]},
    {"title":"The Mind of Evil","folder":"Doctor Who - S08E02 (056) - The Mind of Evil - Parts 1-6","episode_source":"serial","episodes":[(8,5,"The Mind of Evil Part One",False),(8,6,"The Mind of Evil Part Two",False),(8,7,"The Mind of Evil Part Three",False),(8,8,"The Mind of Evil Part Four",False),(8,9,"The Mind of Evil Part Five",False),(8,10,"The Mind of Evil Part Six",False)],"se_entries":[]},
    {"title":"The Claws of Axos","folder":"Doctor Who - S08E03 (057) - The Claws of Axos - Parts 1-4","episode_source":"serial","episodes":[(8,11,"The Claws of Axos Part One",False),(8,12,"The Claws of Axos Part Two",False),(8,13,"The Claws of Axos Part Three",False),(8,14,"The Claws of Axos Part Four",False)],"se_entries":[]},
    {"title":"Colony in Space","folder":"Doctor Who - S08E04 (058) - Colony in Space - Parts 1-6","episode_source":"serial","episodes":[(8,15,"Colony in Space Part One",False),(8,16,"Colony in Space Part Two",False),(8,17,"Colony in Space Part Three",False),(8,18,"Colony in Space Part Four",False),(8,19,"Colony in Space Part Five",False),(8,20,"Colony in Space Part Six",False)],"se_entries":[]},
    {"title":"The Daemons","folder":"Doctor Who - S08E05 (059) - The Daemons - Parts 1-5","episode_source":"serial","episodes":[(8,21,"The Daemons Part One",False),(8,22,"The Daemons Part Two",False),(8,23,"The Daemons Part Three",False),(8,24,"The Daemons Part Four",False),(8,25,"The Daemons Part Five",False)],"se_entries":[]},
    # --- SEASON 9 ---
    {"title":"Day of the Daleks","folder":"Doctor Who - S09E01 (060) - Day of the Daleks - Parts 1-4","episode_source":"serial","episodes":[(9,1,"Day of the Daleks Part One",False),(9,2,"Day of the Daleks Part Two",False),(9,3,"Day of the Daleks Part Three",False),(9,4,"Day of the Daleks Part Four",False),(9,27,"Day of the Daleks Part One (Special Edition)",False),(9,28,"Day of the Daleks Part Two (Special Edition)",False),(9,29,"Day of the Daleks Part Three (Special Edition)",False),(9,30,"Day of the Daleks Part Four (Special Edition)",False)],"se_entries":[{"folder":"Doctor Who - S09E01 (060) - Day of the Daleks - Parts 1-4 (Special Edition)","episodes":[(9,27,"Day of the Daleks Part One (Special Edition)",False),(9,28,"Day of the Daleks Part Two (Special Edition)",False),(9,29,"Day of the Daleks Part Three (Special Edition)",False),(9,30,"Day of the Daleks Part Four (Special Edition)",False)],"include_extras":True}]},
    {"title":"The Curse of Peladon","folder":"Doctor Who - S09E02 (061) - The Curse of Peladon - Parts 1-4","episode_source":"serial","episodes":[(9,5,"The Curse of Peladon Part One",False),(9,6,"The Curse of Peladon Part Two",False),(9,7,"The Curse of Peladon Part Three",False),(9,8,"The Curse of Peladon Part Four",False)],"se_entries":[]},
    {"title":"The Sea Devils","folder":"Doctor Who - S09E03 (062) - The Sea Devils - Parts 1-6","episode_source":"serial","episodes":[(9,9,"The Sea Devils Part One",False),(9,10,"The Sea Devils Part Two",False),(9,11,"The Sea Devils Part Three",False),(9,12,"The Sea Devils Part Four",False),(9,13,"The Sea Devils Part Five",False),(9,14,"The Sea Devils Part Six",False)],"se_entries":[]},
    {"title":"The Mutants","folder":"Doctor Who - S09E04 (063) - The Mutants - Parts 1-6","episode_source":"serial","episodes":[(9,15,"The Mutants Part One",False),(9,16,"The Mutants Part Two",False),(9,17,"The Mutants Part Three",False),(9,18,"The Mutants Part Four",False),(9,19,"The Mutants Part Five",False),(9,20,"The Mutants Part Six",False)],"se_entries":[]},
    {"title":"The Time Monster","folder":"Doctor Who - S09E05 (064) - The Time Monster - Parts 1-6","episode_source":"serial","episodes":[(9,21,"The Time Monster Part One",False),(9,22,"The Time Monster Part Two",False),(9,23,"The Time Monster Part Three",False),(9,24,"The Time Monster Part Four",False),(9,25,"The Time Monster Part Five",False),(9,26,"The Time Monster Part Six",False)],"se_entries":[]},
    # --- SEASON 10 ---
    {"title":"The Three Doctors","folder":"Doctor Who - S10E01 (065) - The Three Doctors - Parts 1-4","episode_source":"serial","episodes":[(10,1,"The Three Doctors Part One",False),(10,2,"The Three Doctors Part Two",False),(10,3,"The Three Doctors Part Three",False),(10,4,"The Three Doctors Part Four",False)],"se_entries":[]},
    {"title":"Carnival of Monsters","folder":"Doctor Who - S10E02 (066) - Carnival of Monsters - Parts 1-4","episode_source":"serial","episodes":[(10,5,"Carnival of Monsters Part One",False),(10,6,"Carnival of Monsters Part Two",False),(10,7,"Carnival of Monsters Part Three",False),(10,8,"Carnival of Monsters Part Four",False)],"se_entries":[]},
    {"title":"Frontier in Space","folder":"Doctor Who - S10E03 (067) - Frontier in Space - Parts 1-6","episode_source":"serial","episodes":[(10,9,"Frontier in Space Part One",False),(10,10,"Frontier in Space Part Two",False),(10,11,"Frontier in Space Part Three",False),(10,12,"Frontier in Space Part Four",False),(10,13,"Frontier in Space Part Five",False),(10,14,"Frontier in Space Part Six",False)],"se_entries":[]},
    {"title":"Planet of the Daleks","folder":"Doctor Who - S10E04 (068) - Planet of the Daleks - Parts 1-6","episode_source":"serial","episodes":[(10,15,"Planet of the Daleks Part One",False),(10,16,"Planet of the Daleks Part Two",False),(10,17,"Planet of the Daleks Part Three",False),(10,18,"Planet of the Daleks Part Four",False),(10,19,"Planet of the Daleks Part Five",False),(10,20,"Planet of the Daleks Part Six",False)],"se_entries":[]},
    {"title":"The Green Death","folder":"Doctor Who - S10E05 (069) - The Green Death - Parts 1-6","episode_source":"serial","episodes":[(10,21,"The Green Death Part One",False),(10,22,"The Green Death Part Two",False),(10,23,"The Green Death Part Three",False),(10,24,"The Green Death Part Four",False),(10,25,"The Green Death Part Five",False),(10,26,"The Green Death Part Six",False)],"se_entries":[]},
    # --- SEASON 11 ---
    {"title":"The Time Warrior","folder":"Doctor Who - S11E01 (070) - The Time Warrior - Parts 1-4","episode_source":"serial","episodes":[(11,1,"The Time Warrior Part One",False),(11,2,"The Time Warrior Part Two",False),(11,3,"The Time Warrior Part Three",False),(11,4,"The Time Warrior Part Four",False)],"se_entries":[]},
    {"title":"Invasion of the Dinosaurs","folder":"Doctor Who - S11E02 (071) - Invasion of the Dinosaurs - Parts 1-6","episode_source":"serial","episodes":[(11,5,"Invasion of the Dinosaurs Part One",False),(11,6,"Invasion of the Dinosaurs Part Two",False),(11,7,"Invasion of the Dinosaurs Part Three",False),(11,8,"Invasion of the Dinosaurs Part Four",False),(11,9,"Invasion of the Dinosaurs Part Five",False),(11,10,"Invasion of the Dinosaurs Part Six",False)],"se_entries":[]},
    {"title":"Death to the Daleks","folder":"Doctor Who - S11E03 (072) - Death to the Daleks - Parts 1-4","episode_source":"serial","episodes":[(11,11,"Death to the Daleks Part One",False),(11,12,"Death to the Daleks Part Two",False),(11,13,"Death to the Daleks Part Three",False),(11,14,"Death to the Daleks Part Four",False)],"se_entries":[]},
    {"title":"The Monster of Peladon","folder":"Doctor Who - S11E04 (073) - The Monster of Peladon - Parts 1-6","episode_source":"serial","episodes":[(11,15,"The Monster of Peladon Part One",False),(11,16,"The Monster of Peladon Part Two",False),(11,17,"The Monster of Peladon Part Three",False),(11,18,"The Monster of Peladon Part Four",False),(11,19,"The Monster of Peladon Part Five",False),(11,20,"The Monster of Peladon Part Six",False)],"se_entries":[]},
    {"title":"Planet of the Spiders","folder":"Doctor Who - S11E05 (074) - Planet of the Spiders - Parts 1-6","episode_source":"serial","episodes":[(11,21,"Planet of the Spiders Part One",False),(11,22,"Planet of the Spiders Part Two",False),(11,23,"Planet of the Spiders Part Three",False),(11,24,"Planet of the Spiders Part Four",False),(11,25,"Planet of the Spiders Part Five",False),(11,26,"Planet of the Spiders Part Six",False)],"se_entries":[]},
    # --- SEASON 12 ---
    {"title":"Robot","folder":"Doctor Who - S12E01 (075) - Robot - Parts 1-4","episode_source":"serial","episodes":[(12,1,"Robot Part One",False),(12,2,"Robot Part Two",False),(12,3,"Robot Part Three",False),(12,4,"Robot Part Four",False)],"se_entries":[]},
    {"title":"The Ark in Space","folder":"Doctor Who - S12E02 (076) - The Ark in Space - Parts 1-4","episode_source":"serial","episodes":[(12,5,"The Ark in Space Part One",False),(12,6,"The Ark in Space Part Two",False),(12,7,"The Ark in Space Part Three",False),(12,8,"The Ark in Space Part Four",False)],"se_entries":[]},
    {"title":"The Sontaran Experiment","folder":"Doctor Who - S12E03 (077) - The Sontaran Experiment - Parts 1-2","episode_source":"serial","episodes":[(12,9,"The Sontaran Experiment Part One",False),(12,10,"The Sontaran Experiment Part Two",False)],"se_entries":[]},
    {"title":"Genesis of the Daleks","folder":"Doctor Who - S12E04 (078) - Genesis of the Daleks - Parts 1-6","episode_source":"serial","episodes":[(12,11,"Genesis of the Daleks Part One",False),(12,12,"Genesis of the Daleks Part Two",False),(12,13,"Genesis of the Daleks Part Three",False),(12,14,"Genesis of the Daleks Part Four",False),(12,15,"Genesis of the Daleks Part Five",False),(12,16,"Genesis of the Daleks Part Six",False)],"se_entries":[]},
    {"title":"Revenge of the Cybermen","folder":"Doctor Who - S12E05 (079) - Revenge of the Cybermen - Parts 1-4","episode_source":"serial","episodes":[(12,17,"Revenge of the Cybermen Part One",False),(12,18,"Revenge of the Cybermen Part Two",False),(12,19,"Revenge of the Cybermen Part Three",False),(12,20,"Revenge of the Cybermen Part Four",False)],"se_entries":[]},
    # --- SEASON 13 ---
    {"title":"Terror of the Zygons","folder":"Doctor Who - S13E01 (080) - Terror of the Zygons - Parts 1-4","episode_source":"serial","episodes":[(13,1,"Terror of the Zygons Part One",False),(13,2,"Terror of the Zygons Part Two",False),(13,3,"Terror of the Zygons Part Three",False),(13,4,"Terror of the Zygons Part Four",False)],"se_entries":[]},
    {"title":"Planet of Evil","folder":"Doctor Who - S13E02 (081) - Planet of Evil - Parts 1-4","episode_source":"serial","episodes":[(13,5,"Planet of Evil Part One",False),(13,6,"Planet of Evil Part Two",False),(13,7,"Planet of Evil Part Three",False),(13,8,"Planet of Evil Part Four",False)],"se_entries":[]},
    {"title":"Pyramids of Mars","folder":"Doctor Who - S13E03 (082) - Pyramids of Mars - Parts 1-4","episode_source":"serial","episodes":[(13,9,"Pyramids of Mars Part One",False),(13,10,"Pyramids of Mars Part Two",False),(13,11,"Pyramids of Mars Part Three",False),(13,12,"Pyramids of Mars Part Four",False)],"se_entries":[]},
    {"title":"The Android Invasion","folder":"Doctor Who - S13E04 (083) - The Android Invasion - Parts 1-4","episode_source":"serial","episodes":[(13,13,"The Android Invasion Part One",False),(13,14,"The Android Invasion Part Two",False),(13,15,"The Android Invasion Part Three",False),(13,16,"The Android Invasion Part Four",False)],"se_entries":[]},
    {"title":"The Brain of Morbius","folder":"Doctor Who - S13E05 (084) - The Brain of Morbius - Parts 1-4","episode_source":"serial","episodes":[(13,17,"The Brain of Morbius Part One",False),(13,18,"The Brain of Morbius Part Two",False),(13,19,"The Brain of Morbius Part Three",False),(13,20,"The Brain of Morbius Part Four",False)],"se_entries":[]},
    {"title":"The Seeds of Doom","folder":"Doctor Who - S13E06 (085) - The Seeds of Doom - Parts 1-6","episode_source":"serial","episodes":[(13,21,"The Seeds of Doom Part One",False),(13,22,"The Seeds of Doom Part Two",False),(13,23,"The Seeds of Doom Part Three",False),(13,24,"The Seeds of Doom Part Four",False),(13,25,"The Seeds of Doom Part Five",False),(13,26,"The Seeds of Doom Part Six",False)],"se_entries":[]},
    # --- SEASON 14 ---
    {"title":"The Masque of Mandragora","folder":"Doctor Who - S14E01 (086) - The Masque of Mandragora - Parts 1-4","episode_source":"serial","episodes":[(14,1,"The Masque of Mandragora Part One",False),(14,2,"The Masque of Mandragora Part Two",False),(14,3,"The Masque of Mandragora Part Three",False),(14,4,"The Masque of Mandragora Part Four",False)],"se_entries":[]},
    {"title":"The Hand of Fear","folder":"Doctor Who - S14E02 (087) - The Hand of Fear - Parts 1-4","episode_source":"serial","episodes":[(14,5,"The Hand of Fear Part One",False),(14,6,"The Hand of Fear Part Two",False),(14,7,"The Hand of Fear Part Three",False),(14,8,"The Hand of Fear Part Four",False)],"se_entries":[]},
    {"title":"The Deadly Assassin","folder":"Doctor Who - S14E03 (088) - The Deadly Assassin - Parts 1-4","episode_source":"serial","episodes":[(14,9,"The Deadly Assassin Part One",False),(14,10,"The Deadly Assassin Part Two",False),(14,11,"The Deadly Assassin Part Three",False),(14,12,"The Deadly Assassin Part Four",False)],"se_entries":[]},
    {"title":"The Face of Evil","folder":"Doctor Who - S14E04 (089) - The Face of Evil - Parts 1-4","episode_source":"serial","episodes":[(14,13,"The Face of Evil Part One",False),(14,14,"The Face of Evil Part Two",False),(14,15,"The Face of Evil Part Three",False),(14,16,"The Face of Evil Part Four",False)],"se_entries":[]},
    {"title":"The Robots of Death","folder":"Doctor Who - S14E05 (090) - The Robots of Death - Parts 1-4","episode_source":"serial","episodes":[(14,17,"The Robots of Death Part One",False),(14,18,"The Robots of Death Part Two",False),(14,19,"The Robots of Death Part Three",False),(14,20,"The Robots of Death Part Four",False)],"se_entries":[]},
    {"title":"The Talons of Weng-Chiang","folder":"Doctor Who - S14E06 (091) - The Talons of Weng-Chiang - Parts 1-6","episode_source":"serial","episodes":[(14,21,"The Talons of Weng-Chiang Part One",False),(14,22,"The Talons of Weng-Chiang Part Two",False),(14,23,"The Talons of Weng-Chiang Part Three",False),(14,24,"The Talons of Weng-Chiang Part Four",False),(14,25,"The Talons of Weng-Chiang Part Five",False),(14,26,"The Talons of Weng-Chiang Part Six",False)],"se_entries":[]},
    # --- SEASON 15 ---
    {"title":"Horror of Fang Rock","folder":"Doctor Who - S15E01 (092) - Horror of Fang Rock - Parts 1-4","episode_source":"serial","episodes":[(15,1,"Horror of Fang Rock Part One",False),(15,2,"Horror of Fang Rock Part Two",False),(15,3,"Horror of Fang Rock Part Three",False),(15,4,"Horror of Fang Rock Part Four",False)],"se_entries":[]},
    {"title":"The Invisible Enemy","folder":"Doctor Who - S15E02 (093) - The Invisible Enemy - Parts 1-4","episode_source":"serial","episodes":[(15,5,"The Invisible Enemy Part One",False),(15,6,"The Invisible Enemy Part Two",False),(15,7,"The Invisible Enemy Part Three",False),(15,8,"The Invisible Enemy Part Four",False)],"se_entries":[]},
    {"title":"Image of the Fendahl","folder":"Doctor Who - S15E03 (094) - Image of the Fendahl - Parts 1-4","episode_source":"serial","episodes":[(15,9,"Image of the Fendahl Part One",False),(15,10,"Image of the Fendahl Part Two",False),(15,11,"Image of the Fendahl Part Three",False),(15,12,"Image of the Fendahl Part Four",False)],"se_entries":[]},
    {"title":"The Sun Makers","folder":"Doctor Who - S15E04 (095) - The Sun Makers - Parts 1-4","episode_source":"serial","episodes":[(15,13,"The Sun Makers Part One",False),(15,14,"The Sun Makers Part Two",False),(15,15,"The Sun Makers Part Three",False),(15,16,"The Sun Makers Part Four",False)],"se_entries":[]},
    {"title":"Underworld","folder":"Doctor Who - S15E05 (096) - Underworld - Parts 1-4","episode_source":"serial","episodes":[(15,17,"Underworld Part One",False),(15,18,"Underworld Part Two",False),(15,19,"Underworld Part Three",False),(15,20,"Underworld Part Four",False)],"se_entries":[]},
    {"title":"The Invasion of Time","folder":"Doctor Who - S15E06 (097) - The Invasion of Time - Parts 1-6","episode_source":"serial","episodes":[(15,21,"The Invasion of Time Part One",False),(15,22,"The Invasion of Time Part Two",False),(15,23,"The Invasion of Time Part Three",False),(15,24,"The Invasion of Time Part Four",False),(15,25,"The Invasion of Time Part Five",False),(15,26,"The Invasion of Time Part Six",False)],"se_entries":[]},
    # --- SEASON 16 (Key to Time) ---
    {"title":"The Ribos Operation","folder":"Doctor Who - S16E01 (098) - The Ribos Operation - Parts 1-4","episode_source":"serial","episodes":[(16,1,"The Ribos Operation Part One",False),(16,2,"The Ribos Operation Part Two",False),(16,3,"The Ribos Operation Part Three",False),(16,4,"The Ribos Operation Part Four",False)],"se_entries":[]},
    {"title":"The Pirate Planet","folder":"Doctor Who - S16E02 (099) - The Pirate Planet - Parts 1-4","episode_source":"serial","episodes":[(16,5,"The Pirate Planet Part One",False),(16,6,"The Pirate Planet Part Two",False),(16,7,"The Pirate Planet Part Three",False),(16,8,"The Pirate Planet Part Four",False)],"se_entries":[]},
    {"title":"The Stones of Blood","folder":"Doctor Who - S16E03 (100) - The Stones of Blood - Parts 1-4","episode_source":"serial","episodes":[(16,9,"The Stones of Blood Part One",False),(16,10,"The Stones of Blood Part Two",False),(16,11,"The Stones of Blood Part Three",False),(16,12,"The Stones of Blood Part Four",False)],"se_entries":[]},
    {"title":"The Androids of Tara","folder":"Doctor Who - S16E04 (101) - The Androids of Tara - Parts 1-4","episode_source":"serial","episodes":[(16,13,"The Androids of Tara Part One",False),(16,14,"The Androids of Tara Part Two",False),(16,15,"The Androids of Tara Part Three",False),(16,16,"The Androids of Tara Part Four",False)],"se_entries":[]},
    {"title":"The Power of Kroll","folder":"Doctor Who - S16E05 (102) - The Power of Kroll - Parts 1-4","episode_source":"serial","episodes":[(16,17,"The Power of Kroll Part One",False),(16,18,"The Power of Kroll Part Two",False),(16,19,"The Power of Kroll Part Three",False),(16,20,"The Power of Kroll Part Four",False)],"se_entries":[]},
    {"title":"The Armageddon Factor","folder":"Doctor Who - S16E06 (103) - The Armageddon Factor - Parts 1-6","episode_source":"serial","episodes":[(16,21,"The Armageddon Factor Part One",False),(16,22,"The Armageddon Factor Part Two",False),(16,23,"The Armageddon Factor Part Three",False),(16,24,"The Armageddon Factor Part Four",False),(16,25,"The Armageddon Factor Part Five",False),(16,26,"The Armageddon Factor Part Six",False)],"se_entries":[]},
    # --- SEASON 17 ---
    {"title":"Destiny of the Daleks","folder":"Doctor Who - S17E01 (104) - Destiny of the Daleks - Parts 1-4","episode_source":"serial","episodes":[(17,1,"Destiny of the Daleks Part One",False),(17,2,"Destiny of the Daleks Part Two",False),(17,3,"Destiny of the Daleks Part Three",False),(17,4,"Destiny of the Daleks Part Four",False)],"se_entries":[]},
    {"title":"City of Death","folder":"Doctor Who - S17E02 (105) - City of Death - Parts 1-4","episode_source":"serial","episodes":[(17,5,"City of Death Part One",False),(17,6,"City of Death Part Two",False),(17,7,"City of Death Part Three",False),(17,8,"City of Death Part Four",False)],"se_entries":[]},
    {"title":"The Creature from the Pit","folder":"Doctor Who - S17E03 (106) - The Creature from the Pit - Parts 1-4","episode_source":"serial","episodes":[(17,9,"The Creature from the Pit Part One",False),(17,10,"The Creature from the Pit Part Two",False),(17,11,"The Creature from the Pit Part Three",False),(17,12,"The Creature from the Pit Part Four",False)],"se_entries":[]},
    {"title":"Nightmare of Eden","folder":"Doctor Who - S17E04 (107) - Nightmare of Eden - Parts 1-4","episode_source":"serial","episodes":[(17,13,"Nightmare of Eden Part One",False),(17,14,"Nightmare of Eden Part Two",False),(17,15,"Nightmare of Eden Part Three",False),(17,16,"Nightmare of Eden Part Four",False)],"se_entries":[]},
    {"title":"The Horns of Nimon","folder":"Doctor Who - S17E05 (108) - The Horns of Nimon - Parts 1-4","episode_source":"serial","episodes":[(17,17,"The Horns of Nimon Part One",False),(17,18,"The Horns of Nimon Part Two",False),(17,19,"The Horns of Nimon Part Three",False),(17,20,"The Horns of Nimon Part Four",False)],"se_entries":[]},
    # --- SEASON 18 ---
    {"title":"The Leisure Hive","folder":"Doctor Who - S18E01 (109) - The Leisure Hive - Parts 1-4","episode_source":"serial","episodes":[(18,1,"The Leisure Hive Part One",False),(18,2,"The Leisure Hive Part Two",False),(18,3,"The Leisure Hive Part Three",False),(18,4,"The Leisure Hive Part Four",False)],"se_entries":[]},
    {"title":"Meglos","folder":"Doctor Who - S18E02 (110) - Meglos - Parts 1-4","episode_source":"serial","episodes":[(18,5,"Meglos Part One",False),(18,6,"Meglos Part Two",False),(18,7,"Meglos Part Three",False),(18,8,"Meglos Part Four",False)],"se_entries":[]},
    {"title":"Full Circle","folder":"Doctor Who - S18E03 (111) - Full Circle - Parts 1-4 (E-Space Trilogy 1)","episode_source":"serial","episodes":[(18,9,"Full Circle Part One",False),(18,10,"Full Circle Part Two",False),(18,11,"Full Circle Part Three",False),(18,12,"Full Circle Part Four",False)],"se_entries":[]},
    {"title":"State of Decay","folder":"Doctor Who - S18E04 (112) - State of Decay - Parts 1-4 (E-Space Trilogy 2)","episode_source":"serial","episodes":[(18,13,"State of Decay Part One",False),(18,14,"State of Decay Part Two",False),(18,15,"State of Decay Part Three",False),(18,16,"State of Decay Part Four",False)],"se_entries":[]},
    {"title":"Warriors' Gate","folder":"Doctor Who - S18E05 (113) - Warriors’ Gate - Parts 1-4 (E-Space Trilogy 3)","episode_source":"serial","episodes":[(18,17,"Warriors' Gate Part One",False),(18,18,"Warriors' Gate Part Two",False),(18,19,"Warriors' Gate Part Three",False),(18,20,"Warriors' Gate Part Four",False)],"se_entries":[]},
    {"title":"The Keeper of Traken","folder":"Doctor Who - S18E06 (114) - The Keeper of Traken - Parts 1-4","episode_source":"serial","episodes":[(18,21,"The Keeper of Traken Part One",False),(18,22,"The Keeper of Traken Part Two",False),(18,23,"The Keeper of Traken Part Three",False),(18,24,"The Keeper of Traken Part Four",False)],"se_entries":[]},
    {"title":"Logopolis","folder":"Doctor Who - S18E07 (115) - Logopolis - Parts 1-4","episode_source":"serial","episodes":[(18,25,"Logopolis Part One",False),(18,26,"Logopolis Part Two",False),(18,27,"Logopolis Part Three",False),(18,28,"Logopolis Part Four",False)],"se_entries":[]},
    # --- SEASON 19 ---
    {"title":"Castrovalva","folder":"Doctor Who - S19E01 (116) - Castrovalva - Parts 1-4","episode_source":"serial","episodes":[(19,1,"Castrovalva Part One",False),(19,2,"Castrovalva Part Two",False),(19,3,"Castrovalva Part Three",False),(19,4,"Castrovalva Part Four",False)],"se_entries":[]},
    {"title":"Four to Doomsday","folder":"Doctor Who - S19E02 (117) - Four to Doomsday - Parts 1-4","episode_source":"serial","episodes":[(19,5,"Four to Doomsday Part One",False),(19,6,"Four to Doomsday Part Two",False),(19,7,"Four to Doomsday Part Three",False),(19,8,"Four to Doomsday Part Four",False)],"se_entries":[]},
    {"title":"Kinda","folder":"Doctor Who - S19E03 (118) - Kinda - Parts 1-4","episode_source":"serial","episodes":[(19,9,"Kinda Part One",False),(19,10,"Kinda Part Two",False),(19,11,"Kinda Part Three",False),(19,12,"Kinda Part Four",False)],"se_entries":[]},
    {"title":"The Visitation","folder":"Doctor Who - S19E04 (119) - The Visitation - Parts 1-4","episode_source":"serial","episodes":[(19,13,"The Visitation Part One",False),(19,14,"The Visitation Part Two",False),(19,15,"The Visitation Part Three",False),(19,16,"The Visitation Part Four",False)],"se_entries":[]},
    {"title":"Black Orchid","folder":"Doctor Who - S19E05 (120) - Black Orchid - Parts 1-2","episode_source":"serial","episodes":[(19,17,"Black Orchid Part One",False),(19,18,"Black Orchid Part Two",False)],"se_entries":[]},
    {"title":"Earthshock","folder":"Doctor Who - S19E06 (121) - Earthshock - Parts 1-4","episode_source":"serial","episodes":[(19,19,"Earthshock Part One",False),(19,20,"Earthshock Part Two",False),(19,21,"Earthshock Part Three",False),(19,22,"Earthshock Part Four",False)],"se_entries":[]},
    {"title":"Time-Flight","folder":"Doctor Who - S19E07 (122) - Time-Flight - Parts 1-4","episode_source":"serial","episodes":[(19,23,"Time-Flight Part One",False),(19,24,"Time-Flight Part Two",False),(19,25,"Time-Flight Part Three",False),(19,26,"Time-Flight Part Four",False)],"se_entries":[]},
    # --- SEASON 20 ---
    {"title":"Arc of Infinity","folder":"Doctor Who - S20E01 (123) - Arc of Infinity - Parts 1-4","episode_source":"serial","episodes":[(20,1,"Arc of Infinity Part One",False),(20,2,"Arc of Infinity Part Two",False),(20,3,"Arc of Infinity Part Three",False),(20,4,"Arc of Infinity Part Four",False)],"se_entries":[]},
    {"title":"Snakedance","folder":"Doctor Who - S20E02 (124) - Snakedance - Parts 1-4","episode_source":"serial","episodes":[(20,5,"Snakedance Part One",False),(20,6,"Snakedance Part Two",False),(20,7,"Snakedance Part Three",False),(20,8,"Snakedance Part Four",False)],"se_entries":[]},
    {"title":"Mawdryn Undead","folder":"Doctor Who - S20E03 (125) - Mawdryn Undead - Parts 1-4 (The Guardian Trilogy 1)","episode_source":"serial","episodes":[(20,9,"Mawdryn Undead Part One",False),(20,10,"Mawdryn Undead Part Two",False),(20,11,"Mawdryn Undead Part Three",False),(20,12,"Mawdryn Undead Part Four",False)],"se_entries":[]},
    {"title":"Terminus","folder":"Doctor Who - S20E04 (126) - Terminus - Parts 1-4 (The Guardian Trilogy 2)","episode_source":"serial","episodes":[(20,13,"Terminus Part One",False),(20,14,"Terminus Part Two",False),(20,15,"Terminus Part Three",False),(20,16,"Terminus Part Four",False)],"se_entries":[]},
    {"title":"Enlightenment","folder":"Doctor Who - S20E05 (127) - Enlightenment - Parts 1-4 (The Guardian Trilogy 3)","episode_source":"serial","episodes":[(20,17,"Enlightenment Part One",False),(20,18,"Enlightenment Part Two",False),(20,19,"Enlightenment Part Three",False),(20,20,"Enlightenment Part Four",False),(20,24,"Enlightenment (Special Edition)",False)],"se_entries":[{"folder":"Doctor Who - S20E05 (127) - Enlightenment - Parts 1-4 (The Guardian Trilogy 3) (Special Edition)","episodes":[(20,24,"Enlightenment (Special Edition)",False)],"include_extras":False}]},
    {"title":"The King's Demons","folder":"Doctor Who - S20E06 (128) - The King’s Demons - Parts 1-2","episode_source":"serial","episodes":[(20,21,"The King's Demons Part One",False),(20,22,"The King's Demons Part Two",False)],"se_entries":[]},
    {"title":"The Five Doctors","folder":"Doctor Who - S20E07 (129) - The Five Doctors - Parts 1-1 (Transmission Version)","episode_source":"serial","episodes":[(20,23,"The Five Doctors",False),(20,25,"The Five Doctors (Special Edition)",False)],"se_entries":[{"folder":"Doctor Who - S20E07 (129) - The Five Doctors - Parts 1-1 (Special Edition+Extras)","episodes":[(20,25,"The Five Doctors (Special Edition)",False)],"include_extras":True}]},
    # --- SEASON 21 ---
    {"title":"Warriors of the Deep","folder":"Doctor Who - S21E01 (130) - Warriors of the Deep - Parts 1-4","episode_source":"serial","episodes":[(21,1,"Warriors of the Deep Part One",False),(21,2,"Warriors of the Deep Part Two",False),(21,3,"Warriors of the Deep Part Three",False),(21,4,"Warriors of the Deep Part Four",False)],"se_entries":[]},
    {"title":"The Awakening","folder":"Doctor Who - S21E02 (131) - The Awakening - Parts 1-2","episode_source":"serial","episodes":[(21,5,"The Awakening Part One",False),(21,6,"The Awakening Part Two",False)],"se_entries":[]},
    {"title":"Frontios","folder":"Doctor Who - S21E03 (132) - Frontios - Parts 1-4","episode_source":"serial","episodes":[(21,7,"Frontios Part One",False),(21,8,"Frontios Part Two",False),(21,9,"Frontios Part Three",False),(21,10,"Frontios Part Four",False)],"se_entries":[]},
    {"title":"Resurrection of the Daleks","folder":"Doctor Who - S21E04 (133) - Resurrection of the Daleks - Parts 1-4","episode_source":"serial","episodes":[(21,11,"Resurrection of the Daleks Part One",False),(21,12,"Resurrection of the Daleks Part Two",False),(21,13,"Resurrection of the Daleks Part Three",False),(21,14,"Resurrection of the Daleks Part Four",False)],"se_entries":[]},
    {"title":"Planet of Fire","folder":"Doctor Who - S21E05 (134) - Planet of Fire - Parts 1-4","episode_source":"serial","episodes":[(21,15,"Planet of Fire Part One",False),(21,16,"Planet of Fire Part Two",False),(21,17,"Planet of Fire Part Three",False),(21,18,"Planet of Fire Part Four",False)],"se_entries":[]},
    {"title":"The Caves of Androzani","folder":"Doctor Who - S21E06 (135) - Caves of Androzani - Parts 1-4","episode_source":"serial","episodes":[(21,19,"The Caves of Androzani Part One",False),(21,20,"The Caves of Androzani Part Two",False),(21,21,"The Caves of Androzani Part Three",False),(21,22,"The Caves of Androzani Part Four",False)],"se_entries":[]},
    {"title":"The Twin Dilemma","folder":"Doctor Who - S21E07 (136) - The Twin Dilemma - Parts 1-4","episode_source":"serial","episodes":[(21,23,"The Twin Dilemma Part One",False),(21,24,"The Twin Dilemma Part Two",False),(21,25,"The Twin Dilemma Part Three",False),(21,26,"The Twin Dilemma Part Four",False)],"se_entries":[]},
    # --- SEASON 22 (45-minute format) ---
    {"title":"Attack of the Cybermen","folder":"Doctor Who - S22E01 (137) - Attack of the Cybermen - Parts 1-2","episode_source":"serial","episodes":[(22,1,"Attack of the Cybermen Part One",False),(22,2,"Attack of the Cybermen Part Two",False)],"se_entries":[]},
    {"title":"Vengeance on Varos","folder":"Doctor Who - S22E02 (138) - Vengeance on Varos - Parts 1-2","episode_source":"serial","episodes":[(22,3,"Vengeance on Varos Part One",False),(22,4,"Vengeance on Varos Part Two",False)],"se_entries":[]},
    {"title":"The Mark of the Rani","folder":"Doctor Who - S22E03 (139) - The Mark of the Rani - Parts 1-2","episode_source":"serial","episodes":[(22,5,"The Mark of the Rani Part One",False),(22,6,"The Mark of the Rani Part Two",False)],"se_entries":[]},
    {"title":"The Two Doctors","folder":"Doctor Who - S22E04 (140) - The Two Doctors - Parts 1-3","episode_source":"serial","episodes":[(22,7,"The Two Doctors Part One",False),(22,8,"The Two Doctors Part Two",False),(22,9,"The Two Doctors Part Three",False)],"se_entries":[]},
    {"title":"Timelash","folder":"Doctor Who - S22E05 (141) - Timelash - Parts 1-2","episode_source":"serial","episodes":[(22,10,"Timelash Part One",False),(22,11,"Timelash Part Two",False)],"se_entries":[]},
    {"title":"Revelation of the Daleks","folder":"Doctor Who - S22E06 (142) - Revelation of the Daleks - Parts 1-2","episode_source":"serial","episodes":[(22,12,"Revelation of the Daleks Part One",False),(22,13,"Revelation of the Daleks Part Two",False)],"se_entries":[]},
    # --- SEASON 23 (Trial of a Time Lord — all 14 parts in one folder) ---
    {"title":"The Trial of a Time Lord","folder":"Doctor Who - S23E01 (143) - The Trial of a Time Lord - Parts 1-14 - Segment 1-4","episode_source":"serial","episodes":[(23,1,"The Mysterious Planet Part One",False),(23,2,"The Mysterious Planet Part Two",False),(23,3,"The Mysterious Planet Part Three",False),(23,4,"The Mysterious Planet Part Four",False),(23,5,"Mindwarp Part One",False),(23,6,"Mindwarp Part Two",False),(23,7,"Mindwarp Part Three",False),(23,8,"Mindwarp Part Four",False),(23,9,"Terror of the Vervoids Part One",False),(23,10,"Terror of the Vervoids Part Two",False),(23,11,"Terror of the Vervoids Part Three",False),(23,12,"Terror of the Vervoids Part Four",False),(23,13,"The Ultimate Foe Part One",False),(23,14,"The Ultimate Foe Part Two",False)],"se_entries":[]},
    # --- SEASON 24 ---
    {"title":"Time and the Rani","folder":"Doctor Who - S24E01 (144) - Time and the Rani - Parts 1-4","episode_source":"serial","episodes":[(24,1,"Time and the Rani Part One",False),(24,2,"Time and the Rani Part Two",False),(24,3,"Time and the Rani Part Three",False),(24,4,"Time and the Rani Part Four",False)],"se_entries":[]},
    {"title":"Paradise Towers","folder":"Doctor Who - S24E02 (145) - Paradise Towers - Parts 1-4","episode_source":"serial","episodes":[(24,5,"Paradise Towers Part One",False),(24,6,"Paradise Towers Part Two",False),(24,7,"Paradise Towers Part Three",False),(24,8,"Paradise Towers Part Four",False)],"se_entries":[]},
    {"title":"Delta and the Bannermen","folder":"Doctor Who - S24E03 (146) - Delta and the Bannermen - Parts 1-3","episode_source":"serial","episodes":[(24,9,"Delta and the Bannermen Part One",False),(24,10,"Delta and the Bannermen Part Two",False),(24,11,"Delta and the Bannermen Part Three",False)],"se_entries":[]},
    {"title":"Dragonfire","folder":"Doctor Who - S24E04 (147) - Dragonfire - Parts 1-3","episode_source":"serial","episodes":[(24,12,"Dragonfire Part One",False),(24,13,"Dragonfire Part Two",False),(24,14,"Dragonfire Part Three",False)],"se_entries":[]},
    # --- SEASON 25 ---
    {"title":"Remembrance of the Daleks","folder":"Doctor Who - S25E01 (148) - Remembrance of the Daleks - Parts 1-4","episode_source":"serial","episodes":[(25,1,"Remembrance of the Daleks Part One",False),(25,2,"Remembrance of the Daleks Part Two",False),(25,3,"Remembrance of the Daleks Part Three",False),(25,4,"Remembrance of the Daleks Part Four",False)],"se_entries":[]},
    {"title":"The Happiness Patrol","folder":"Doctor Who - S25E02 (149) - The Happiness Patrol - Parts 1-3","episode_source":"serial","episodes":[(25,5,"The Happiness Patrol Part One",False),(25,6,"The Happiness Patrol Part Two",False),(25,7,"The Happiness Patrol Part Three",False)],"se_entries":[]},
    {"title":"Silver Nemesis","folder":"Doctor Who - S25E03 (150) - Silver Nemesis - Parts 1-3","episode_source":"serial","episodes":[(25,8,"Silver Nemesis Part One",False),(25,9,"Silver Nemesis Part Two",False),(25,10,"Silver Nemesis Part Three",False)],"se_entries":[]},
    {"title":"The Greatest Show in the Galaxy","folder":"Doctor Who - S25E04 (151) - The Greatest Show in the Galaxy - Parts 1-4","episode_source":"serial","episodes":[(25,11,"The Greatest Show in the Galaxy Part One",False),(25,12,"The Greatest Show in the Galaxy Part Two",False),(25,13,"The Greatest Show in the Galaxy Part Three",False),(25,14,"The Greatest Show in the Galaxy Part Four",False)],"se_entries":[]},
    # --- SEASON 26 ---
    {"title":"Battlefield","folder":"Doctor Who - S26E01 (152) - Battlefield - Parts 1-4","episode_source":"serial","episodes":[(26,1,"Battlefield Part One",False),(26,2,"Battlefield Part Two",False),(26,3,"Battlefield Part Three",False),(26,4,"Battlefield Part Four",False)],"se_entries":[]},
    {"title":"Ghost Light","folder":"Doctor Who - S26E02 (153) - Ghost Light - Parts 1-4","episode_source":"serial","episodes":[(26,5,"Ghost Light Part One",False),(26,6,"Ghost Light Part Two",False),(26,7,"Ghost Light Part Three",False)],"se_entries":[]},
    {"title":"The Curse of Fenric","folder":"Doctor Who - S26E03 (154) - The Curse of Fenric - Parts 1-4","episode_source":"serial","episodes":[(26,8,"The Curse of Fenric Part One",False),(26,9,"The Curse of Fenric Part Two",False),(26,10,"The Curse of Fenric Part Three",False),(26,11,"The Curse of Fenric Part Four",False)],"se_entries":[]},
    {"title":"Survival","folder":"Doctor Who - S26E04 (155) - Survival - Parts 1-3","episode_source":"serial","episodes":[(26,12,"Survival Part One",False),(26,13,"Survival Part Two",False),(26,14,"Survival Part Three",False)],"se_entries":[]},
]


def _ep_dest(season: int, ep: int, title: str, recon: bool) -> Path:
    suffix = " (Recon)" if recon else ""
    fname = f"Doctor Who (1963) - S{season:02d}E{ep:02d} - {title}{suffix}.avi"
    return SHOW_DEST / f"Season {season:02d}" / fname


def _extras_dest(season: int, filename: str) -> Path:
    return SHOW_DEST / f"Season {season:02d}" / "extras" / filename


def _find_serial_eps(folder: Path) -> list:
    files = sorted([
        f for f in folder.iterdir()
        if f.suffix == ".avi"
        and "Bonus" not in f.name
        and "Special Edition" not in f.name
        and not re.search(r"\(0\)", f.name)
    ])
    return files


def _find_extras(folder: Path) -> list:
    result = []
    for f in folder.iterdir():
        if f.suffix == ".pdf":
            result.append(f)
        elif f.suffix == ".avi" and (
            "Bonus" in f.name or re.search(r"\(0\)", f.name)
        ):
            result.append(f)
    return result


def _find_season1_flat(ep_num: int) -> Path | None:
    for f in SEASON1_FLAT.iterdir():
        if f.suffix != ".avi":
            continue
        for pat in [f"S01E{ep_num:02d}", f"S01E0{ep_num:02d}"]:
            if pat in f.name:
                return f
    return None


def build_plan(serials: list, specials: list) -> list:
    moves = []

    for entry in specials:
        moves.extend(_plan_special(entry))

    for entry in serials:
        moves.extend(_plan_serial(entry))

    return moves


def _plan_special(entry: dict) -> list:
    moves = []
    if entry["episode_source"] == "loose":
        src = COLLECTION / entry["folder"]
        s, e, title, recon = entry["episodes"][0]
        moves.append((src, _ep_dest(s, e, title, recon)))
    elif entry["episode_source"] == "serial":
        folder = COLLECTION / entry["folder"]
        eps = _find_serial_eps(folder)
        for i, (s, e, title, recon) in enumerate(entry["episodes"]):
            if i < len(eps):
                moves.append((eps[i], _ep_dest(s, e, title, recon)))
            else:
                logging.warning(f"WARN missing part {i+1} for {entry['title']}")
    return moves


def _plan_serial(entry: dict) -> list:
    moves = []
    folder = COLLECTION / entry["folder"] if entry["folder"] else None
    season = entry["episodes"][0][0] if entry["episodes"] else 0

    if entry["episode_source"] == "serial" and folder:
        eps = _find_serial_eps(folder)
        for i, (s, e, title, recon) in enumerate(entry["episodes"]):
            if i < len(eps):
                moves.append((eps[i], _ep_dest(s, e, title, recon)))
            else:
                logging.warning(f"WARN missing part {i+1} for {entry['title']}")
        for f in eps[len(entry["episodes"]):]:
            moves.append((f, _extras_dest(season, f.name)))
        for f in _find_extras(folder):
            moves.append((f, _extras_dest(season, f.name)))

    elif entry["episode_source"] == "season1_flat":
        for (s, e, title, recon) in entry["episodes"]:
            src = _find_season1_flat(e)
            if src:
                moves.append((src, _ep_dest(s, e, title, recon)))
            else:
                logging.warning(f"WARN S01E{e:02d} not found in flat folder")
        if folder and folder.exists():
            for f in _find_extras(folder):
                moves.append((f, _extras_dest(season, f.name)))
            for f in _find_serial_eps(folder):
                moves.append((f, _extras_dest(season, f.name)))

    elif entry["episode_source"] == "tv_movie":
        avs = [f for f in TV_MOVIE_DIR.iterdir() if f.suffix == ".avi"]
        if avs:
            _, _, title, _ = entry["episodes"][0]
            dest = MOVIE_DEST / title / f"{title}.avi"
            moves.append((avs[0], dest))

    for se in entry.get("se_entries", []):
        se_folder = COLLECTION / se["folder"]
        if not se_folder.exists():
            logging.warning(f"WARN SE folder not found: {se['folder']}")
            continue
        eps = _find_serial_eps(se_folder)
        for i, (s, e, title, recon) in enumerate(se["episodes"]):
            if i < len(eps):
                moves.append((eps[i], _ep_dest(s, e, title, recon)))
        if se.get("include_extras"):
            for f in _find_extras(se_folder):
                moves.append((f, _extras_dest(se["episodes"][0][0], f.name)))

    return moves


def execute_plan(moves: list, dry_run: bool = True) -> tuple:
    moved = skipped = errors = 0
    for src, dest in moves:
        if not src.exists():
            logging.warning(f"WARN  source missing: {src}")
            errors += 1
            continue
        if dest.exists():
            logging.info(f"SKIP  {dest.name}")
            skipped += 1
            continue
        if dry_run:
            logging.info(f"DRY   {src.name}\n   -> {dest}")
            moved += 1
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                os.rename(src, dest)
            except OSError:
                shutil.move(str(src), str(dest))
            logging.info(f"MOVE  {src.name}\n   -> {dest}")
            moved += 1
    return moved, skipped, errors


def main():
    parser = argparse.ArgumentParser(description="Reorganize Classic Doctor Who for Plex")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("organize_classic_who.log"),
        ],
    )

    moves = build_plan(SERIALS, SPECIALS)
    logging.info(f"\nPlan: {len(moves)} file operations")
    moved, skipped, errors = execute_plan(moves, dry_run=not args.execute)
    logging.info(f"\nSummary: moved={moved}  skipped={skipped}  errors={errors}")


if __name__ == "__main__":
    main()
