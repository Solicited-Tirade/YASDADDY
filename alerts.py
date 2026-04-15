# Import standard library modules for CLI input, timestamps, and shell commands.
import re
import sys
import time
import random
import subprocess

# Matches an offset like "4m30s", "4m", "30s", or a bare integer (legacy minutes).
_OFFSET_RE = re.compile(r"^(?:(\d+)m)?(?:(\d+)s)?$")

###Initialization Components###

# IMPORTANT: Set to False to strip the animated Nitro-only emojis from ACTIVE_ALERT_TEMPLATE. If you do not have Nitro, this will not work well for you.
USE_NITRO_EMOJI = True

# Your name, used in {Introduction} and anywhere else NAME is referenced.
NAME = "YourName"

# Constructors are shorthands that expand into a full template string before variables are resolved.
# Use {ConstructorName} in your -M string to expand a constructor.
# Constructor values may contain {VarName} tokens — they are resolved in the normal variable pass.
# IMPORTANT: Do NOT end constructor templates with punctuation; let the auto-formatter handle it,
# OR include your own closing punctuation (e.g. "?") directly in the template string.
# Use MESSAGE_CONSTRUCTORS as your personal toolkit to build out exactly what you want to say to a client. For example: Lets say that you have a stranded in Space alert.
# You can have a "Stranded" button/function that will construct a question about their oxygen levels.
# How about if the client is at Onyx? Well, then you can have a MESSAGE_CONSTRUCTORS dictionary that constructs a question about radiation and what you're able to do for the client

MESSAGE_CONSTRUCTORS: dict[str, str] = {
    #Some basic constructors to get you started, but feel free to customize these as much as you'd like! You can also add more constructors for different scenarios.
    # Greeting openers
    "FullGreetingQuestionnaire": "{Greetings}, {Introduction}, {Pleasantries}. {Questionnaire}?",
    "FullGreetingStranded": "{Greetings}, {Introduction}. I see that you are stranded in space. Can you provide me with your oxygen and thirst levels?",
    "FullGreetingMoreInfo": "{Greetings}, {Introduction}, {Pleasantries}. {Moreinfo}",
    "GreetingQUpdate": "{Greetings}, {Introduction}. {QUpdate}",

    # Thank → follow-up
    "ThanksMoreInfo": "{Thanks}, {Moreinfo}",
    "ThanksUpdate": "{Thanks}. {AUpdate}",
    "ThanksWaitQUpdate": "{ThanksWait}. {QUpdate}",
    "ThanksWaitMoreInfo": "{ThanksWait}. {Moreinfo}",

    # Apology → follow-up
    "ApologyWaitQUpdate": "{ApologiesWait}. {QUpdate}",
    "ApologyWaitUpdate": "{ApologiesWait}. {AUpdate}",
    "ApologyInconvenienceMoreInfo": "{ApologiesInconvenience}. {Moreinfo}",
    "ApologyFrustrationMoreInfo": "{ApologiesFrustration}. {Moreinfo}",
    "ApologyConfusionMoreInfo": "{ApologiesConfusion}. {Moreinfo}",

    # Vitals checks
    "VitalsCheck":                  "{OxygenLevel}? {ThirstHunger}?",
    "VitalsRadiationCheck":         "{OxygenLevel}? {ThirstHunger}? {Radiation}?",
    "GreetingVitalsCheck":          "{Greetings}, {Introduction}. {OxygenLevel}? {ThirstHunger}?",
    "GreetingVitalsRadiationCheck": "{Greetings}, {Introduction}. {OxygenLevel}? {ThirstHunger}? {Radiation}?",

    # --- Legacy Medrunner canned responses (L-prefix = verbatim originals) ---

    # Opening / intake
    "LWelcomeQuestionnaire":       "Thank you for choosing Medrunner Services!\n\nOnce the Questionnaire has been submitted we can proceed.",
    "LQuestionnaireReminder":      "Could you please fill in the Questionnaire?\nIf you have already, be sure to press submit for I don't see them.",
    "LDispatchGreeting":           "Hello! My name is {Name}, and I'll be leading the team dispatched to your location.\n\nI will be sending you a friend request and/or party invite.\n(To accept the invite, make sure you're in first-person view and spam the key to the right of P — typically the [ key - though it may vary depending on your keyboard layout.)\n\nPlease confirm here when you are ready to receive the invites!",
    "LNoTeamsAvailable":           "Thank you for choosing Medrunner Services!\n\nWe've received your alert — no need to worry. All active teams are currently deployed, but one will be assigned to you shortly.\nIn the meantime, if you haven't already, please complete and submit the questionnaire.\n\nThank you for your patience!",
    "LInviteConfirmationReminder": "Please let me know when you are ready to receive the invites!",

    # No contact
    "LNoContactWarning":   "Just as fair warning, if we haven't heard from you within the next 5 minutes, we will hope all is well and close this alert.",
    "LNoContactStanddown": "Standing down due to no contact. You're welcome to resubmit, but please know that you will need to be ready to accept friend and party invites and answer the questions in order for us to respond.",

    # Friend request issues
    "LFriendRequestCheckKey": "Hmm it was not accepted, is your default accept key the Left Bracket [ ?",
    "LFriendRequestBugged":   "The Friend Request has bugged, this is a known problem.\nPlease can you navigate to https://robertsspaceindustries.com/spectrum to accept the Friend Request.\n\nPlease confirm here once you have accepted it.",

    # Invites & joining
    "LFriendRequestSent":   "Friend Request sent, please spam the accept key!",
    "LPartyInviteSent":     "Party Invite sent, please spam the accept key!",
    "LJoiningServer":       "Perfect! Our Team is joining your Server now. I will notify you when we are en route.",
    "LJoiningServerFull":   "Perfect! Our Team is joining your Server now. I will notify you when we are en route.\nDo note your server is full, there may be a short delay. I apologize for this in advance.",
    "LLoadingInForFriends": "I will get your friend(s) in the party as well. Please provide me a moment to load into the server.",

    # Deploying
    "LCanInviteFriends": "I can now invite your friend(s) to the party. Please confirm here when they are ready to accept.",
    "LNoPartyMarker":    "We sadly do not have your party marker.\n\nCould you please open up your console, type r_displayinfo 2, close the console, and send me a screenshot of your screen with the info at the top right visible?\n\nUpload it to https://imgur.com/upload and drop the link here.",
    "LDeployMoreInfo":   "To help ensure we provide an efficient service, please answer the following 2 questions:\n\n1) Will you be needing to use our Medical Bed?\n2) Will you be needing an Extraction to the Closest Station?",
    "LEnRoute":          "Our Team is en route. I will update you when we are shortly arriving.",
    "LShortlyArriving":  "Depending on the situation, we may not pick you up immediately. Please be patient while we secure the area.\n\nWe will reach you soon. Switching over to in-game party chat now.\nNote: If you are downed, it will be harder to read until you are revived.",

    # Closing
    "LCloseSuccess": "As we conclude our service, we'd like to sincerely thank you for trusting us. We hope today's response was prompt, professional, and met your expectations. Your health and satisfaction are our top priorities, and we hope to assist you again in the future if needed.\n\nIf you have a moment, we'd greatly appreciate it if you could leave a rating and comment on the alert card to let us know how we did today!",
    "LCloseFailure": "As we conclude our service, we'd like to sincerely thank you for trusting us. We're sorry that we were unable to rescue you this time. Your health and satisfaction are our top priorities, and we hope that we will be able to assist you in the future if needed.\n\nIf you have a moment, we'd greatly appreciate it if you could leave a rating and comment on the alert card to let us know how we handled your case today!",
    "LCloseNeutral": "As we conclude our service, we'd like to sincerely thank you for trusting us. We're sorry that we were unable to rescue you this time. Your health and satisfaction are our top priorities, and we hope that we will be able to assist you in the future if needed.\n\nUntil then, we wish you safe travels in the 'Verse.",

    # --- Medrunner canned responses with variable flair ---

    # Opening / intake
    "WelcomeQuestionnaire":       "{ServiceWelcome}!\n\n{Questionnaire}.",
    "QuestionnaireReminder":      "{Questionnaire}?\nIf you have already, be sure to press submit for I don't see them.",
    "DispatchGreeting":           "{Greetings}! {Introduction}, and {StandingBy}.\n\n{SendingInvites}.\n(To accept the invite, make sure you're in first-person view and spam the key to the right of P — typically the [ key - though it may vary depending on your keyboard layout.)\n\n{ReadyForInvites}!",
    "NoTeamsAvailable":           "{ServiceWelcome}!\n\n{Received} — {Assurances}. All active teams are currently deployed, but one will be assigned to you shortly.\nIn the meantime, if you haven't already, please complete and submit the questionnaire.\n\n{ThanksWait}!",
    "InviteConfirmationReminder": "{ThanksWait}! {ReadyForInvites}.",

    # No contact
    "NoContactWarning":   "{ThanksWait}. Just as fair warning, {NoContactClose}.",
    "NoContactStanddown": "{ApologiesInconvenience}. {StandingDown}. You're welcome to resubmit, but please know that you will need to be ready to accept friend and party invites and answer the questions in order for us to respond.",

    # Friend request issues
    "FriendRequestCheckKey": "{ApologiesInconvenience}. It was not accepted — is your default accept key the Left Bracket [ ?",
    "FriendRequestBugged":   "{ApologiesInconvenience}. The Friend Request has bugged, this is a known problem.\nPlease can you navigate to https://robertsspaceindustries.com/spectrum to accept the Friend Request.\n\nPlease confirm here once you have accepted it.",

    # Invites & joining
    "FriendRequestSent":   "{AUpdate}! A Friend Request has been sent — {SpamAcceptKey}!",
    "PartyInviteSent":     "{AUpdate}! A Party Invite has been sent — {SpamAcceptKey}!",
    "JoiningServer":       "{AUpdate}! Our Team is joining your Server now. {ArrivalNotice}.",
    "JoiningServerFull":   "{AUpdate}! Our Team is joining your Server now. {ArrivalNotice}.\nDo note your server is full, there may be a short delay. {ApologiesWait}.",
    "LoadingInForFriends": "{ThanksWait}! I will get your friend(s) in the party as well. Please give me a moment to load into the server.",

    # Deploying
    "CanInviteFriends": "{AUpdate}! I can now invite your friend(s) to the party. Please confirm here when they are ready to accept.",
    "NoPartyMarker":    "{ApologiesInconvenience}. We do not have your party marker.\n\nCould you please open up your console, type r_displayinfo 2, close the console, and send me a screenshot of your screen with the info at the top right visible?\n\nUpload it to https://imgur.com/upload and drop the link here.",
    "DeployMoreInfo":   "{Moreinfo}. To help ensure we provide an efficient service, please answer the following 2 questions:\n\n1) Will you be needing to use our Medical Bed?\n2) Will you be needing an Extraction to the Closest Station?",
    "EnRoute":          "{AUpdate}! {TeamEnRoute}. {ArrivalNotice}.",
    "ShortlyArriving":  "{AUpdate}! Depending on the situation, we may not pick you up immediately. {SecuringArea}.\n\nWe will reach you soon. Switching over to in-game party chat now.\nNote: If you are downed, it will be harder to read until you are revived.",

    # Closing
    "CloseSuccess": "{ThanksWait}! As we conclude our service, we'd like to sincerely thank you for trusting us. We hope today's response was prompt, professional, and met your expectations. Your health and satisfaction are our top priorities, and we hope to assist you again in the future if needed.\n\nIf you have a moment, we'd greatly appreciate it if you could leave a rating and comment on the alert card to let us know how we did today!",
    "CloseFailure": "{ApologiesFrustration}. As we conclude our service, we'd like to sincerely thank you for trusting us. We're sorry that we were unable to rescue you this time. Your health and satisfaction are our top priorities, and we hope that we will be able to assist you in the future if needed.\n\nIf you have a moment, we'd greatly appreciate it if you could leave a rating and comment on the alert card to let us know how we handled your case today!",
    "CloseNeutral": "{ApologiesInconvenience}. As we conclude our service, we'd like to sincerely thank you for trusting us. We're sorry that we were unable to rescue you this time. Your health and satisfaction are our top priorities, and we hope that we will be able to assist you in the future if needed.\n\nUntil then, we wish you safe travels in the 'Verse.",
}

# Variables used in custom messages via the -M flag.
# Use {VarName} in your message string to insert a variable.
# Example: alerts.py -M "{Greetings}, {Introduction}, {Pleasantries}. {Questionnaire}?"
# Or using a constructor shorthand: alerts.py -M "{FullGreetingQuestionnaire}"
#
# IMPORTANT: Do NOT end variable values with punctuation (no commas, periods, etc.).
# Punctuation and spacing belong in your -M template string (or constructor), not in the values below.
# The auto-formatter will capitalize the first letter and add a trailing period if needed.
# List values are randomly selected each time; plain strings are always used as-is.
MESSAGE_VARIABLES: dict[str, str | list[str]] = {
    "Name": NAME,  # plain string — always resolves to the configured NAME
    "Greetings": [
        "Hey there",
        "Hello",
        "Hi",
        "Good day",
        "Greetings",
        "Hey",
    ],
    "Introduction": [
        f"my name is {NAME}",
        f"I'm {NAME}",
        f"the name's {NAME}",
        f"you can call me {NAME}",
        f"I go by {NAME}",
    ],
    "Pleasantries": [
        "I hope you're having a great day",
        "I'm here to help",
        "hope all is well",
        "I hope everything is going well for you",
    ],
    "Questionnaire": [
        "please take a moment to fill out the questionnaire",
        "please fill out the questionnaire",
        "if you have a moment, please fill out the questionnaire",
    ],
    "QUpdate": [
        "can you provide me with an update while we wait for a team leader to grab this alert",
        "while we wait for a team leader, could you give me an update on the situation",
        "do you have any updates for me while we wait for a team leader to pick this up",
    ],
    "Moreinfo": [
        "sorry to ask, but could you provide me with some more information",
        "I'm going to need some more details from you",
        "to better assist you, I'll need a little more information",
    ],
    "AUpdate": [
        "good news, I have an update for you",
        "I have an update",
        "I've got some news for you",
        "just wanted to let you know, I have an update",
    ],
    "Thanks": [
        "thanks",
        "thank you",
        "I appreciate that",
        "I appreciate it",
        "thank you very much",
        "much appreciated",
    ],
    "ThanksWait": [
        "thank you for your patience and cooperation",
        "I sincerely appreciate your patience",
        "thank you for your time and understanding",
        "your patience is greatly appreciated",
        "I appreciate your continued cooperation",
        "thank you for bearing with us",
    ],
    "ApologiesWait": [
        "I'm sorry for the delay",
        "please accept my apologies for the wait",
        "I apologize for the hold",
        "I'm sorry to keep you waiting",
        "thank you for your patience, and I apologize for the wait",
        "I'm sorry for the extended wait time",
    ],
    "ApologiesInconvenience": [
        "I apologize for the inconvenience",
        "I sincerely apologize for any inconvenience this may have caused",
        "I'm sorry for the inconvenience this has caused you",
        "please accept my sincerest apologies for the inconvenience",
        "I apologize for any inconvenience on our end",
    ],
    "ApologiesFrustration": [
        "I apologize for any frustration this may have caused",
        "I'm sorry for any frustration on your end",
        "I understand this may be frustrating, and I sincerely apologize",
        "I apologize if this has been a frustrating experience",
        "I'm sorry for the frustration this situation may have caused you",
    ],
    "ApologiesConfusion": [
        "I'm sorry for any confusion",
        "I apologize for any confusion this may have caused",
        "I'm sorry if that was unclear",
        "I apologize for the miscommunication",
        "I'm sorry for any misunderstanding on our end",
        "I apologize if we were not clear, allow me to clarify",
    ],
    "OxygenLevel": [
        "what are your current oxygen levels",
        "can you tell me your current oxygen level",
        "how are your oxygen levels looking",
        "what is your oxygen level sitting at right now",
        "could you share your current oxygen level with me",
    ],
    "Radiation": [
        "are you currently in a radiation zone",
        "is there any radiation in your current area",
        "are you experiencing any radiation exposure at your current location",
        "can you confirm whether you are in a radiation zone",
        "do you have any radiation in your current area",
    ],
    "ThirstHunger": [
        "what are your current thirst and hunger levels",
        "can you give me your thirst and hunger levels",
        "how are your thirst and hunger levels looking",
        "could you share your thirst and hunger levels with me",
        "what are your hunger and thirst levels sitting at right now",
    ],
    # Medrunner operational phrases
    "ServiceWelcome": [
        "thank you for choosing Medrunner Services",
        "thanks for reaching out to Medrunner",
        "welcome to Medrunner Services",
        "thank you for contacting Medrunner",
        "glad you reached out to Medrunner Services",
    ],
    "Received": [
        "we've received your alert",
        "your alert has been received",
        "we've got your alert",
        "we have your alert",
    ],
    "Assurances": [
        "no need to worry",
        "you're in good hands",
        "help is on the way",
        "we've got you covered",
        "rest assured, we're on it",
        "you're in safe hands",
    ],
    "StandingBy": [
        "I'll be your dispatcher for this alert",
        "I'm handling your dispatch today",
        "I'll be coordinating your rescue",
    ],
    "SendingInvites": [
        "the team leader will be sending you a friend request and/or party invite",
        "your team leader will reach out via friend request and party invite",
        "expect a friend request and party invite from the team leader shortly",
        "the team leader will send you a friend request followed by a party invite",
    ],
    "ReadyForInvites": [
        "please let me know when you are ready to receive the invites",
        "let me know when you're ready for the invites",
        "give me the go-ahead when you're ready for the invites",
        "confirm here once you're ready to receive the invites",
        "just say the word when you're ready for the invites",
    ],
    "SpamAcceptKey": [
        "please spam the accept key",
        "keep tapping the accept key until it goes through",
        "spam your accept key to accept",
        "hit the accept key repeatedly until it goes through",
        "mash that accept key",
    ],
    "TeamEnRoute": [
        "our team is en route",
        "our team is on their way to you",
        "the team is headed your way",
        "we're on our way to your location",
    ],
    "ArrivalNotice": [
        "I will update you when we are shortly arriving",
        "I'll keep you posted as we get close",
        "I'll update you once we're nearly there",
        "expect an update from me as we approach your location",
    ],
    "SecuringArea": [
        "please be patient while we secure the area",
        "give us a moment to secure the situation",
        "hold tight while we handle the area",
        "please bear with us as we work to secure the area",
    ],
    "NoContactClose": [
        "if we haven't heard from you within the next 5 minutes, we will hope all is well and close this alert",
        "if there's no response in the next 5 minutes, we'll assume all is well and stand down",
        "should we not hear back within 5 minutes, we'll close this alert and hope you're safe",
        "if we don't receive a response in the next 5 minutes, we'll go ahead and close the alert",
    ],
    "StandingDown": [
        "standing down due to no contact",
        "closing this alert due to no response",
        "we're standing down as we were unable to reach you",
        "standing down — we were unable to make contact",
    ],
}


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
PASTE_KEYS = ["ydotool", "key", "29:1", "47:1", "47:0", "29:0"]  # Ctrl+V


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

    # Direct status templates just append the timestamp.
    if base_name in STATUS_TEMPLATES:
        return STATUS_TEMPLATES[base_name] + timestamp

    # SB statuses use a unique prefix plus the shared SB body and timestamp.
    if base_name in SB_PREFIXES:
        return SB_PREFIXES[base_name] + SB_TEMPLATE + timestamp

    # Show valid options when the user passes an unknown status action.
    valid = sorted([*STATUS_TEMPLATES.keys(), *SB_PREFIXES.keys()])
    raise ValueError(
        f"Unknown status case: {case_name}. Valid cases: {', '.join(valid)}"
    )


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


def _clipboard_paste(text: str, *, replace: bool, delay: float = 0.1) -> None:
    subprocess.run(["wl-copy"], input=text, text=True, check=True)
    time.sleep(delay)
    if replace:
        # Select all existing field contents before pasting.
        subprocess.run(SELECT_ALL_KEYS, check=True)
        time.sleep(delay)
    subprocess.run(PASTE_KEYS, check=True)


def main() -> int:
    # -M "message" pastes a custom message, optionally with {Variable} interpolation.
    if len(sys.argv) == 3 and sys.argv[1] == "-M":
        try:
            message = resolve_message(sys.argv[2])
            _clipboard_paste(message, replace=False)
            return 0
        except Exception as exc:
            print(exc, file=sys.stderr)
            return 1

    # Expect exactly one action argument after the script name.
    if len(sys.argv) != 2:
        print(
            "Usage: python alerts.py <action[+N|-N|+NmNs|-NmNs|+Nm|-Nm|+Ns|-Ns]>\n"
            '       python alerts.py -M "message with optional {Variables}"',
            file=sys.stderr,
        )
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
