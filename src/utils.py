"""

    Utils Funcs archives of Crimson Launcher v1.0 by @devcheckog

"""

import requests

def check_internet() -> bool:

    try:

        requests.get(url= 'https://www.google.com/', timeout= 60, allow_redirects= True)
        return True

    except:
        return False


