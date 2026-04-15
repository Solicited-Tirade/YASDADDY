# YASDADDY Guide

## Yet Another Stream Deck Alert tool Developed for Dispatchers with Ydotool 

### This tool is agnostic, and can be run without a physical button, if you so choose. It just makes it more convenient. Essentially, you just need something that launches the python script.

`alerts.py` is a small helper script targeted at Linux users that builds a Discord-formatted alert string, copies it to the clipboard with `wl-copy`, and pastes it with `ydotool`.

Personally, I use this with a Stream Deck, but you can use whatever you want as long as it can run a python script. I made this script with multi-interface usages in mind.

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
- `wl-copy`
- `ydotool`

> **Note:** All examples in this guide use `python` for brevity. Substitute the correct invocation for your system (e.g. `python3 alerts.py active_alert`).

## Future Plans

Future plans include adding small API functionality, or OCR to determine who the client is, to perform a `%CLIENT_NAME%` grabbing functionality to personalize messages.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_NITRO_EMOJI` | `True` | Include animated Nitro-only emojis in `active_alert`. Set to `False` if you don't have Discord Nitro. |
| `NAME` | `"YourName"` | Your name, used in the `{Introduction}` variable and anywhere else `NAME` is referenced. |
| `MESSAGE_CONSTRUCTORS` | *(see below)* | Shorthand names that expand into full template strings before variable resolution. |
| `MESSAGE_VARIABLES` | *(see below)* | Named tokens used in `-M` messages. List values are randomly selected; plain strings are always used as-is. |

### Message Constructors

Constructors are named shorthands that expand into a full template string. Use `{ConstructorName}` inside your `-M` string to expand one. They are your personal toolkit — build out exactly the messages you want to send, composed from whatever variables and fixed text fit your style. A constructor can be as simple or as elaborate as you like, and you can add as many as you need.

```python
MESSAGE_CONSTRUCTORS: dict[str, str] = {
    "FullGreetingQuestionnaire": "{Greetings}, {Introduction}, {Pleasantries}. {Questionnaire}?",
    "DispatchGreeting":          "{Greetings}! {Introduction}, and {StandingBy}. {SendingInvites}...",
    "EnRoute":                   "{AUpdate}! {TeamEnRoute}. {ArrivalNotice}.",
    "CloseSuccess":              "{ThanksWait}! As we conclude our service...",
    # ... see MESSAGE_CONSTRUCTORS in alerts.py for the full list
}
```

Constructors are grouped in `alerts.py` as follows:

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
MESSAGE_VARIABLES: dict[str, str | list[str]] = {
    # Identity
    "Name":                   NAME,  # plain string, always resolves to the configured NAME
    # General
    "Greetings":              ["Hey there", "Hello", "Hi", ...],
    "Introduction":           [f"my name is {NAME}", f"I'm {NAME}", ...],
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
python alerts.py <action>
python alerts.py -M "message with optional {Variables}"
```

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

This means the current input field is overwritten.

#### Note

Statuses and Timestamp actions function differently. Consider Timestamp actions supplemental, so the script will not overwrite `Ctrl+A/Ctrl+V` whatever is in the current text box if you solely use the Timestamp functionality.



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

This means the timestamp is inserted at the cursor instead of replacing the field.

## Custom Message Actions (`-M`)

The `-M` flag pastes a freeform message at the current cursor position (no `Ctrl+A`). The message is processed through constructor expansion and variable resolution before pasting.

```bash
python alerts.py -M "your message here"
python alerts.py -M "{ConstructorName}"
python alerts.py -M "{Greetings}, {Introduction}. {Pleasantries}."
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

### `build_status(case_name)`

Builds the full output string for a named status action.

- Uses the current timestamp from `build_timestamp()`
- Appends that timestamp to the selected emoji template
- Raises an error if the action name is unknown

### `build_timestamp(offset_seconds=0)`

Builds the Discord relative timestamp suffix.

- Uses the current Unix time
- Applies any provided offset in seconds
- Returns a string in the format `<t:...:R>`

### `build_timestamp_action(action)`

Parses timestamp commands.

- `timestamp` returns the current timestamp
- `timestamp+N` returns a future timestamp
- `timestamp-N` returns a past timestamp
- Returns `None` if the action is not a timestamp action

### `parse_offset_action(action, prefix)`

Parses commands that allow an optional signed time offset.

- `prefix` matches the base action name with no offset
- Accepts `+N`, `+Nm`, `+Ns`, `+NmNs` (and `-` equivalents) — result is always in seconds
- Bare `+N` / `-N` with no unit is treated as minutes for backwards compatibility
- Returns `None` when the action does not match the expected pattern

### `resolve_message(text)`

Resolves a freeform `-M` message string.

- First pass: expands any `{ConstructorName}` tokens using `MESSAGE_CONSTRUCTORS` (case-insensitive)
- Second pass: replaces every `{VarName}` token using `MESSAGE_VARIABLES`; list values are randomly chosen
- Unknown token names are left unchanged
- Capitalizes the first letter of the message
- Capitalizes the first letter after sentence-ending punctuation
- Appends a trailing period if the message has no closing punctuation

### `_clipboard_paste(text, *, replace, delay=0.1)`

Copies `text` to the Wayland clipboard and pastes it.

- `replace=True` — sends `Ctrl+A` before pasting, overwriting the current field (used by status actions)
- `replace=False` — pastes at the cursor without selecting anything (used by timestamp and custom message actions)

### `main()`

The CLI entry point.

- Reads command-line arguments
- If `-M "message"` is given, resolves and pastes the custom message
- Otherwise, detects whether the single argument is a timestamp action or a status action
- Calls the correct paste function
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

---

```bash
python alerts.py active_alert-4m30s
```

Pastes the full active alert emoji string with a Discord relative timestamp set 4 minutes and 30 seconds in the past, overwriting the current input field via `Ctrl+A` + `Ctrl+V`.

```bash
python alerts.py -M "{FullGreetingQuestionnaire}"
```

Expands the `FullGreetingQuestionnaire` constructor, resolves all `{Variable}` tokens with randomly selected values, auto-formats the result, and pastes it at the current cursor position.
