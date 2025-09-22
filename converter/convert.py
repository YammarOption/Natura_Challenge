import os
import json
import re

pokemon_dict = [
    ("BULBASAUR", "BULBOHSAUR"),
    ("IVYSAUR", "GEMMAHSAUR"),
    ("VENUSAUR", "MERAVISAUR"),
    ("CHARMANDER", "TORCERTOLO"),
    ("CHARMELEON", "ARSAMANDRA"),
    ("CHARIZARD", "TORRIDRAGO"),
    ("SQUIRTLE", "TARTASPRUZ"),
    ("WARTORTLE", "TARTACIUFF"),
    ("BLASTOISE", "ESPLUGGINE"),
    ("CATERPIE", "BACHETTO"),
    ("METAPOD", "BOZZOLUNA"),
    ("BUTTERFREE", "LIBRAPTERA"),
    ("WEEDLE", "TRIVERRME"),
    ("KAKUNA", "TRIVALLO"),
    ("BEEDRILL", "TRIVEZZPA"),
    ("PIDGEY", "PIZZIRILLO"),
    ("PIDGEOTTO", "PUNCCIONE"),
    ("PIDGEOT", "PIJJETTO"),
    ("RATTATA", "RATTATRACK"),
    ("RATICATE", "PATRATRATT"),
    ("SPEAROW", "BECCRUCCIO"),
    ("FEAROW", "BECCATORE"),
    ("EKANS", "OLIBISS"),
    ("ARBOK", "ORBULOC"),
    ("PIKACHU", "PIKACHU"),
    ("RAICHU", "RAICHU"),
    ("SANDSHREW", "SAMBIOLINO"),
    ("SANDSLASH", "PUNGOLINO"),
    ("NIDORANF", "AGONIGLIO F"),
    ("NIDORINA", "AGORINA"),
    ("NIDOQUEEN", "AGOREINA"),
    ("NIDORANM", "AGONIGLIO M"),
    ("NIDORINO", "AGORINO"),
    ("NIDOKING", "AGOREX"),
    ("CLEFAIRY", "LUNINFA"),
    ("CLEFABLE", "SELENINFA"),
    ("VULPIX", "VULPEX"),
    ("NINETALES", "NOVOLPENA"),
    ("JIGGLYPUFF", "ROTONDOLCE"),
    ("WIGGLYTUFF", "MORBIDOLCE"),
    ("ZUBAT", "PIPISTRIDO"),
    ("GOLBAT", "VESPERTO"),
    ("ODDISH", "MANDRAPA"),
    ("GLOOM", "TANFLORA"),
    ("VILEPLUME", "RAFFLETORE"),
    ("PARAS", "PARASSAY"),
    ("PARASECT", "PARASCORDY"),
    ("VENONAT", "VILMOSCO"),
    ("VENOMOTH", "VELENA"),
    ("DIGLETT", "SCAVETTUN"),
    ("DUGTRIO", "SCAVATRINO"),
    ("MEOWTH", "MEO"),
    ("PERSIAN", "SNOBILGATT"),
    ("PSYDUCK", "PSIKIQUACK"),
    ("GOLDUCK", "EMIQUAPPA"),
    ("MANKEY", "MACRACK"),
    ("PRIMEAPE", "SPAKKAKO"),
    ("GROWLITHE", "ARFIDO"),
    ("ARCANINE", "ARCANINO"),
    ("POLIWAG", "GIRONDO"),
    ("POLIWHIRL", "RIGIRINO"),
    ("POLIWRATH", "GIRACONDO"),
    ("ABRA", "SVANIA"),
    ("KADABRA", "APPARIA"),
    ("ALAKAZAM", "REAPPARIA"),
    ("MACHOP", "MACHIPITO"),
    ("MACHOKE", "CULTURISSA"),
    ("MACHAMP", "ERCAMPIONE"),
    ("BELLSPROUT", "CAMPAGNULA"),
    ("WEEPINBELL", "BAVORDONG"),
    ("VICTREEBEL", "GIUBILESCA"),
    ("TENTACOOL", "MEDUSER"),
    ("TENTACRUEL", "TENTAZER"),
    ("GEODUDE", "GEODEH"),
    ("GRAVELER", "GRANITOLO"),
    ("GOLEM", "GOLEMASSO"),
    ("PONYTA", "VAMPONY"),
    ("RAPIDASH", "BRUCEFALO"),
    ("SLOWPOKE", "SHONOLENTO"),
    ("SLOWBRO", "SHIMOLENTI"),
    ("MAGNEMITE", "MAGNEMITA"),
    ("MAGNETON", "CALAMITRIS"),
    ("FARFETCHD", "UNUMPORRO"),
    ("DODUO", "DODUO"),
    ("DODRIO", "TREMU'"),
    ("SEEL", "CALOTTARIA"),
    ("DEWGONG", "LAMANFRIGO"),
    ("GRIMER", "MELMOR"),
    ("MUK", "SBRAGOLMOR"),
    ("SHELLDER", "VONGLO"),
    ("CLOYSTER", "OSTRICO"),
    ("GASTLY", "GASPECTER"),
    ("HAUNTER", "SPECTERROR"),
    ("GENGAR", "SIMULUMBRA"),
    ("ONIX", "SERPETRUS"),
    ("DROWZEE", "TORPIRO"),
    ("HYPNO", "TORPENDOL"),
    ("KRABBY", "KELINO"),
    ("KINGLER", "GRANKELONE"),
    ("VOLTORB", "VOLTORBE"),
    ("ELECTRODE", "DEBOTTORBE"),
    ("EXEGGCUTE", "OVINCOLI"),
    ("EXEGGUTOR", "COCCONTROL"),
    ("CUBONE", "LUTTESCHIO"),
    ("MAROWAK", "OSSOSSINO"),
    ("HITMONLEE", "CALCIATEKA"),
    ("HITMONCHAN", "PUGNILE"),
    ("LICKITUNG", "LINGUANA"),
    ("KOFFING", "TOSSIKOFF"),
    ("WEEZING", "DUUMVIRALE"),
    ("RHYHORN", "ROCCERONTE"),
    ("RHYDON", "TRAFORONTE"),
    ("CHANSEY", "TAROTA"),
    ("TANGELA", "GROVILIANA"),
    ("KANGASKHAN", "INDOMATER"),
    ("HORSEA", "CAVALLINO"),
    ("SEADRA", "IDDRAGAMPO"),
    ("GOLDEEN", "PESCIPESSA"),
    ("SEAKING", "ROSSOVRANO"),
    ("STARYU", "RUBISTELLA"),
    ("STARMIE", "CRISTELLA"),
    ("MRMIME", "MAMIMIMA"),
    ("SCYTHER", "INSECATOR"),
    ("JYNX", "LABBRIVIDA"),
    ("ELECTABUZZ", "ROMBITON"),
    ("MAGMAR", "ARROSTRO"),
    ("PINSIR", "STRANGOLIA"),
    ("TAUROS", "TAUROS"),
    ("MAGIKARP", "KARPADIEM"),
    ("GYARADOS", "APOKALYPSO"),
    ("LAPRAS", "TRAGHESSIE"),
    ("DITTO", "IDEM"),
    ("EEVEE", "EVVU'"),
    ("VAPOREON", "AQUAEON"),
    ("JOLTEON", "FULGURAEON"),
    ("FLAREON", "FLAMMAEON"),
    ("PORYGON", "PORYGON"),
    ("OMANYTE", "AMMONAUTA"),
    ("OMASTAR", "AMMONITRO"),
    ("KABUTO", "ELMULO"),
    ("KABUTOPS", "LAMULORD"),
    ("AERODACTYL", "AERODACTYL"),
    ("SNORLAX", "PISOLAX"),
    ("ARTICUNO", "ARTICUNO"),
    ("ZAPDOS", "ZAPDOS"),
    ("MOLTRES", "CALIENTRES"),
    ("DRATINI", "DRAGHELLO"),
    ("DRAGONAIR", "DRAGAERE"),
    ("DRAGONITE", "DRAGONITE"),
    ("MEWTWO", "MEWTWO"),
    ("MEW", "MEW"),
    ("MISSINGNO", "MISSINGNO")
]

types_dict = {
    "NORMAL": "NORMALE",
    "FIGHTING": "LOTTA",
    "FLYING": "VOLANTE",
    "POISON": "VELENO",
    "GROUND": "TERRA",
    "ROCK": "ROCCIA",
    "BUG": "COLEOTT",
    "GHOST": "SPETTRO",
    "STEEL": "ACCIAIO",
    "FIRE": "FUOCO",
    "WATER": "ACQUA",
    "GRASS": "ERBA",
    "ELECTRIC": "ELETTRO",
    "PSYCHIC_TYPE": "PSICO",
    "ICE": "GHIACCIO",
    "DRAGON": "DRAGO",
    "BIRD": "UCCELLO"
}

moves = {
    "NO_MOVE": ("", "", 0, 0, 0, 0),
    "ACID": ("ACIDO", "VELENO", 30, 40, 100, 51),
    "SKY_ATTACK": ("AEROATTACCO", "VOLANTE", 5, 140, 90, 143),
    "SHARPEN": ("AFFILATORE", "NORMALE", 30, 0, 0, 159),
    "AGILITY": ("AGILITÀ", "PSICO", 30, 0, 0, 97),
    "AMNESIA": ("AMNESIA", "PSICO", 20, 0, 0, 133),
    "ABSORB": ("ASSORBIMENTO", "ERBA", 20, 20, 100, 71),
    "WING_ATTACK": ("ATT. D'ALA", "VOLANTE", 35, 35, 100, 17),
    "QUICK_ATTACK": ("ATT. RAPIDO", "NORMALE", 30, 40, 100, 98),
    "SELFDESTRUCT": ("AUTODISTRUZ.", "NORMALE", 5, 130, 100, 120),
    "WRAP": ("AVVOLGIBOTTA", "NORMALE", 20, 15, 85, 35),
    "TACKLE": ("AZIONE", "NORMALE", 35, 35, 95, 33),
    "BARRIER": ("BARRIERA", "PSICO", 30, 0, 0, 112),
    "PECK": ("BECCATA", "VOLANTE", 35, 35, 100, 64),
    "ROAR": ("BOATO", "NORMALE", 20, 0, 100, 46),
    "BUBBLE": ("BOLLA", "ACQUA", 30, 20, 100, 145),
    "BUBBLEBEAM": ("BOLLARAGGIO", "ACQUA", 20, 65, 100, 61),
    "BLIZZARD": ("BORA", "GHIACCIO", 5, 120, 90, 59),
    "POUND": ("BOTTA", "NORMALE", 35, 40, 100, 1),
    "HEADBUTT": ("BOTTINTESTA", "NORMALE", 15, 70, 100, 29),
    "EMBER": ("BRACIERE", "FUOCO", 25, 40, 100, 52),
    "HI_JUMP_KICK": ("CALCINVOLO", "LOTTA", 20, 85, 90, 136),
    "ROLLING_KICK": ("CALCIORULLO", "LOTTA", 15, 60, 85, 27),
    "JUMP_KICK": ("CALCIOSALTO", "LOTTA", 25, 70, 95, 26),
    "SING": ("CANTO", "NORMALE", 15, 0, 55, 47),
    "SKULL_BASH": ("CAPOCCIATA", "NORMALE", 15, 100, 100, 130),
    "WATERFALL": ("CASCATA", "ACQUA", 15, 80, 100, 127),
    "KINESIS": ("CINÉSI", "PSICO", 15, 0, 80, 134),
    "THRASH": ("COLPO", "NORMALE", 20, 90, 100, 37),
    "LOW_KICK": ("COLPO BASSO", "LOTTA", 20, 50, 90, 67),
    "TAIL_WHIP": ("COLPOCODA", "NORMALE", 30, 0, 100, 39),
    "KARATE_CHOP": ("COLPOKARATE", "NORMALE", 25, 50, 100, 2),
    "COMET_PUNCH": ("COMETAPUGNO", "NORMALE", 15, 18, 85, 4),
    "SWIFT": ("COMETE", "NORMALE", 20, 60, 0, 129),
    "CONFUSION": ("CONFUSIONE", "PSICO", 25, 50, 100, 93),
    "COUNTER": ("CONTRATTACCO", "LOTTA", 20, 0, 100, 68),
    "CONVERSION": ("CONVERSIONE", "NORMALE", 30, 0, 100, 160),
    "BODY_SLAM": ("CORPOSCONTRO", "NORMALE", 15, 85, 100, 34),
    "SOFTBOILED": ("COVAUOVA", "NORMALE", 10, 0, 0, 135),
    "GROWTH": ("CRESCITA", "NORMALE", 40, 0, 0, 74),
    "SWORDS_DANCE": ("DANZASPADA", "NORMALE", 30, 0, 0, 14),
    "LOVELY_KISS": ("DEMONBACIO", "NORMALE", 10, 0, 75, 142),
    "DOUBLESLAP": ("DOPPIASBERLA", "NORMALE", 10, 15, 85, 3),
    "TWINEEDLE": ("DOPPIO AGO", "COLEOTT", 20, 25, 100, 41),
    "DOUBLE_KICK": ("DOPPIOCALCIO", "LOTTA", 30, 30, 100, 24),
    "DOUBLE_TEAM": ("DOPPIOTEAM", "NORMALE", 15, 0, 0, 104),
    "EXPLOSION": ("ESPLOSIONE", "NORMALE", 5, 170, 100, 153),
    "SLUDGE": ("FANGO", "VELENO", 20, 65, 100, 124),
    "FLASH": ("FLASH", "NORMALE", 20, 0, 70, 148),
    "FOCUS_ENERGY": ("FOCALENERGIA", "NORMALE", 30, 0, 0, 116),
    "RAZOR_LEAF": ("FOGLIELAMA", "ERBA", 25, 55, 95, 75),
    "STRENGTH": ("FORZA", "NORMALE", 15, 80, 100, 70),
    "DIG": ("FOSSA", "TERRA", 10, 100, 100, 91),
    "ROCK_SLIDE": ("FRANA", "ROCCIA", 10, 75, 90, 157),
    "VINE_WHIP": ("FRUSTATA", "ERBA", 10, 35, 100, 22),
    "THUNDERBOLT": ("FULMINE", "ELETTRO", 15, 95, 100, 85),
    "LEER": ("FULMISGUARDO", "NORMALE", 30, 0, 100, 43),
    "FIRE_BLAST": ("FUOCOBOMBA", "FUOCO", 5, 120, 85, 126),
    "FIRE_PUNCH": ("FUOCOPUGNO", "FUOCO", 15, 75, 100, 7),
    "FURY_ATTACK": ("FURIA", "NORMALE", 20, 15, 85, 31),
    "ICE_PUNCH": ("GELOPUGNO", "GHIACCIO", 15, 75, 100, 8),
    "ICE_BEAM": ("GELORAGGIO", "GHIACCIO", 10, 95, 100, 58),
    "GUILLOTINE": ("GHIGLIOTTINA", "NORMALE", 5, 0, 30, 12),
    "PAY_DAY": ("GIORNOPAGA", "NORMALE", 20, 40, 100, 6),
    "SCRATCH": ("GRAFFIO", "NORMALE", 35, 40, 100, 10),
    "HYDRO_PUMP": ("IDROPOMPA", "ACQUA", 5, 120, 80, 56),
    "HORN_ATTACK": ("INCORNATA", "NORMALE", 25, 65, 100, 30),
    "DISABLE": ("INIBITORE", "NORMALE", 20, 0, 55, 50),
    "HYPER_BEAM": ("IPERRAGGIO", "NORMALE", 5, 150, 90, 63),
    "HYPER_FANG": ("IPERZANNA", "NORMALE", 15, 80, 90, 158),
    "HYPNOSIS": ("IPNOSI", "PSICO", 20, 0, 60, 95),
    "RAGE": ("IRA", "NORMALE", 20, 20, 100, 99),
    "DRAGON_RAGE": ("IRA DI DRAGO", "DRAGO", 10, 0, 100, 82),
    "SLASH": ("LACERAZIONE", "NORMALE", 20, 70, 100, 163),  # Not in list, set to 0
    "FLAMETHROWER": ("LANCIAFIAMME", "FUOCO", 15, 95, 100, 53),
    "LICK": ("LECCATA", "SPETTRO", 30, 20, 100, 122),
    "BIND": ("LEGATUTTO", "NORMALE", 20, 15, 85, 20),
    "CONSTRICT": ("LIMITAZIONE", "NORMALE", 35, 10, 100, 132),
    "DREAM_EATER": ("MANGIASOGNI", "PSICO", 15, 100, 100, 138),
    "CRABHAMMER": ("MARTELCHELA", "ACQUA", 10, 90, 85, 152),
    "MEDITATE": ("MEDITAZIONE", "PSICO", 40, 0, 0, 96),
    "GLARE": ("MEDUSGUARDO", "NORMALE", 30, 0, 75, 137),
    "MEGA_KICK": ("MEGACALCIO", "NORMALE", 5, 120, 75, 25),
    "MEGA_PUNCH": ("MEGAPUGNO", "NORMALE", 20, 80, 85, 5),
    "MEGA_DRAIN": ("MEGASSORBIM.", "ERBA", 10, 40, 100, 72),
    "METRONOME": ("METRONOMO", "NORMALE", 10, 0, 0, 118),
    "STRING_SHOT": ("MILLEBAVE", "COLEOTT", 40, 0, 95, 81),
    "MIMIC": ("MIMICA", "NORMALE", 10, 0, 0, 102),
    "MINIMIZE": ("MINIMIZZATO", "NORMALE", 20, 0, 0, 107),
    "PIN_MISSILE": ("MISSILSPILLO", "COLEOTT", 20, 14, 85, 42),
    "BITE": ("MORSO", "NORMALE", 25, 60, 100, 44),
    "SEISMIC_TOSS": ("MOV SISMICO", "LOTTA", 20, 0, 100, 69),
    "SMOKESCREEN": ("MURO DI FUMO", "NORMALE", 20, 0, 100, 108),
    "MIST": ("NEBBIA", "GHIACCIO", 30, 0, 0, 54),
    "HAZE": ("NUBE", "GHIACCIO", 30, 0, 0, 114),
    "NIGHT_SHADE": ("OMBRA NOTT.", "SPETTRO", 15, 0, 100, 101),
    "BONE_CLUB": ("OSSOCLAVA", "TERRA", 20, 65, 85, 125),
    "BONEMERANG": ("OSSOMERANG", "TERRA", 10, 50, 90, 155),
    "STUN_SPORE": ("PARALIZZANTE", "ERBA", 30, 0, 75, 78),
    "LEECH_SEED": ("PARASSISEME", "ERBA", 10, 0, 90, 73),
    "BIDE": ("PAZIENZA", "NORMALE", 10, 0, 0, 117),
    "DRILL_PECK": ("PERFORBECCO", "VOLANTE", 20, 80, 100, 65),
    "HORN_DRILL": ("PERFORCORNO", "NORMALE", 5, 0, 30, 32),
    "STOMP": ("PESTONE", "NORMALE", 20, 65, 100, 23),
    "PETAL_DANCE": ("PETALODANZA", "ERBA", 20, 70, 100, 80),
    "WATER_GUN": ("PISTOLACQUA", "ACQUA", 25, 40, 100, 55),
    "VICEGRIP": ("PRESA", "NORMALE", 30, 55, 100, 11),
    "PSYCHIC_M": ("PSICHICO", "PSICO", 10, 90, 100, 94),
    "PSYWAVE": ("PSICONDA", "PSICO", 15, 0, 80, 149),
    "PSYBEAM": ("PSICORAGGIO", "PSICO", 20, 65, 100, 60),
    "GUST": ("RAFFICA", "NORMALE", 35, 40, 100, 16),
    "HARDEN": ("RAFFORZATORE", "NORMALE", 30, 0, 0, 106),
    "AURORA_BEAM": ("RAGGIAURORA", "GHIACCIO", 20, 65, 100, 62),
    "DEFENSE_CURL": ("RICCIOLSCUDO", "NORMALE", 40, 0, 0, 111),
    "TAKE_DOWN": ("RIDUTTORE", "NORMALE", 20, 90, 85, 36),
    "REFLECT": ("RIFLESSO", "PSICO", 20, 0, 0, 115),
    "REST": ("RIPOSO", "PSICO", 10, 0, 0, 156),
    "RECOVER": ("RIPRESA", "NORMALE", 20, 0, 0, 105),
    "WITHDRAW": ("RITIRATA", "ACQUA", 40, 0, 0, 110),
    "GROWL": ("RUGGITO", "NORMALE", 40, 0, 100, 45),
    "LEECH_LIFE": ("SANGUISUGA", "COLEOTT", 15, 20, 100, 141),
    "ROCK_THROW": ("SASSATA", "ROCCIA", 15, 50, 65, 88),
    "LIGHT_SCREEN": ("SCHERMOLUCE", "PSICO", 30, 0, 0, 113),
    "SLAM": ("SCHIANTO", "NORMALE", 20, 80, 75, 21),
    "STRUGGLE": ("SCONTRO", "NORMALE", 0, 50, 100, 165),
    "ACID_ARMOR": ("SCUDO ACIDO", "VELENO", 40, 0, 0, 151),
    "DOUBLE_EDGE": ("SDOPPIATORE", "NORMALE", 15, 100, 100, 38),
    "BARRAGE": ("SFERATTACCO", "NORMALE", 20, 15, 85, 140),
    "FURY_SWIPES": ("SFURIATE", "NORMALE", 15, 18, 80, 154),
    "SMOG": ("SMOG", "VELENO", 20, 20, 70, 123),
    "SOLARBEAM": ("SOLARRAGGIO", "ERBA", 10, 120, 100, 76),
    "SONICBOOM": ("SONICBOOM", "NORMALE", 20, 0, 90, 49),
    "SLEEP_POWDER": ("SONNIFERO", "ERBA", 15, 0, 75, 79),
    "SUBSTITUTE": ("SOSTITUTO", "NORMALE", 10, 0, 0, 164),
    "SUBMISSION": ("SOTTOMISS.", "LOTTA", 25, 80, 80, 66),
    "SPIKE_CANNON": ("SPARALANCE", "NORMALE", 15, 20, 100, 131),
    "MIRROR_MOVE": ("SPECULMOSSA", "VOLANTE", 20, 0, 0, 119),
    "SPLASH": ("SPLASH", "NORMALE", 40, 0, 0, 150),
    "SPORE": ("SPORA", "ERBA", 15, 0, 100, 147),
    "DIZZY_PUNCH": ("STORDIPUGNO", "NORMALE", 10, 70, 100, 146),
    "CONFUSE_RAY": ("STORDIRAGGIO", "SPETTRO", 10, 0, 100, 109),
    "SCREECH": ("STRIDIO", "NORMALE", 40, 0, 85, 103),
    "SUPERSONIC": ("SUPERSUONO", "NORMALE", 20, 0, 55, 48),
    "SUPER_FANG": ("SUPERZANNA", "NORMALE", 10, 0, 90, 162),
    "SURF": ("SURF", "ACQUA", 15, 95, 100, 57),
    "CUT": ("TAGLIO", "NORMALE", 30, 50, 95, 15),
    "TELEPORT": ("TELETRASPOR.", "PSICO", 20, 0, 0, 100),
    "CLAMP": ("TENAGLIA", "ACQUA", 10, 35, 75, 128),
    "EARTHQUAKE": ("TERREMOTO", "TERRA", 10, 100, 100, 89),
    "TOXIC": ("TOSSINA", "VELENO", 10, 0, 85, 92),
    "TRANSFORM": ("TRASFORMAZ.", "NORMALE", 10, 0, 0, 144),
    "TRI_ATTACK": ("TRIPLETTA", "NORMALE", 10, 80, 100, 161),
    "THUNDER": ("TUONO", "ELETTRO", 10, 120, 70, 87),
    "THUNDER_WAVE": ("TUONONDA", "ELETTRO", 20, 0, 100, 86),
    "THUNDERPUNCH": ("TUONOPUGNO", "ELETTRO", 15, 75, 100, 9),
    "THUNDERSHOCK": ("TUONOSHOCK", "ELETTRO", 30, 40, 100, 84),
    "WHIRLWIND": ("TURBINE", "NORMALE", 20, 0, 85, 18),
    "FIRE_SPIN": ("TURBOFUOCO", "FUOCO", 15, 15, 70, 83),
    "SAND_ATTACK": ("TURBOSABBIA", "NORMALE", 15, 0, 100, 28),
    "EGG_BOMB": ("UOVOBOMBA", "NORMALE", 10, 100, 75, 121),
    "POISON_GAS": ("VELENOGAS", "VELENO", 40, 0, 55, 139),
    "POISON_STING": ("VELENOSPINA", "VELENO", 35, 15, 100, 40),
    "POISONPOWDER": ("VELENPOLVERE", "VELENO", 35, 0, 75, 77),
    "RAZOR_WIND": ("VENTAGLIENTE", "NORMALE", 10, 80, 75, 13),
    "FLY": ("VOLO", "VOLANTE", 15, 70, 95, 19)
}


growrate_to_level={"GROWTH_MEDIUM_FAST":(54,1000000),"GROWTH_MEDIUM_SLOW":(55,1059860),"GROWTH_FAST":(58,800000),"GROWTH_SLOW":(50,1250000),"GROWTH_GLITCH":(67,345420)}

# Input and output paths
input_path = 'evos_moves.asm'
output_dir = '../data/mons_json'
os.makedirs(output_dir, exist_ok=True)


# Regular expressions for parsing
mon_name_pattern = re.compile(r'^(\w+)EvosMoves:')
move_entry_pattern = re.compile(r'\s*db\s+(\d+),\s+(\w+)')
evolution_end_pattern = re.compile(r'\s*db\s+0')

# State machine flags
in_learnset = False
current_mon = None
current_moves = {}

mons_dict = {i[0].lower():{"name": i[1]} for i in pokemon_dict}

for j in range (len(pokemon_dict)):
    mon = pokemon_dict[j][0]
    input_path = "base_stats/"+mon.lower() + '.asm'
    with open(input_path, 'r') as f:
        lines = f.readlines()
        # Extract base stats from line 2
        base_stats_line = lines[2]
        base_stats = list(map(int, re.findall(r'\d+', base_stats_line)))
        base_stats.append(round(100*base_stats[3]/512,2))
        assert len(base_stats) == 6, f"Expected 6 base stats, got {len(base_stats)} in {mon}"
        # Swap last and second to last base stat
        types_line = lines[5]
        types = re.findall(r'\b[A-Z_]+\b', types_line)
        assert len(types) == 2, f"Expected 2 types, got {len(types)} in {mon}"
        moves_line=lines[12]
        start_moves = re.findall(r'\b[A-Z_]+\b', moves_line)
        growth_line=lines[13]
        growth_rate = re.findall(r'\b[A-Z_]+\b', growth_line)
        mons_dict[mon.lower()]["NO"]= j+1
        mons_dict[mon.lower()]["base_stats"]= base_stats
        mons_dict[mon.lower()]["types"]= [types_dict[types[0]], types_dict[types[1]]]
        mons_dict[mon.lower()]["expected_level"]= growrate_to_level[growth_rate[0]]
        mons_dict[mon.lower()]["level_up_moves"]= [(int(i),moves[start_moves[i].upper()]) for i in range(0, len(start_moves))]


input_path = 'evos_moves.asm'
# Process the file
with open(input_path, 'r') as f:
    for line in f:
        mon_match = mon_name_pattern.match(line)
        if mon_match:
            if current_mon in mons_dict:
                mons_dict[current_mon]["level_up_moves"].extend(current_moves)
                # Save previous mon's data
                #if current_mon and current_moves:
                # Reset state
            current_mon = mon_match.group(1).lower()
            current_moves = []
            in_learnset = False
            continue

        if current_mon:
            if not in_learnset:
                # Look for the end of evolution section
                if evolution_end_pattern.match(line):
                    in_learnset = True
                continue

            # Parse move entry lines
            move_match = move_entry_pattern.match(line)
            if move_match:
                level = int(move_match.group(1))
                move = move_match.group(2)
                current_moves.append((level, moves[move.upper()]))
            elif evolution_end_pattern.match(line):
                # End of learnset
                in_learnset = False

# Save the last mon

for i in mons_dict.keys():
    with open(os.path.join(output_dir, f"{i}.json"), 'w') as out_file:
        json.dump(mons_dict[i], out_file, indent=2)


print(f"JSON files generated in '{output_dir}' directory.")
