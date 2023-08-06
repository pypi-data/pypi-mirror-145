from shutil import copytree, rmtree

from dotcp.cli import fatal, get_args_parser, info
from dotcp.config import Config


def main():
    parser = get_args_parser()
    args = parser.parse_args()
    if args.overwrite and args.append:
        parser.error("`--overwrite` and `--append` flags can't be used at once")

    try:
        config = Config(args.config, args.config_home)
    except Exception as err:
        fatal(err)

    if args.overwrite:
        if args.destination.exists():
            rmtree(args.destination)
            info(f"Rewriting dotfiles to {args.destination}...")
        else:
            fatal(f"{args.destination} does not exist")
    elif args.append:
        if args.destination.exists():
            info(f"Appending dotfiles to {args.destination}...")
        else:
            fatal(f"{args.destination} does not exist")
    else:
        if args.destination.exists():
            fatal(
                f"{args.destination} already exists. Use `--append` or `--overwrite` flag"
            )
        else:
            info(f"Copying dotfiles to {args.destination}...")

    try:
        targets = config.get_targets()
    except Exception as err:
        fatal(err)

    for target in targets:
        copytree(
            target.resolve(), args.destination.joinpath(target.name), dirs_exist_ok=True
        )
        info(f"+ {str(args.destination.joinpath(target.name)):<25} ({target})")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
