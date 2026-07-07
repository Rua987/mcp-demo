import argparse

from ce_snapshot import build_snapshot


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build a coin era snapshot.")
    parser.add_argument("--coins", type=int, required=True)
    parser.add_argument("--deaths", type=int, default=0)
    parser.add_argument("--era", type=int, default=0)
    args = parser.parse_args(argv)
    print(build_snapshot(args.coins, args.deaths, args.era))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
