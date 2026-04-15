# Personal message overrides. This file will NOT be overwritten by repository updates.
# Any key defined here takes precedence over the matching key in Messages.py.
#
# HOW TO USE:
#   1. Uncomment and edit the examples below, or add your own entries.
#   2. Only list keys you want to change — everything else falls back to Messages.py.
#   3. Run: python alerts.py -M "{ConstructorName}" to use a constructor.
#
# SET YOUR NAME:
#   Uncomment, and add "Name" to MESSAGE_VARIABLES below. It will appear anywhere {Name} is used,
#   including Introduction phrases and the LDispatchGreeting constructor.
#
# VARIABLE MODIFIERS (list variables only):
#   "Key"   — fully replace the base list with your own (plain override)
#   "+Key"  — append your phrases to the base list (adds to the rotation)
#   "-Key"  — remove specific phrases from the base list (prunes the rotation)
#
# OVERRIDE A CONSTRUCTOR:
#   Define the same key here with a new template. Your version wins.
#   (Constructors are strings, so +/- modifiers do not apply to them.)
#
# ADD A NEW CONSTRUCTOR OR VARIABLE:
#   Just add a new key — it will be available in -M strings right away.

# MESSAGE_CONSTRUCTORS: dict[str, str] = {
#
#     # --- Example: override an existing constructor ---
#     # "ApologyWaitQUpdate": "{ApologiesWait}. {TeamEnRoute}. {QUpdate}",
#     # "ApologyWaitUpdate":  "{ApologiesWait}. {TeamEnRoute}. {AUpdate}",
#
#     # --- Example: add a brand-new constructor ---
#     # "MyCustomGreeting": "{Greetings}, {Introduction}. {Pleasantries}.",
#
# }
MESSAGE_CONSTRUCTORS: dict[str, str] = {}

# MESSAGE_VARIABLES: dict[str, str | list[str]] = {
#
#     # --- Set your name (appears in {Introduction}, {LDispatchGreeting}, etc.) ---
#     # "Name": "YourName",
#
#     # --- Add phrases to an existing variable (+ prefix, does not remove base phrases) ---
#     # "+Greetings": ["Howdy", "What's up"],
#
#     # --- Remove specific phrases from an existing variable (- prefix) ---
#     # "-Greetings": ["Good day", "Greetings"],
#
#     # --- Fully replace an existing variable (no prefix, base phrases are discarded) ---
#     # "Greetings": ["Hey there", "Hello"],
#
#     # --- Add a brand-new variable for use in custom constructors ---
#     # "MyVar": ["option one", "option two"],
#
# }
MESSAGE_VARIABLES: dict[str, str | list[str]] = {
    # "Name": "YourName",
}
