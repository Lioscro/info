OUTLETS = [
    'cv',
    'resume',
    'web',
]

ALL_ACTIVE = {
    outlet: True for outlet in OUTLETS
}

ALL_INACTIVE = {
    outlet: False for outlet in OUTLETS
}

ONLY_WEB = {
    'cv': False,
    'resume': False,
    'web': True,
}

NOT_RESUME = {
    'cv': True,
    'resume': False,
    'web': True,
}
