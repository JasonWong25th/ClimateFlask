# Scopes are what google calls the privleges necessary to do certain things.
# These scopes are communicated to the user when they log in to the app.
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.

# For a thorough description of how to do stuff, go to the feedback.py file.

SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
    ]
 