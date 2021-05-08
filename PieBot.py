from functions import *

# Kill the script if the API key and API secret aren't defined
if not API_KEY and API_SECRET:
    print(colored(".env is missing your API key and secret", "red"))
    sys.exit()

# Kill the script if no environment has been defined
if not ENVIRONMENT:
    print(colored(".env is missing a defined environment. This should either be 'production' or 'dev'", "red"))
    sys.exit()
