import re
email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

def email(v, accept=None, reject=None):
    if not isinstance(v, str): reject('expected_email')
    if not email_regex.match(v): reject('expected_email')
