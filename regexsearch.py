import re



def use_regex(input_text):
    pattern = re.compile(r'<meta name="DC\.identifier" content="(?:[^\\"]|\\\\|\\")*">', re.IGNORECASE)
    return pattern.match(input_text)
