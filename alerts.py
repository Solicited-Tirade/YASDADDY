# Import standard library modules for CLI input, timestamps, and shell commands.
import re
import sys
import time
import random
import subprocess
from Messages import MESSAGE_CONSTRUCTORS as _base_constructors, MESSAGE_VARIABLES as _base_variables
from CustomMessages import MESSAGE_CONSTRUCTORS as _custom_constructors, MESSAGE_VARIABLES as _custom_variables
from Settings import OS_MODE, STATUS_TEMPLATES

# Matches an offset like "4m30s", "4m", "30s", or a bare integer (legacy minutes).
_OFFSET_RE = re.compile(r"^(?:(\d+)m)?(?:(\d+)s)?$")

###Initialization Components###

def _merge_variables(
    base: dict[str, str | list[str]],
    custom: dict[str, str | list[str]],
) -> dict[str, str | list[str]]:
    # Merge custom variable overrides into the base, supporting +/- key modifiers.
    # +Key  — append the custom list to the existing base list for Key
    # -Key  — remove each listed item from the existing base list for Key
    # Key   — fully replace the base entry (plain override)
    result: dict[str, str | list[str]] = dict(base)
    for key, value in custom.items():
        if key.startswith("+"):
            base_key = key[1:]
            if base_key in result and isinstance(result[base_key], list) and isinstance(value, list):
                result[base_key] = result[base_key] + value
            else:
                result[base_key] = value
        elif key.startswith("-"):
            base_key = key[1:]
            if base_key in result and isinstance(result[base_key], list) and isinstance(value, list):
                remove_set = set(value)
                result[base_key] = [v for v in result[base_key] if v not in remove_set]
        else:
            result[key] = value
    return result


# Messages are loaded from Messages.py (built-in) and CustomMessages.py (your overrides).
# Constructors: plain key override only. Variables: use +Key / -Key to append or remove
# individual phrases without replacing the full list — see CustomMessages.py.
MESSAGE_CONSTRUCTORS: dict[str, str] = {**_base_constructors, **_custom_constructors}
MESSAGE_VARIABLES: dict[str, str | list[str]] = _merge_variables(_base_variables, _custom_variables)


# Discord relative timestamp format, e.g. <t:1710000000:R>.
TIMESTAMP_SUFFIX = "<t:{unix_time}:R>"

# Key sequence for Ctrl+A to replace the current field contents.
SELECT_ALL_KEYS = ["ydotool", "key", "29:1", "30:1", "30:0", "29:0"]  # Ctrl+A
# Key sequence for Ctrl+V to paste clipboard contents.
PASTE_KEYS = ["ydotool", "key", "29:1", "47:1", "47:0", "29:0"]  # Ctrl+V
# Key sequence for Enter to submit the current field.
ENTER_KEYS = ["ydotool", "key", "28:1", "28:0"]  # Enter


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

    remainder = action[len(prefix) + 1 :]

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

    # All status templates just append the timestamp.
    if base_name in STATUS_TEMPLATES:
        return STATUS_TEMPLATES[base_name] + timestamp

    # Show valid options when the user passes an unknown status action.
    valid = sorted(STATUS_TEMPLATES.keys())
    raise ValueError(
        f"Unknown status case: {case_name}. Valid cases: {', '.join(valid)}"
    )


def parse_status_action(action: str) -> tuple[str, int]:
    # Try every known status name, allowing an optional +N or -N minute suffix.
    for name in STATUS_TEMPLATES.keys():
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


def resolve_message(text: str) -> str:
    # Pre-pass: expand any {ConstructorName} tokens into their full template strings.
    # This happens before variable resolution so the expanded template is then processed normally.
    def _expand_constructor(match: re.Match) -> str:
        name = match.group(1)
        for key, template in MESSAGE_CONSTRUCTORS.items():
            if key.lower() == name.lower():
                return template
        return match.group(0)

    result = re.sub(r"\{(\w+)\}", _expand_constructor, text)

    # Main pass: replace every {VarName} token with its value from MESSAGE_VARIABLES.
    # List values are randomly chosen; string values are used directly.
    # Unknown variable names are left unchanged.
    def _replace(match: re.Match) -> str:
        var_name = match.group(1)
        for key, value in MESSAGE_VARIABLES.items():
            if key.lower() == var_name.lower():
                return random.choice(value) if isinstance(value, list) else value
        return match.group(0)

    result = re.sub(r"\{(\w+)\}", _replace, result)
    # Second pass: resolves variable tokens embedded inside variable values (e.g. {Name} inside Introduction).
    result = re.sub(r"\{(\w+)\}", _replace, result)

    # Capitalize the first letter of the message.
    # Variable values are lowercase phrases — the template decides what leads the sentence.
    if result:
        result = result[0].upper() + result[1:]

    # Capitalize the first letter after any sentence-ending punctuation (". ", "! ", "? ").
    # This handles mid-string periods from the template, e.g. "...help. please..." → "...help. Please..."
    result = re.sub(
        r"([.!?]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), result
    )

    # Append a period only if the message has no closing punctuation.
    # If your template ends with "?" or "!" or ".", this is left alone.
    # Commas and other mid-sentence punctuation in the template are never affected.
    if result and result[-1] not in ".!?":
        result += "."

    return result


def _resolve_os() -> str:
    """Return the active OS backend name, resolving 'auto' via platform detection."""
    if OS_MODE != "auto":
        return OS_MODE.lower()
    import platform
    system = platform.system().lower()
    if system == "linux":
        return "linux"
    if system == "windows":
        return "windows"
    raise RuntimeError(
        f"Unsupported OS detected: {platform.system()!r}. "
        "Set OS_MODE to 'linux' or 'windows' manually in Settings.py."
    )


def _clipboard_paste_linux(text: str, *, replace: bool, send: bool = False, delay: float = 0.1) -> None:
    subprocess.run(["wl-copy"], input=text, text=True, check=True)
    time.sleep(delay)
    if replace:
        # Select all existing field contents before pasting.
        subprocess.run(SELECT_ALL_KEYS, check=True)
        time.sleep(delay)
    subprocess.run(PASTE_KEYS, check=True)
    if send:
        time.sleep(delay)
        subprocess.run(ENTER_KEYS, check=True)


def _clipboard_paste_windows(text: str, *, replace: bool, send: bool = False, delay: float = 0.1) -> None:
    del text, replace, send, delay  # unused until Windows support is implemented
    # TODO: implement Windows clipboard (e.g. win32clipboard or ctypes SetClipboardData)
    # and keypress automation (e.g. ctypes SendInput or pyautogui) for Ctrl+A / Ctrl+V / Enter.
    raise NotImplementedError(
        "Windows clipboard support is not yet implemented. "
        "Set OS_MODE = 'linux' in Settings.py if you are on Linux."
    )


def _clipboard_paste(text: str, *, replace: bool, send: bool = False, delay: float = 0.1) -> None:
    backend = _resolve_os()
    if backend == "linux":
        _clipboard_paste_linux(text, replace=replace, send=send, delay=delay)
    elif backend == "windows":
        _clipboard_paste_windows(text, replace=replace, send=send, delay=delay)
    else:
        raise RuntimeError(f"No clipboard backend for OS: {backend!r}")


def main() -> int:
    # Strip the optional -S flag before dispatching; its presence enables auto-submit.
    args = sys.argv[1:]
    send = "-S" in args
    if send:
        args = [a for a in args if a != "-S"]

    # -M "message" pastes a custom message, optionally with {Variable} interpolation.
    if len(args) == 2 and args[0] == "-M":
        try:
            message = resolve_message(args[1])
            _clipboard_paste(message, replace=False, send=send)
            return 0
        except Exception as exc:
            print(exc, file=sys.stderr)
            return 1

    # Expect exactly one action argument after the script name.
    if len(args) != 1:
        print(
            "Usage: python alerts.py [-S] <action[+N|-N|+NmNs|-NmNs|+Nm|-Nm|+Ns|-Ns]>\n"
            '       python alerts.py [-S] -M "message with optional {Variables}"\n'
            "       -S  send immediately by pressing Enter after the paste",
            file=sys.stderr,
        )
        return 1

    try:
        # Normalize the action so commands are case-insensitive.
        action = args[0].lower()
        # Timestamp actions insert at the cursor instead of replacing the whole field.
        if timestamp := build_timestamp_action(action):
            _clipboard_paste(timestamp, replace=False, send=send)
        else:
            # All other recognized actions are full status templates.
            _clipboard_paste(build_status(action), replace=True, send=send)
        return 0
    except Exception as exc:
        # Report invalid actions or shell failures to stderr for easier debugging.
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    # Run the CLI entry point and exit with its status code.
    raise SystemExit(main())
