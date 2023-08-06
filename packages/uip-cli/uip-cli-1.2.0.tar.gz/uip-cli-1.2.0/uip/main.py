from uip.cliconfig.setupcli import setup_cli_args
from uip.config import config


def main():
    """
    Entry point of the CLI
    """
    config.create_global_config_file()
    setup_cli_args()


if __name__ == "__main__":
    main()
