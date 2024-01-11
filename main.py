import app.config.config as config
import app.config.cli_args as cli_args
import app.runner.runner as runner

arguments = cli_args.process_args()
configuration = config.set_config(arguments=arguments)
runner.run_parser(configuration)
