import config
import cli_args
import runner

arguments = cli_args.process_args()
configuration = config.config.set_config(arguments=arguments)
runner.run_parser(configuration)
