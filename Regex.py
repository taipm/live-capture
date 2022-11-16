import re

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def is_email(email):
    if(re.fullmatch(email_regex, email)):
        return True
    else:
        return False
        
url_regex = ("((http|https)://)(www.)?" +
        "[a-zA-Z0-9@:%._\\+~#?&//=]" +
        "{2,256}\\.[a-z]" +
        "{2,6}\\b([-a-zA-Z0-9@:%" +
        "._\\+~#?&//=]*)")
    
def is_url(str):
    p = re.compile(url_regex)
    if (str == None):
        return False
    if(re.search(p, str)):
        return True
    else:
        return False