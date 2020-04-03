# The "main.py" file is the file that you actually run to make the whole app work.

from app import app
import os

if __name__ == "__main__":
    
    # This line is a way to not use https. leave it commented out unless you have a problem
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    # This line lets you run using a fake version of https for a local computer 
    # You must use https to login to google
    app.run(debug="True", ssl_context='adhoc')