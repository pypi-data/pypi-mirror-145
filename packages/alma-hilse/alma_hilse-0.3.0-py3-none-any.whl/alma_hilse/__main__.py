import typer
from typing import Optional

from alma_hilse import __version__

# Commands and subcommands import
from alma_hilse.cli import utils
from alma_hilse.cli import corr
from alma_hilse.cli import timing

# Command-line application based on Typer
app = typer.Typer(add_completion=False)

# Commands and subcommands definition divided by subsystem or functionality set
app.add_typer(timing.timing_app, name="timing")
app.add_typer(corr.corr_app, name="corr")
app.add_typer(utils.utils_app, name="utils")


@app.callback()
def callback():
    """
    Collection of diagnostics and configuration commands for ALMA HILSE

    Usage example (not all commands shown. Use --help for complete list):

    \b
    alma-hilse --help
    alma-hilse version
    alma-hilse timing --help
    alma-hilse timing status # LORR/LFTRR status for HILSE
    alma-hilse timing resync # LORR/LFTRR resync to CLO reference

    alma-hilse corr --help
    alma-hilse corr status # power, parity and delay status of DRXs

    alma-hilse utils --help
    alma-hilse utils get-devices # list devices connected to ABM
    alma-hilse utils turn-on-ambmanager

    """


@app.command(short_help="Show current version")
def version():
    print(__version__)


def main():
    app()


if __name__ == "__main__":
    main()
