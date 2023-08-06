if __name__ == "__main__":
    print("Hey, this script is just an example! DO NOT RUN IT DIRECTLY!")
    __import__("sys").exit(1)

import mwng as mw

# Select Chinese Wikipedia
# URL: https://zh.wikipedia.org/w/api.php
site = mw.WMSites.wp("zh")

# Create the API object
API = mw.API(site)

# Login, we have a function to do this complex job
# Remember to use a [[Special:Botpasswords]] instead of your own password.
# As from MediaWiki 1.27 password login is no longer supported
# And we have no plan to introduce clientlogin; you have to do it yourself.
API.login("username","botpassword")

# Edit! You can let the script to generate the token and request body
API.edit("A-TESTING-PAGE","TESTING-REPLACING-CONTENT")

# Or supplying your own body
API.edit("A-TESTING-PAGE",{"appendtext":"CUSTOM-APPEND-TEXT"})

# You can supply your own token!
token, ts = API.csrf()
API.edit("A-TESTING-PAGE","TESTING-REPLACING-CONTENT",token,ts)

# In case there's an error...
try:
    API.login("INVALID-USER","INVALID-PASSWORD-1234")
except MWAPIError as e:
    print(e.codes) # List of error codes
    print(e.dump) # The original JSON message
    raise

# That's all for now! You can always use API.[get,post] to do custom requests!
