from dotenv import load_dotenv

from .cli.interface import CLIInterface
from .storage.in_memory_storage import InMemoryStorage


def main() -> None:
    load_dotenv()

    storage = InMemoryStorage()
    cli = CLIInterface(storage=storage)

    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\n Exiting...")
    except Exception as e:
        print(f" Unexpected error: {e}")


if __name__ == "__main__":
    main()
