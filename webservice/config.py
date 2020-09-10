import web
web.config.cache = False
web.config.debug = False

# 16 character strings, alpha upper and lower, and digits, no special chars
allowed = (
    ('planet',        'booty'),
    )
