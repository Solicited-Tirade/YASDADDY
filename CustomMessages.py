# Personal message overrides. This file will NOT be overwritten by repository updates.
# Any key defined here takes precedence over the matching key in Messages.py.
#
# HOW TO USE:
#   1. Uncomment and edit the examples below, or add your own entries.
#   2. Only list keys you want to override — everything else falls back to Messages.py.
#   3. Run: python alerts.py -M "{ConstructorName}" to use a constructor.
#
# SET YOUR NAME:
#   Uncomment, and add "Name" to MESSAGE_VARIABLES below. It will appear anywhere {Name} is used,
#   including Introduction phrases and the LDispatchGreeting constructor.
#
# OVERRIDE A CONSTRUCTOR:
#   Define the same key here with a new template. Your version wins.
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
#     # --- Example: narrow down an existing variable to fewer options ---
#     # "Greetings": ["Hey there", "Hello"],
#
#     # --- Example: add a brand-new variable for use in custom constructors ---
#     # "MyVar": ["option one", "option two"],
#
# }
MESSAGE_VARIABLES: dict[str, str | list[str]] = {
    # "Name": "YourName",
}
