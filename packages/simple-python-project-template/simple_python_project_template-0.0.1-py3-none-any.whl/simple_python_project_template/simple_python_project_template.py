import logging

logging.basicConfig(level=logging.DEBUG)

def hello():
    logging.info("Hello from the example project.")

if __name__ == "__main__":
    hello()