import argparse


def greet(name: str) -> str:
    return f"Hello, {name}!"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="app", description="python-app template CLI")
    parser.add_argument("name", nargs="?", default="world", help="Name to greet")
    return parser


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    print(greet(args.name))


if __name__ == "__main__":
    main()
