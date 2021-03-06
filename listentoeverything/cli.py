# -*- coding: utf-8 -*-

"""Console script for listentoeverything."""
import sys
import click
try:
    from listentoeverything import listen
except:
    import listen
from os import path
sys.path.append('..')


@click.command()
@click.option("--config_file", default=path.join(path.expanduser("~"), ".listen.yml"), help="Path of config file")
def main(config_file):
    """Console script for listentoeverything."""
    listen.main(config_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
