from rich.console import Console
from rich.__main__ import make_test_card

def run():
    Console().print(make_test_card())

if __name__ == "__main__":
    run()