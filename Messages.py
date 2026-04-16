# Built-in message constructors and variables.
# This file ships with the repository and will be overwritten on updates.
# To add or override any entry without losing your changes, use CustomMessages.py.

# Constructors are shorthands that expand into a full template string before variables are resolved.
# Use {ConstructorName} in your -M string to expand a constructor.
# Constructor values may contain {VarName} tokens — they are resolved in the normal variable pass.
# IMPORTANT: Do NOT end constructor templates with punctuation; let the auto-formatter handle it,
# OR include your own closing punctuation (e.g. "?") directly in the template string.

MESSAGE_CONSTRUCTORS: dict[str, str] = {
    #Some basic constructors to get you started, but feel free to customize these as much as you'd like inside of the CustomMessages.py file! You can also add more constructors for different scenarios.
    # Greeting openers
    "FullGreetingQuestionnaire": "{Greetings}, {Introduction}, {Pleasantries}. {Questionnaire}.",
    "FullGreetingStranded": "{Greetings}, {Introduction}. I see that you are stranded in space. {SpaceVitalsCheck}?",
    "FullGreetingStrandedRadiation": "{Greetings}, {Introduction}. I see that you are stranded in space. {SpaceVitalsRadiationCheck}?",
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
    "VitalsRadiationCheck":          "{ThirstHunger}? {Radiation}?",
    "SpaceVitalsCheck":              "{OxygenLevel}? {ThirstHunger}?",
    "SpaceVitalsRadiationCheck":     "{OxygenLevel}? {ThirstHunger}? {Radiation}?",


    # --- Legacy Medrunner canned responses (L-prefix = verbatim originals) ---

    # Opening / intake
    "LWelcomeQuestionnaire":       "Thank you for choosing Medrunner Services!\n\nOnce the Questionnaire has been submitted we can proceed.",
    "LQuestionnaireReminder":      "Could you please fill in the Questionnaire?\nIf you have already, be sure to press submit for I don't see them.",
    "LLeaderGreeting":           "Hello! My name is {Name}, and I'll be leading the team dispatched to your location.\n\nI will be sending you a friend request and/or party invite.\n(To accept the invite, make sure you're in first-person view and spam the key to the right of P — typically the [ key - though it may vary depending on your keyboard layout.)\n\nPlease confirm here when you are ready to receive the invites!",
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
    "QuestionnaireReminder":      "{Questionnaire}.\nIf you have already, be sure to press submit for I don't see them.",
    "LeaderGreeting":           "{Greetings}! {Introduction}, and {TeamLeadIntro}.\n\n{LeaderSendingInvites}.\n(To accept the invite, make sure you're in first-person view and spam the key to the right of P — typically the [ key - though it may vary depending on your keyboard layout.)",
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

    # Quick shorthands
    "QuickGreeting":  "{Greetings}! {Introduction}.",
    "BriefUpdate":    "{AUpdate}! {TeamEnRoute}. {ArrivalNotice}.",
    "ServerFull":     "{AUpdate}! {TeamEnRoute}. {ArrivalNotice}. {ApologiesWait} — your server is full, there may be a short delay.",
    "VitalsFollowUp": "{ThanksWait}. Before we proceed — {OxygenLevel}? {ThirstHunger}?",
    "ClosingThanks":  "{ThanksWait}! {ServiceWelcome} — we hope to assist you again in the future.",

    # Closing
    "CloseSuccess": "{ThanksWait}! As we conclude our service, we'd like to sincerely thank you for trusting us. We hope today's response was prompt, professional, and met your expectations. Your health and satisfaction are our top priorities, and we hope to assist you again in the future if needed.\n\nIf you have a moment, we'd greatly appreciate it if you could leave a rating and comment on the alert card to let us know how we did today!",
    "CloseFailure": "{ApologiesFrustration}. As we conclude our service, we'd like to sincerely thank you for trusting us. We're sorry that we were unable to rescue you this time. Your health and satisfaction are our top priorities, and we hope that we will be able to assist you in the future if needed.\n\nIf you have a moment, we'd greatly appreciate it if you could leave a rating and comment on the alert card to let us know how we handled your case today!",
    "CloseNeutral": "{ApologiesInconvenience}. As we conclude our service, we'd like to sincerely thank you for trusting us. We're sorry that we were unable to rescue you this time. Your health and satisfaction are our top priorities, and we hope that we will be able to assist you in the future if needed.\n\nUntil then, we wish you safe travels in the 'Verse.",
}

# Variables used in custom messages via the -M flag.
# Use {VarName} in your message string to insert a variable.
# Example: alerts.py -M "{Greetings}, {Introduction}, {Pleasantries}. {Questionnaire}."
# Or using a constructor shorthand: alerts.py -M "{FullGreetingQuestionnaire}"
#
# IMPORTANT: Do NOT end variable values with punctuation (no commas, periods, etc.).
# Punctuation and spacing belong in your -M template string (or constructor), not in the values below.
# The auto-formatter will capitalize the first letter and add a trailing period if needed.
# List values are randomly selected each time; plain strings are always used as-is.
MESSAGE_VARIABLES: dict[str, str | list[str]] = {
    "Greetings": [
        "Hey there",
        "Hello",
        "Hi",
        "Good day",
        "Greetings",
        "Hey",
    ],
    "Introduction": [
        "my name is {Name}",  # {Name} is resolved at message-build time
        "I'm {Name}",
        "the name's {Name}",
        "you can call me {Name}",
        "I go by {Name}",
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
    "DispatchIntro": [
        "I'll be your dispatcher for this alert",
        "I'm handling dispatch for your alert today",
        "I'll be coordinating your rescue",
    ],
    "TeamLeadIntro": [
        "I'll be the team lead for this alert",
        "I'll be leading the rescue efforts for your alert",
    ],
    "DispatchSendingInvites": [
        "the team leader will be sending you a friend request and/or party invite",
        "your team leader will reach out via friend request and party invite",
        "expect a friend request and party invite from the team leader shortly",
        "the team leader will send you a friend request followed by a party invite",
    ],
    "LeaderSendingInvites": [
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
    "ContactAgain": [
        "don't hesitate to reach out if you ever need us again",
        "feel free to contact us again anytime you need assistance",
        "we're always here if you need us again",
        "should you ever need our services again, don't hesitate to get in touch",
        "if you ever find yourself in need again, we're just an alert away",
        "remember, we're always available if you need us again",
    ],
    "Signoff": [
        "stay safe out there",
        "fly safe",
        "safe travels in the 'Verse",
    ],
}
