import re

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def is_email(email):
    if(re.fullmatch(email_regex, email)):
        return True
    else:
        return False

# text = 'taipm@bidv.com.vn'
# print(is_email(text))

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

# stock_regex = ('[a-zA-Z]')
# def is_stock_quick(text):
#     p = re.compile(url_regex)
#     if (text == None):
#         return False
#     if(re.search(p, text)):
#         return True
#     else:
#         return False
# text = 'VND'
# print(is_stock_quick(text))
# text = 'https://www.geeksforgeeks.org/check-if-an-url-is-valid-or-not-using-regular-expression/?ref=rp'
# print(is_url(text))