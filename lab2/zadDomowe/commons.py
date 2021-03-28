#Shared names for exchanges present in project
CLIENT_EXCHANGE = "client_exchange"
SUPPLIER_EXCHNAGE = "supplier_exchange"
ADMIN_CLIENT_EXCHANGE = "admin_client_exchange"
ADMIN_SUPPLIER_EXCHANGE = "admin_supplier_exchange"

#All items that suppliers can provide
ITEMS = ['plecak', 'tlen', 'buty']

#Setting up non-unique structures for communication
def standard_setup(channel):
    #All Exchanges that should be present in application
    channel.exchange_declare(exchange=CLIENT_EXCHANGE, exchange_type='topic')
    channel.exchange_declare(exchange=SUPPLIER_EXCHNAGE, exchange_type='topic')
    channel.exchange_declare(exchange=ADMIN_CLIENT_EXCHANGE, exchange_type='fanout')
    channel.exchange_declare(exchange=ADMIN_SUPPLIER_EXCHANGE, exchange_type='fanout')

    #Queues on which Administrator should listen
    channel.queue_declare(queue="admin-order")
    channel.queue_bind(exchange=CLIENT_EXCHANGE, queue="admin-order", routing_key="*")
    channel.queue_declare(queue="admin-delivery")
    channel.queue_bind(exchange=SUPPLIER_EXCHNAGE, queue="admin-delivery", routing_key="*.*")

    #Queues for each item type
    for item in ITEMS:
        channel.queue_declare(queue=item)
        channel.queue_bind(exchange=CLIENT_EXCHANGE, queue=item, routing_key=item)
        
#List of random names
NAMES = [
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