# YASDADDY Guide

## Yet Another Stream Deck Alert Developed for Dispatchers with Ydotool 

`alerts.py` is a small helper script targetged adt Linux users that builds a Discord-formatted alert string, copies it to the clipboard with `wl-copy`, and pastes it with `ydotool`.

Personally, I use this with a Stream Deck, but you can use whatever you want as long as it can run a python script. I made this script with multi-interface usages in mind.

## What It Does

The script supports two kinds of actions:

1. Status actions
   These build a full alert/status string and replace the current field contents with `Ctrl+A` + paste.
   They can also include a `+N` or `-N` suffix to offset the timestamp.

2. Timestamp actions
   These build only the Discord relative timestamp suffix and paste it at the current cursor position without `Ctrl+A`.

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

## Usage

```bash
python alerts.py <action>
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

Statuses and Timestamp actions function differently. Consider Timestamp actions suplimental, so the script will not overwrite `Ctrl+A/Ctrl+V` whatever is in the current text box if you soley use the Timestamp functionality.



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

### `_clipboard_paste(text, *, replace, delay=0.1)`

Copies `text` to the Wayland clipboard and pastes it.

- `replace=True` — sends `Ctrl+A` before pasting, overwriting the current field (used by status actions)
- `replace=False` — pastes at the cursor without selecting anything (used by timestamp actions)

### `main()`

The CLI entry point.

- Reads the single command-line argument
- Detects whether it is a timestamp action or a status action
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

---

```bash
python alerts.py active_alert-4m30s
```

Pastes the full active alert emoji string with a Discord relative timestamp set 4 minutes and 30 seconds in the past, overwriting the current input field via `Ctrl+A` + `Ctrl+V`.
