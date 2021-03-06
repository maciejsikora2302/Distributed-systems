PORT = 38000
SERVER_IP = "127.0.0.1"

SERVER_IP_UDP = "127.0.0.100"
PORT_UDP = 48005

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 58009
MULTICAST_TTL = 2

from sys import getsizeof
def send_in_fragments(msg, s_udp, address):
    chunk = ""
    i = 0
    for char in msg:
        chunk += char
        if getsizeof(chunk)>1000 and getsizeof(chunk)<1024:
            s_udp.sendto(bytes(chunk, encoding='utf-8'), address)
            chunk = ""
    s_udp.sendto(bytes(chunk, encoding='utf-8'), address)
    chunk = ""

def send_in_fragments_multi(msg, soc, address):   
    chunk = ""
    i = 0
    for char in msg:
        chunk += char
        if getsizeof(chunk)>1000 and getsizeof(chunk)<1024:
            soc.sendto(bytes(chunk, encoding='utf-8'), address)
            chunk = ""
    soc.sendto(bytes(chunk, encoding='utf-8'), address)
    chunk = ""




NICKNAMES = [
"Cannoli",
"Sweety",
"Cloud",
"Honey Pie",
"Buddy",
"Sunny",
"Daria",
"Buckeye",
"Loosetooth",
"Chiquita",
"Junior",
"Cottonball",
"Weirdo",
"Genius",
"Tickles",
"Bub",
"Azkaban",
"Boo Bear",
"Ducky",
"Buffalo",
"Twiggy",
"Lobster",
"Fun Dip",
"Sweet 'n Sour",
"Gator",
"Romeo",
"Knucklebutt",
"Chicken Legs",
"Muffin",
"Goon",
"Goose",
"Pintsize",
"Cold Front",
"Baby Carrot",
"Toodles",
"Dreamey",
"Smarty",
"Spicy",
"Hermione",
"Pinata",
"Rubber",
"Fly",
"Doll",
"Jet",
"Babe",
"Itchy",
"Diet Coke",
"Frau Frau",
"Amorcita",
"Shuttershy",
"Rockette",
"Miss Piggy",
"Ghoulie",
"Shorty",
"Tank",
"Autumn",
"Pig",
"Marshmallow",
"Bug",
"Dud",
"Smoochie",
"Papito",
"Pansy",
"French Fry",
"Boomhauer",
"Dunce",
"Einstein",
"Bruiser",
"Piglet",
"Smirk",
"Gummy Pop",
"Terminator",
"Big Mac",
"Mini Skirt",
"Gingersnap",
"Gordo",
"Pyscho",
"Duckling",
"Oompa Loompa",
"Dumbledore",
"Wilma",
"Mini Mini",
"Dummy",
"Amazon",
"Dimples",
"Ami",
"Skipper",
"Twig",
"Beautiful",
"Captain Crunch",
"Rumplestiltskin",
"Amour",
"Creedence",
"Cheddar",
"Joker",
"Candycane",
"Chump",
"Dragonfly",
"Silly Gilly",
"Sweetums",
]