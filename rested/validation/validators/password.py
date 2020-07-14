import re


# strong password means: 8 characters, one capital, one number, one lowercase
digits = re.compile('[0-9]')
lowercase = re.compile('[a-z]')
uppercase = re.compile('[A-Z]')

def password(v, accept=None, reject=None):
    if not isinstance(v, str): reject('expected_strong_password')
    strong = digits.search(v) and lowercase.search(v) and uppercase.search(v) and len(v) >= 8
    if not strong : reject('expected_strong_password')
