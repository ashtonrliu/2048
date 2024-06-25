def is_power_of_two(n):
    """ Check if a number n can be expressed as a power of 2 """
    if n <= 1:
        return False
    return (n & (n - 1)) == 0

def get_digits(n):
    return len(str(n))