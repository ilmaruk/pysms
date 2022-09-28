import random


def bounded_gauss(mu: float, sigma: float) -> float:
    """A bounded implementation of random.gauss(), which
    makes sure that the returned valua is always within a given range.
    """
    MAX_TRIES = 10
    lower = mu - sigma
    upper = mu + sigma

    tries = 0
    while tries < MAX_TRIES:
        val = random.gauss(mu, sigma)
        if lower <= val <= upper:
            return val
        tries += 1

    # If all tries have failed to generate a value inside the range, then return the mean
    return mu

