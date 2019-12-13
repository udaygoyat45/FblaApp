def generate_id (N):
    import random, string
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))