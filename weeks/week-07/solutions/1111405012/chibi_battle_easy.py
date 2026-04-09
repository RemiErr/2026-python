import argparse

from chibi_battle import (
    DEFAULT_BATTLES_PATH,
    DEFAULT_GENERALS_PATH,
    GameExitRequested,
    run_cli,
    run_interactive_cli,
)


def main(argv=None):
    parser = argparse.ArgumentParser(description="赤壁戰役簡化版 CLI")
    parser.add_argument("--generals", default=str(DEFAULT_GENERALS_PATH))
    parser.add_argument("--battles", default=str(DEFAULT_BATTLES_PATH))
    parser.add_argument("--mode", choices=["auto", "play"], default="play")
    args = parser.parse_args(argv)

    print("赤壁戰役簡化版")
    try:
        if args.mode == "play":
            run_interactive_cli(args.generals, args.battles)
        else:
            print(run_cli(args.generals, args.battles))
    except GameExitRequested:
        print("你已離開戰役。")
    return 0


if __name__ == "__main__":
    main()
