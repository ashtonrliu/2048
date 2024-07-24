def is_power_of_two(n):
    """ Check if a number n can be expressed as a power of 2 """
    if n <= 1:
        return False
    return (n & (n - 1)) == 0

def get_digits(n):
    return len(str(n))

def load_output(filename):
    try:
        with open(filename, 'r') as file:
            filedata = file.read()
        return filedata
    except FileNotFoundError:
        return f"Error: The file '{filename}' does not exist."
    except IOError as e:
        return f"Error: {e}"