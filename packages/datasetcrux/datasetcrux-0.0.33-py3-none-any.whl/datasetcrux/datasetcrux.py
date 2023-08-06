def random_string(length):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters) for i in range(length))
