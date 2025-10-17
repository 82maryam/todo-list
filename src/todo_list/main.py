
from .cli.interface import CLIInterface


def main() -> None:
    try:
        cli = CLIInterface()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n excist")
    except Exception as e:
        print(f" erorr {e}")


if __name__ == "__main__":
    main()