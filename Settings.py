# ============================================================
# CONFIGURE THIS FILE BEFORE YOUR FIRST RUN
#
#   1. Set NAME to your in-game name.
#   2. Set USE_NITRO_EMOJI to False if you do not have Discord Nitro.
#   3. Set OS_MODE if you prefer not to use auto-detection.
#
# Everything else can be left at its default.
# This file will NOT be overwritten by repository updates.
# ============================================================

###############################################################################
# USER SETTINGS
# Common options most users will want to configure.
###############################################################################

# Controls which clipboard/input backend is used.
# "auto"    — detect the OS at runtime (recommended for most users)
# "linux"   — force Linux backend (wl-copy + ydotool), regardless of detected OS
# "windows" — force Windows backend, regardless of detected OS (not yet implemented)
# Set this manually if you prefer not to have the script inspect your system at runtime.
OS_MODE: str = "auto"  # "auto" | "linux" | "windows"

# Your in-game name. Appears in {Introduction} phrases, {LDispatchGreeting}, and anywhere {Name} is used.
NAME: str = "YourName"

# IMPORTANT: Set to False to strip the animated Nitro-only emojis from the active_alert status.
# If you do not have Discord Nitro, set this to False.
USE_NITRO_EMOJI: bool = True

###############################################################################
# ADVANCED — EMOJI TEMPLATES

##ONLY ADJUST IF YOU KNOW WHAT YOU'RE DOING##

# Discord emoji IDs are server-specific. Only edit these if you want to use
# different custom emojis than the defaults.
# Don't forget that you need Nitro to edit emojis in your status, and that the emojis you use must
# be in a server you have access to.
# Each template is a concatenated string of Discord emoji tags
# in the format <:name:id> or <a:name:id>.
###############################################################################

# Emoji sequence for the "return to base" status.
RTB_TEMPLATE = (
    "<:RTB1:1182246669564256296>"
    "<:RTB2:1182246670717689867>"
    "<:RTB3:1182246674383507476>"
    "<:RTB4:1182246677101412392>"
    "<:RTB5:1182246678397464596>"
    "<:RTB6:1182246679680929803>"
    "<:RTB7:1182246686177894430>"
    "<:RTB8:1182246689336213575>"
)

# Static (non-Nitro) core emoji sequence for the "active_alert" status.
_ACTIVE_ALERT_CORE = (
    "<:AA1:1182246601557823520>"
    "<:AA2:1182246604401561610>"
    "<:AA3:1182246605718556682>"
    "<:AA4:1182246607228514304>"
    "<:AA5:1182246610189692938>"
    "<:AA6:1182246613150859304>"
    "<:AA7:1182246614665019393>"
    "<:AA8:1182246617559072838>"
)

# Animated Nitro-only bookend emojis that wrap the core sequence.
_AA_NITRO_PREFIX = "<a:AlertBlue:1064652389711360043><a:AlertRed:985293780288700476>"
_AA_NITRO_SUFFIX = "<a:AlertRed:985293780288700476><a:AlertBlue:1064652389711360043>"

# Emoji sequence for the "active_alert" status.
# Nitro prefix/suffix are included or excluded based on USE_NITRO_EMOJI above.
ACTIVE_ALERT_TEMPLATE = (
    (_AA_NITRO_PREFIX if USE_NITRO_EMOJI else "")
    + _ACTIVE_ALERT_CORE
    + (_AA_NITRO_SUFFIX if USE_NITRO_EMOJI else "")
)

# Shared emoji sequence used by all "sb" variants.
SB_TEMPLATE = (
    "<:SB1:1182246721129025657>"
    "<:SB2:1182246723981164665>"
    "<:SB3:1182246726137036891>"
    "<:SB4:1182246729844797440>"
    "<:SB5:1182246731447021589>"
    "<:SB6:1182246733946818620>"
    "<:SB7:1182246735616155648>"
)

# Prefix emoji for each SB variant before the shared SB template.
SB_PREFIXES: dict[str, str] = {
    "sb1": "<:P1:1432823559364935852>",
    "sb2": "<:P2:1432823555698982973>",
    "sb3": "<:P3:1432823553186861109>",
    "sb4": "<:P4:1432823550997299330>",
    "sb5": "<:P5:1432823547902034010>",
}

# Full status templates that only need the timestamp appended.
# Add new statuses here as { "name": EMOJI_TEMPLATE } entries.
STATUS_TEMPLATES: dict[str, str] = {
    "rtb": RTB_TEMPLATE,
    "active_alert": ACTIVE_ALERT_TEMPLATE,
    **{name: prefix + SB_TEMPLATE for name, prefix in SB_PREFIXES.items()},
}
