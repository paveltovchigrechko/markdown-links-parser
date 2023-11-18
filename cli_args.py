import argparse
import config.config


def create_parser():
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
                        help=f"The parser output. Accepted values: {config.config.Output.CONSOLE.value}, {config.config.Output.FILE.value}.",
                        type=str,
                        required=False)

    parser.add_argument('-a',
                        '--action',
                        help=f'The action that the parser will perform. Accepted values: {config.config.Action.CHECK_LINKS.value}, {config.config.Action.PRINT_LINKS.value}, {config.config.Action.SEARCH.value}',
                        type=str,
                        required=False)

    return parser


def check_and_set_args(args):
    if not args.root and not args.file_extension and not args.output and not args.action:
        print("No arguments passed.")
        return

    if not args.root:
        print("No root in args, using the default value.")
        args.root = config.config.DEFAULT_CONFIG['MAIN']['root']
        # print(f"root={args.root}")

    if not args.file_extension:
        print("No file in args, using the default value.")
        args.file_extension = config.config.DEFAULT_CONFIG['MAIN']['file_extension']
        # print(f"file={args.file_extension}")

    if not args.output or args.output not in {item.value for item in config.config.Output}:
        print("No output in args or output has incorrect value, using the default value.")
        args.output = config.config.DEFAULT_CONFIG['MAIN']['output']
        # print(f"output={args.output}")

    if not args.action or args.action not in {item.value for item in config.config.Action}:
        print("No action in args or action has incorrect value, using the default value.")
        args.action = config.config.DEFAULT_CONFIG['MAIN']['action']
        # print(f"action={args.action}")

    return args


def process_args():
    parser = create_parser()
    args = parser.parse_args()
    return check_and_set_args(args)
