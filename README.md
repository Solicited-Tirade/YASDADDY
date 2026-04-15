# YASDADDY Guide

## Yet Another Stream Deck Alert tool Developed for Dispatchers with Ydotool 

### This tool is agnostic, and can be run without a physical button, if you so choose. It just makes it more convenient. Essentially, you just need something that launches the python script.

`alerts.py` is a small helper script that builds a Discord-formatted alert string, copies it to the clipboard, and pastes it. It is currently implemented for Linux (`wl-copy` + `ydotool`), with a Windows backend planned. The active backend is controlled by `OS_MODE` in `Settings.py`.

Personally, I use this with a Stream Deck, but you can use whatever you want as long as it can run a python script. I made this script with multi-interface usages in mind.

---

## Table of Contents

- [Before You Start](#before-you-start)
- [What It Does](#what-it-does)
- [Requirements](#requirements)
- [Future Plans](#future-plans)
- [Configuration](#configuration)
  - [Emoji Templates](#emoji-templates)
  - [Setting Your Name](#setting-your-name)
- [Customization Files](#customization-files)
  - [How Overrides Work](#how-overrides-work)
  - [Message Constructors](#message-constructors)
  - [Message Variables](#message-variables)
- [Usage](#usage)
- [Supported Status Actions](#supported-status-actions)
- [Offset Format](#offset-format)
- [Supported Timestamp Actions](#supported-timestamp-actions)
- [Custom Message Actions](#custom-message-actions)
- [Internal Function Overview](#internal-function-overview)
  - [`_resolve_os`](#_resolve_os)
  - [`_clipboard_paste`](#_clipboard_paste)
  - [`build_status`](#build_status)
  - [`build_timestamp`](#build_timestamp)
  - [`build_timestamp_action`](#build_timestamp_action)
  - [`parse_offset_action`](#parse_offset_action)
  - [`resolve_message`](#resolve_message)
  - [`main`](#main)
- [Quick Reference](#quick-reference)

---

## Before You Start

**Open `Settings.py` and configure it before running the script for the first time.**

| Setting | What to do |
|---------|------------|
| `NAME` | Set this to your in-game name. It appears in greetings, introductions, and anywhere `{Name}` is used. |
| `USE_NITRO_EMOJI` | Set to `False` if you do not have Discord Nitro. Leaving it `True` without Nitro will send broken animated emoji tags. |
| `OS_MODE` | Leave as `"auto"` unless you want to force a specific backend or avoid runtime OS detection. |

Everything else in `Settings.py` can be left at its default until you need it.

---

## What It Does

The script currently supports three kinds of actions:

1. Status actions
   These build a full alert/status string and replace the current field contents with `Ctrl+A` + paste.
   They can also include a `+N` or `-N` suffix to offset the timestamp.

2. Timestamp actions
   These build only the Discord relative timestamp suffix and paste it at the current cursor position without `Ctrl+A`.

3. Custom message actions (`-M`)
   These paste a freeform message at the current cursor position. The message can contain `{Variable}` tokens and `{ConstructorName}` shorthands that are resolved before pasting. This is the core of the personalization system — build messages that reflect your own style, tone, and workflow rather than sending the same text every time.

## Requirements

The script expects these tools to exist on the system:

- `python` (may be `python3`, `python3.14`, etc. — use whatever your environment resolves to)
- `wl-copy` *(Linux only)*
- `ydotool` *(Linux only)*

> **Note:** All examples in this guide use `python` for brevity. Substitute the correct invocation for your system (e.g. `python3 alerts.py active_alert`).

## Future Plans

- **Windows clipboard support** — the backend stub is in place; copy/paste automation via `win32clipboard` / `ctypes SendInput` is the next step.
- **Small API functionality or OCR** to determine who the client is and perform `%CLIENT_NAME%` grabbing to personalize messages automatically.

## Configuration

User-configurable settings live in `Settings.py`. Edit this file to match your setup. It is gitignored, so your changes are never overwritten by updates.

| Variable | Default | Description |
|----------|---------|-------------|
| `OS_MODE` | `"auto"` | Controls which clipboard/input backend is used. `"auto"` detects the OS at runtime via `platform.system()`. `"linux"` or `"windows"` forces a specific backend regardless of detection. Set manually for a more privacy-focused approach — auto-detection never runs. |
| `USE_NITRO_EMOJI` | `True` | Include animated Nitro-only emojis in `active_alert`. Set to `False` if you don't have Discord Nitro. |

### Emoji Templates

`Settings.py` also contains all Discord emoji sequences used by status actions. Each template is a string of custom emoji IDs tied to a specific Discord server. Edit these if your server uses different emoji IDs.

| Constant | Used by |
|----------|---------|
| `RTB_TEMPLATE` | `rtb` status |
| `ACTIVE_ALERT_TEMPLATE` | `active_alert` status — built from `_ACTIVE_ALERT_CORE` plus optional Nitro bookends controlled by `USE_NITRO_EMOJI` |
| `SB_TEMPLATE` | `sb1`–`sb5` statuses (shared body) |
| `SB_PREFIXES` | `sb1`–`sb5` statuses (per-variant prefix emoji) |
| `STATUS_TEMPLATES` | Maps status names to their emoji strings — add new statuses here |

### Setting Your Name

Set `NAME` in `Settings.py`:

```python
NAME: str = "YourName"
```

It will appear anywhere `{Name}` is used — `{Introduction}` phrases, `{LDispatchGreeting}`, and any constructor or `-M` string you write.

## Customization Files

Three files let you customize behaviour without touching `alerts.py`, and without risking your changes being overwritten on updates.

| File | Tracked by git | Purpose |
|------|---------------|---------|
| `Messages.py` | Yes | Ships with the repo. Contains all built-in `MESSAGE_CONSTRUCTORS` and `MESSAGE_VARIABLES`. **Do not edit** — it will be overwritten on updates. |
| `CustomMessages.py` | No | Your personal message overrides. Never touched by repo updates. Any key defined here takes precedence over the same key in `Messages.py`. |
| `Settings.py` | No | Your personal runtime settings and emoji templates. Never touched by repo updates. Edit this to set `OS_MODE`, `USE_NITRO_EMOJI`, and Discord emoji IDs. |

### How Overrides Work

`alerts.py` merges the two files at startup. Constructors use a plain dict merge (last key wins). Variables use a smarter merge that understands `+`/`-` key modifiers:

| Key style | Effect |
|-----------|--------|
| `"Key"` | **Replace** — your list fully replaces the base list |
| `"+Key"` | **Append** — your phrases are added to the base rotation |
| `"-Key"` | **Remove** — listed phrases are pruned from the base rotation |

You only need to list the keys you want to change. Everything else falls back to `Messages.py`.

**Example — add phrases to an existing variable:**

```python
MESSAGE_VARIABLES: dict[str, str | list[str]] = {
    "+Greetings": ["Howdy", "What's up"],  # base phrases kept, these added
}
```

**Example — remove phrases from an existing variable:**

```python
MESSAGE_VARIABLES: dict[str, str | list[str]] = {
    "-Greetings": ["Good day", "Greetings"],  # prune the formal ones
}
```

**Example — fully replace a variable:**

```python
MESSAGE_VARIABLES: dict[str, str | list[str]] = {
    "Greetings": ["Hey there", "Hello"],  # base phrases discarded
}
```

**Example — override a constructor:**

```python
# Constructors are strings — no +/- modifiers, plain key wins.
MESSAGE_CONSTRUCTORS: dict[str, str] = {
    "ApologyWaitQUpdate": "{ApologiesWait}. {TeamEnRoute}. {QUpdate}",
}
```

### Message Constructors

Constructors are named shorthands that expand into a full template string. Use `{ConstructorName}` inside your `-M` string to expand one. They are your personal toolkit — build out exactly the messages you want to send, composed from whatever variables and fixed text fit your style. A constructor can be as simple or as elaborate as you like, and you can add as many as you need.

```python
# Messages.py (built-in)
MESSAGE_CONSTRUCTORS: dict[str, str] = {
    "FullGreetingQuestionnaire": "{Greetings}, {Introduction}, {Pleasantries}. {Questionnaire}?",
    "DispatchGreeting":          "{Greetings}! {Introduction}, and {StandingBy}. {SendingInvites}...",
    "EnRoute":                   "{AUpdate}! {TeamEnRoute}. {ArrivalNotice}.",
    "CloseSuccess":              "{ThanksWait}! As we conclude our service...",
    # ... see Messages.py for the full list
}
```

Constructors are grouped in `Messages.py` as follows:

- **Greeting openers** — `FullGreetingQuestionnaire`, `FullGreetingStranded`, `FullGreetingMoreInfo`, `GreetingQUpdate`
- **Thank → follow-up** — `ThanksMoreInfo`, `ThanksUpdate`, `ThanksWaitQUpdate`, `ThanksWaitMoreInfo`
- **Apology → follow-up** — `ApologyWaitQUpdate`, `ApologyWaitUpdate`, `ApologyInconvenienceMoreInfo`, `ApologyFrustrationMoreInfo`, `ApologyConfusionMoreInfo`
- **Vitals checks** — `VitalsCheck`, `VitalsRadiationCheck`, `GreetingVitalsCheck`, `GreetingVitalsRadiationCheck`
- **Legacy canned responses** (`L` prefix) — verbatim originals for every stage of the normal alert workflow
- **Flair canned responses** — similar to the above, but with `{Variable}` tokens for randomized phrasing, and added flair

#### Legacy vs. Flair

Not every constructor needs to use variables. Sometimes you already have a set of phrases you're comfortable with and want them sent exactly as written — no randomness, no surprises. The `L`-prefixed constructors exist for that reason: they are static, predictable, and unchanged from the original wording.

The flair versions of those same constructors inject `{Variable}` tokens to vary the phrasing on each use. Both are valid — which you reach for is a matter of preference and situation.

Constructor values may themselves contain `{VarName}` tokens — they are resolved in the normal variable pass after expansion.

> **Note:** Do not end constructor templates with punctuation. Let the auto-formatter handle it, or include your own closing punctuation (e.g. `?`) directly in the template string.

### Message Variables

Variables are resolved after constructors. List values are randomly chosen on each run; plain strings are always used verbatim. They are the building blocks of the personalization system — swap in your own phrases, adjust the tone, and tailor the wording to your personality. Adding more options to a list increases variety without requiring any changes to your constructors.

```python
# Messages.py (built-in defaults)
MESSAGE_VARIABLES: dict[str, str | list[str]] = {
    # Identity
    "Name":                   "YourName",  # override in CustomMessages.py
    # General
    "Greetings":              ["Hey there", "Hello", "Hi", ...],
    "Introduction":           ["my name is {Name}", "I'm {Name}", ...],  # {Name} resolved at build time
    "Pleasantries":           ["I hope you're having a great day", ...],
    "Questionnaire":          ["please take a moment to fill out the questionnaire", ...],
    "QUpdate":                ["can you provide me with an update", ...],
    "Moreinfo":               ["could you provide me with some more information", ...],
    "AUpdate":                ["good news, I have an update for you", ...],
    # Acknowledgements
    "Thanks":                 ["thanks", "thank you", ...],
    "ThanksWait":             ["thank you for your patience and cooperation", ...],
    # Apologies
    "ApologiesWait":          ["I'm sorry for the delay", ...],
    "ApologiesInconvenience": ["I apologize for the inconvenience", ...],
    "ApologiesFrustration":   ["I apologize for any frustration this may have caused", ...],
    "ApologiesConfusion":     ["I'm sorry for any confusion", ...],
    # Vitals
    "OxygenLevel":            ["what are your current oxygen levels", ...],
    "Radiation":              ["are you currently in a radiation zone", ...],
    "ThirstHunger":           ["what are your current thirst and hunger levels", ...],
    # Medrunner operational phrases
    "ServiceWelcome":         ["thank you for choosing Medrunner Services", "welcome to Medrunner Services", ...],
    "Received":               ["we've received your alert", "your alert has been received", ...],
    "Assurances":             ["no need to worry", "you're in good hands", "help is on the way", ...],
    "StandingBy":             ["I'll be your dispatcher for this alert", "I'm handling your dispatch today", ...],
    "SendingInvites":         ["the team leader will be sending you a friend request and/or party invite", ...],
    "ReadyForInvites":        ["please let me know when you are ready to receive the invites", ...],
    "SpamAcceptKey":          ["please spam the accept key", "mash that accept key", ...],
    "TeamEnRoute":            ["our team is en route", "the team is headed your way", ...],
    "ArrivalNotice":          ["I will update you when we are shortly arriving", "I'll keep you posted as we get close", ...],
    "SecuringArea":           ["please be patient while we secure the area", "hold tight while we handle the area", ...],
    "NoContactClose":         ["if we haven't heard from you within the next 5 minutes...", ...],
    "StandingDown":           ["standing down due to no contact", "closing this alert due to no response", ...],
}
```

> **Note:** Do not end variable values with punctuation. Punctuation and spacing belong in your `-M` template string or constructor. The auto-formatter will capitalize the first letter and add a trailing period if needed.

## Usage

```bash
python alerts.py [-S] <action>
python alerts.py [-S] -M "message with optional {Variables}"
```

The optional `-S` flag sends Enter immediately after the paste, submitting the message without touching the keyboard. It can be placed anywhere in the argument list.

If no action or an invalid action is provided, the script exits with an error.

## Supported Status Actions

These actions replace the current text box contents, then paste a generated string that ends with a relative Discord timestamp like `<t:...:R>`.

- `rtb`, `active_alert`, `sb1`–`sb5`
- Any of the above with an optional offset suffix (see [Offset Format](#offset-format))

### How Status Actions Work

- `rtb` uses the RTB emoji template plus the current timestamp suffix.
- `active_alert` uses the active alert emoji template plus the current timestamp suffix. When `USE_NITRO_EMOJI = True`, animated bookend emojis are included.
- `sb1` through `sb5` each use:
  their own prefix emoji, the shared SB emoji template, and the timestamp suffix.

### Status Examples

- `rtb` — current time
- `rtb+20` — 20 minutes in the future
- `active_alert-10` — 10 minutes in the past
- `sb3+4m30s` — 4 minutes and 30 seconds in the future

When a status action runs, the script:

1. Copies the generated text to the clipboard.
2. Waits briefly.
3. Sends `Ctrl+A`.
4. Waits briefly.
5. Sends `Ctrl+V`.
6. *(if `-S`)* Waits briefly, then sends `Enter`.

This means the current input field is overwritten.

> **Note:** Statuses and Timestamp actions function differently. Consider Timestamp actions supplemental — the script will not `Ctrl+A` the current text box if you solely use the Timestamp functionality.

## Offset Format

All actions accept an optional `+` or `-` offset suffix. The offset can be written as:

| Format                       | Meaning                 |
| ------------------------------| -------------------------|
| `+N` / `-N`  / `+Nm` / `-Nm` | N minutes               |
| `+Ns` / `-Ns`                | N seconds               |
| `+NmNs` / `-NmNs`            | N minutes and N seconds |

### Offset Examples

- `+20`/`+20m` — 20 minutes in the future
- `+30s` — 30 seconds in the future
- `-4m30s` — 4 minutes and 30 seconds in the past

## Supported Timestamp Actions

These actions do not replace the whole field. They paste only the timestamp text at the current cursor position.

- `timestamp`, with any offset suffix

### Timestamp Examples

- `timestamp` — current time
- `timestamp+20` — 20 minutes in the future
- `timestamp-4m30s` — 4 minutes and 30 seconds in the past

### How Discord Timestamp Actions Work

The result is converted into a Discord relative timestamp:

```text
<t:UNIX_TIME:R>
```

When a timestamp action runs, the script:

1. Copies the generated timestamp to the clipboard.
2. Waits briefly.
3. Sends `Ctrl+V`.
4. *(if `-S`)* Waits briefly, then sends `Enter`.

This means the timestamp is inserted at the cursor instead of replacing the field.

## Custom Message Actions

The `-M` flag pastes a freeform message at the current cursor position (no `Ctrl+A`). The message is processed through constructor expansion and variable resolution before pasting.

```bash
python alerts.py -M "your message here"
python alerts.py -M "{ConstructorName}"
python alerts.py -M "{Greetings}, {Introduction}. {Pleasantries}."
python alerts.py -S -M "{DispatchGreeting}"   # paste and submit immediately
```

### Auto-Formatting

After all tokens are resolved, the message is automatically cleaned up:

- The first letter is capitalized.
- The first letter after any sentence-ending punctuation (`. `, `! `, `? `) is capitalized.
- A trailing period is appended if the message does not already end with `.`, `!`, or `?`.

### Custom Message Examples

| Command | Result |
|---------|--------|
| `python alerts.py -M "{FullGreetingQuestionnaire}"` | Greeting + intro + pleasantry + questionnaire prompt, randomly chosen phrases |
| `python alerts.py -M "{FullGreetingMoreInfo}"` | Greeting + intro + pleasantry + request for more info |
| `python alerts.py -M "{GreetingQUpdate}"` | Greeting + intro + ask for update while waiting on a TL |
| `python alerts.py -M "{ThanksUpdate}"` | Random thanks phrase + deliver an update |
| `python alerts.py -M "{ThanksWaitQUpdate}"` | Patience acknowledgement + ask for a queue update |
| `python alerts.py -M "{ApologyWaitUpdate}"` | Apologize for the wait + deliver an update |
| `python alerts.py -M "{ApologyConfusionMoreInfo}"` | Apologize for confusion + ask for more info |
| `python alerts.py -M "{GreetingVitalsCheck}"` | Greeting + intro + ask oxygen and thirst/hunger levels |
| `python alerts.py -M "{GreetingVitalsRadiationCheck}"` | Greeting + intro + ask oxygen, thirst/hunger, and radiation |
| `python alerts.py -M "{VitalsCheck}"` | Ask oxygen and thirst/hunger levels (no greeting, mid-conversation) |
| `python alerts.py -M "{Greetings}, {Introduction}!"` | e.g. "Hey, I'm YourName!" |
| `python alerts.py -M "hello"` | "Hello." (capitalized, period appended) |
| `python alerts.py -M "Anything you want."` | Pasted as-is (already ends with punctuation) |

## Internal Function Overview

### `_resolve_os`

`_resolve_os() -> str`

Determines which clipboard/input backend to use.

- Reads `OS_MODE` from `Settings.py`.
- If `OS_MODE` is `"linux"` or `"windows"`, returns that value immediately — `platform` is never imported.
- If `OS_MODE` is `"auto"`, imports `platform` at call time and inspects `platform.system()`.
- Raises `RuntimeError` for any unsupported OS detected under `"auto"` mode.

### `_clipboard_paste`

`_clipboard_paste(text, *, replace, send=False, delay=0.1) -> None`

OS-aware clipboard dispatcher. Calls `_resolve_os()` and routes to the appropriate backend.

- `replace=True` — sends `Ctrl+A` before pasting, overwriting the current field (used by status actions).
- `replace=False` — pastes at the cursor without selecting anything (used by timestamp and custom message actions).
- `send=True` — sends `Enter` after the paste, submitting the message immediately (enabled by the `-S` flag).

#### `_clipboard_paste_linux`

`_clipboard_paste_linux(text, *, replace, send=False, delay=0.1) -> None`

Linux backend. Copies `text` to the Wayland clipboard via `wl-copy` and sends keystrokes via `ydotool`.

#### `_clipboard_paste_windows`

`_clipboard_paste_windows(text, *, replace, send=False, delay=0.1) -> None`

Windows backend stub. Raises `NotImplementedError` until implemented. Planned: `win32clipboard` or `ctypes SetClipboardData` for the clipboard, `ctypes SendInput` or `pyautogui` for `Ctrl+A` / `Ctrl+V` / `Enter`.

### `build_status`

`build_status(case_name) -> str`

Builds the full output string for a named status action.

- Uses the current timestamp from `build_timestamp()`
- Appends that timestamp to the selected emoji template
- Raises an error if the action name is unknown

### `build_timestamp`

`build_timestamp(offset_seconds=0) -> str`

Builds the Discord relative timestamp suffix.

- Uses the current Unix time
- Applies any provided offset in seconds
- Returns a string in the format `<t:...:R>`

### `build_timestamp_action`

`build_timestamp_action(action) -> str | None`

Parses timestamp commands.

- `timestamp` returns the current timestamp
- `timestamp+N` returns a future timestamp
- `timestamp-N` returns a past timestamp
- Returns `None` if the action is not a timestamp action

### `parse_offset_action`

`parse_offset_action(action, prefix) -> tuple[str, int] | None`

Parses commands that allow an optional signed time offset.

- `prefix` matches the base action name with no offset
- Accepts `+N`, `+Nm`, `+Ns`, `+NmNs` (and `-` equivalents) — result is always in seconds
- Bare `+N` / `-N` with no unit is treated as minutes for backwards compatibility
- Returns `None` when the action does not match the expected pattern

### `resolve_message`

`resolve_message(text) -> str`

Resolves a freeform `-M` message string.

- **Constructor pass:** expands any `{ConstructorName}` tokens using `MESSAGE_CONSTRUCTORS` (case-insensitive).
- **Variable pass (×2):** replaces every `{VarName}` token using `MESSAGE_VARIABLES`; list values are randomly chosen. A second pass runs immediately after to resolve any variable tokens that appeared *inside* a variable value — for example, `{Name}` embedded in an `{Introduction}` phrase.
- Unknown token names are left unchanged.
- Capitalizes the first letter of the message.
- Capitalizes the first letter after sentence-ending punctuation.
- Appends a trailing period if the message has no closing punctuation.

### `main`

`main() -> int`

The CLI entry point.

- Strips the optional `-S` flag from the argument list and sets `send=True` if present
- If `-M "message"` is given, resolves and pastes the custom message
- Otherwise, detects whether the single argument is a timestamp action or a status action
- Passes `send` through to `_clipboard_paste` so Enter fires when requested
- Prints any error to stderr and exits with status `1`

## Quick Reference

| Invoker | Script | Action | Result |
|---------|--------|--------|--------|
| `python` | `alerts.py` | `rtb` | RTB status, current time — replaces field |
| `python` | `alerts.py` | `rtb+20` | RTB status, +20 min — replaces field |
| `python` | `alerts.py` | `rtb+4m30s` | RTB status, +4m 30s — replaces field |
| `python` | `alerts.py` | `active_alert` | Active alert status, current time — replaces field |
| `python` | `alerts.py` | `active_alert-10` | Active alert status, −10 min — replaces field |
| `python` | `alerts.py` | `active_alert-4m30s` | Active alert status, −4m 30s — replaces field |
| `python` | `alerts.py` | `sb1` | SB1 status, current time — replaces field |
| `python` | `alerts.py` | `sb3-5` | SB3 status, −5 min — replaces field |
| `python` | `alerts.py` | `timestamp` | Relative timestamp, now — inserted at cursor |
| `python` | `alerts.py` | `timestamp+20` | Relative timestamp, +20 min — inserted at cursor |
| `python` | `alerts.py` | `timestamp-4m30s` | Relative timestamp, −4m 30s — inserted at cursor |
| `python` | `alerts.py` | `-M "{FullGreetingQuestionnaire}"` | Greeting + intro + questionnaire — inserted at cursor |
| `python` | `alerts.py` | `-M "{GreetingQUpdate}"` | Greeting + intro + queue update ask — inserted at cursor |
| `python` | `alerts.py` | `-M "{ApologyWaitUpdate}"` | Apology for wait + update delivery — inserted at cursor |
| `python` | `alerts.py` | `-M "{GreetingVitalsCheck}"` | Greeting + intro + oxygen and thirst/hunger check — inserted at cursor |
| `python` | `alerts.py` | `-M "{GreetingVitalsRadiationCheck}"` | Greeting + intro + full vitals + radiation check — inserted at cursor |
| `python` | `alerts.py` | `-M "{Greetings}, {Introduction}!"` | Custom greeting with name — inserted at cursor |
| `python` | `alerts.py` | `-M "Any freeform text."` | Freeform message — inserted at cursor |
| `python` | `alerts.py` | `-S active_alert` | Active alert status — replaces field and submits |
| `python` | `alerts.py` | `-S -M "{DispatchGreeting}"` | Dispatch greeting — inserted at cursor and submits |
| `python` | `alerts.py` | `-S -M "{FullGreetingQuestionnaire}"` | Full greeting — inserted at cursor and submits |

---

```bash
python alerts.py active_alert-4m30s
```

Pastes the full active alert emoji string with a Discord relative timestamp set 4 minutes and 30 seconds in the past, overwriting the current input field via `Ctrl+A` + `Ctrl+V`.

```bash
python alerts.py -M "{FullGreetingQuestionnaire}"
```

Expands the `FullGreetingQuestionnaire` constructor, resolves all `{Variable}` tokens with randomly selected values, auto-formats the result, and pastes it at the current cursor position.
