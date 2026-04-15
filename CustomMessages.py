# Personal message overrides. This file will NOT be overwritten by repository updates.
# Any key defined here takes precedence over the matching key in Messages.py.
#
# HOW TO USE:
#   1. Edit the entries below, or add your own.
#   2. Only list keys you want to change — everything else falls back to Messages.py.
#   3. Run: python alerts.py -M "{VariableName}" to use a constructor or message variable.
#
# SET YOUR NAME:
#   Edit the "Name" variable to your in-game name. Keep it in quotes. It will appear anywhere {Name} is used,
#   including Introduction phrases and the LDispatchGreeting constructor.
#
# VARIABLE MODIFIERS and overrides (list variables only):
#   "Key"   — fully replace the base list with your own. For example, if you redefine {Greetings}, the original greetings are discarded and only your phrases are used.
#   "+Key"  — append your phrases to the base list (adds to the rotation), for example, if you add "+" to "Greetings" (+Greetings), your phrases are added to the existing greetings and all are used in rotation.
#   "-Key"  — remove specific phrases from the base list (prunes the rotation), for example, if you add "-" to "Greetings" (-Greetings), and list "Good day" and "Greetings", those two greetings are removed from the rotation but all other greetings remain.

# CONSTRUCTOR OVERRIDES:
#   Define the same key here with a new template. Your version wins.
#   Constructors are strings, so +/- modifiers do not apply to them.

## DO NOT ADD MODIFIERS TO MESSAGE_CONSTRUCTORS KEYS##

MESSAGE_CONSTRUCTORS: dict[str, str] = {
    # Override an existing constructor:
    # "ApologyWaitQUpdate": "{ApologiesWait}. {TeamEnRoute}. {QUpdate}",

    # Add a brand-new constructor:
    # "MyCustomGreeting": "{Greetings}, {Introduction}. {Pleasantries}.",
}

MESSAGE_VARIABLES: dict[str, str | list[str]] = {
    # Your name — appears in {Introduction}, {LDispatchGreeting}, and anywhere {Name} is used.
    "Name": "ChangeYourNameHere",

    # Add phrases to an existing variable (base phrases are kept):
    # "+Greetings": ["Howdy", "What's up"],

    # Remove specific phrases from an existing variable:
    # "-Greetings": ["Good day", "Greetings"],

    # Fully replace an existing variable (base phrases are discarded):
    # "Greetings": ["Hey there", "Hello"],

    # Add a brand-new variable for use in custom constructors:
    # "MyVar": ["option one", "option two"],
}
