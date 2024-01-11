import argparse

from app.config import config


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="")
    # TODO: implement config file passed in arguments
    # parser.add_argument('-c',
    #                     '--config',
    #                     help='The path to the configuration file.',
    #                     type=str,
    #                     required=False)

    parser.add_argument('-r',
                        '--root',
                        help='The root directory where the parser starts the action.',
                        type=str,
                        required=False)

    parser.add_argument('-f',
                        '--file',
                        help='The extension for files that will be parsed.',
                        type=str,
                        required=False,
                        dest='file_extension')

    parser.add_argument('-o',
                        '--output',
                        help=f"The parser output. "
                             f"Accepted values: {config.Output.CONSOLE.value}, "
                             f"{config.Output.FILE.value}.",
                        type=str,
                        required=False)

    parser.add_argument('-a',
                        '--action',
                        help=f'The action that the parser will perform. '
                             f'Accepted values: {config.Action.CHECK_LINKS.value}, '
                             f'{config.Action.PRINT_LINKS.value}, '
                             f'{config.Action.SEARCH.value}',
                        type=str,
                        required=False)

    return parser


def check_and_set_args(args: argparse.Namespace) -> argparse.Namespace | None:
    if not args.root and not args.file_extension and not args.output and not args.action:
        print("No arguments passed.")
        return

    if not args.root:
        print("No root in args, using the default value.")
        args.root = config.DEFAULT_CONFIG['MAIN']['root']

    if not args.file_extension:
        print("No file in args, using the default value.")
        args.file_extension = config.DEFAULT_CONFIG['MAIN']['file_extension']

    if not args.output or args.output not in {item.value for item in config.Output}:
        print("No output in args or output has incorrect value, using the default value.")
        args.output = config.DEFAULT_CONFIG['MAIN']['output']

    if not args.action or args.action not in {item.value for item in config.Action}:
        print("No action in args or action has incorrect value, using the default value.")
        args.action = config.DEFAULT_CONFIG['MAIN']['action']

    return args


def process_args() -> argparse.Namespace:
    parser = create_parser()
    args = parser.parse_args()
    return check_and_set_args(args)


if __name__ == "__main__":
    pass
