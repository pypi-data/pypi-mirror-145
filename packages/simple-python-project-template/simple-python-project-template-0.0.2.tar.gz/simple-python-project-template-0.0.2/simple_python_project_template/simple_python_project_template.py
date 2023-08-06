import logging

def hello(name="World"):
    """A simple hello function.

    Args:
        name (str): A persons name in string format. Default is 'World'.

    Returns:
        message (str): A greeting for the person, in string format.
    
    """
    message = f"Hello {name}, from the example project."
    logging.debug(message)
    print(message)
    return message

if __name__ == "__main__":
    hello()