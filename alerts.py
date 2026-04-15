# Import standard library modules for CLI input, timestamps, and shell commands.
import re
import sys
import time
import subprocess

# Matches an offset like "4m30s", "4m", "30s", or a bare integer (legacy minutes).
_OFFSET_RE = re.compile(r"^(?:(\d+)m)?(?:(\d+)s)?$")

# IMPORTANT: Set to False to strip the animated Nitro-only emojis from ACTIVE_ALERT_TEMPLATE. If you do not have Nitro, this will not work well for you.
USE_NITRO_EMOJI = True

# Discord relative timestamp format, e.g. <t:1710000000:R>.
TIMESTAMP_SUFFIX = "<t:{unix_time}:R>"

# Emoji sequence for the "rtb" status.
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
SB_PREFIXES = {
    "sb1": "<:P1:1432823559364935852>",
    "sb2": "<:P2:1432823555698982973>",
    "sb3": "<:P3:1432823553186861109>",
    "sb4": "<:P4:1432823550997299330>",
    "sb5": "<:P5:1432823547902034010>",
}

# Full status templates that only need the timestamp appended.
STATUS_TEMPLATES = {
    "rtb": RTB_TEMPLATE,
    "active_alert": ACTIVE_ALERT_TEMPLATE,
}

# Key sequence for Ctrl+A to replace the current field contents.
SELECT_ALL_KEYS = ["ydotool", "key", "29:1", "30:1", "30:0", "29:0"]  # Ctrl+A
# Key sequence for Ctrl+V to paste clipboard contents.
PASTE_KEYS = ["ydotool", "key", "29:1", "47:1", "47:0", "29:0"]       # Ctrl+V


def parse_offset_action(action: str, prefix: str) -> tuple[str, int] | None:
    # A plain action with no suffix uses the current time.
    if action == prefix:
        return prefix, 0
    # Anything outside the "<prefix>+…" / "<prefix>-…" pattern is not handled here.
    if not action.startswith(prefix) or len(action) <= len(prefix):
        return None

    # The first character after the prefix decides whether to add or subtract time.
    sign = action[len(prefix)]
    if sign not in "+-":
        return None

    remainder = action[len(prefix) + 1:]

    # Legacy: bare integer with no unit is treated as minutes.
    if remainder.isdigit():
        total = int(remainder) * 60
    else:
        # Accepts "NmNs", "Nm", or "Ns" — at least one component must be present.
        m = _OFFSET_RE.match(remainder)
        if not m or not (m.group(1) or m.group(2)):
            return None
        total = int(m.group(1) or 0) * 60 + int(m.group(2) or 0)

    return prefix, total if sign == "+" else -total


def build_status(case_name: str) -> str:
    # Normalize the command so input is case-insensitive.
    case_name = case_name.lower()
    # Split a status action like "rtb+10" into its base name and time offset.
    base_name, offset_seconds = parse_status_action(case_name)
    # Every status ends with a relative timestamp for now, future, or past.
    timestamp = build_timestamp(offset_seconds)

    # Direct status templates just append the timestamp.
    if base_name in STATUS_TEMPLATES:
        return STATUS_TEMPLATES[base_name] + timestamp

    # SB statuses use a unique prefix plus the shared SB body and timestamp.
    if base_name in SB_PREFIXES:
        return SB_PREFIXES[base_name] + SB_TEMPLATE + timestamp

    # Show valid options when the user passes an unknown status action.
    valid = sorted([*STATUS_TEMPLATES.keys(), *SB_PREFIXES.keys()])
    raise ValueError(f"Unknown status case: {case_name}. Valid cases: {', '.join(valid)}")


def parse_status_action(action: str) -> tuple[str, int]:
    # Try every known status name, allowing an optional +N or -N minute suffix.
    for name in (*STATUS_TEMPLATES.keys(), *SB_PREFIXES.keys()):
        if parsed := parse_offset_action(action, name):
            return parsed

    # If no known status matches, return the original action so validation can fail cleanly later.
    return action, 0


def build_timestamp(offset_seconds: int = 0) -> str:
    # Convert the current Unix time, plus any offset, into Discord timestamp syntax.
    return TIMESTAMP_SUFFIX.format(unix_time=int(time.time()) + offset_seconds)


def build_timestamp_action(action: str) -> str | None:
    # Parse standalone timestamp actions with an optional +N or -N minute suffix.
    if not (parsed := parse_offset_action(action, "timestamp")):
        return None

    _, offset_seconds = parsed
    return build_timestamp(offset_seconds)


def _clipboard_paste(text: str, *, replace: bool, delay: float = 0.1) -> None:
    subprocess.run(["wl-copy"], input=text, text=True, check=True)
    time.sleep(delay)
    if replace:
        # Select all existing field contents before pasting.
        subprocess.run(SELECT_ALL_KEYS, check=True)
        time.sleep(delay)
    subprocess.run(PASTE_KEYS, check=True)


def main() -> int:
    # Expect exactly one action argument after the script name.
    if len(sys.argv) != 2:
        print("Usage: python alerts.py <action[+N|-N|+NmNs|-NmNs|+Nm|-Nm|+Ns|-Ns]>", file=sys.stderr)
        return 1

    try:
        # Normalize the action so commands are case-insensitive.
        action = sys.argv[1].lower()
        # Timestamp actions insert at the cursor instead of replacing the whole field.
        if timestamp := build_timestamp_action(action):
            _clipboard_paste(timestamp, replace=False)
        else:
            # All other recognized actions are full status templates.
            _clipboard_paste(build_status(action), replace=True)
        return 0
    except Exception as exc:
        # Report invalid actions or shell failures to stderr for easier debugging.
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    # Run the CLI entry point and exit with its status code.
    raise SystemExit(main())
