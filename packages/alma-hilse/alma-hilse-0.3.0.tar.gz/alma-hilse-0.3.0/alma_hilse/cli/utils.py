import typer
from typing import Optional
from alma_hilse.lib.utils import initCCL_HIL

utils_app = typer.Typer(short_help="HILSE general environment setup commands")


@utils_app.command(short_help="Turn on AmbManager (DMC by default)")
def turn_on_ambmanager(
    abm: Optional[str] = typer.Option("DMC", help="ABM name for AmbManager"),
):
    initCCL_HIL._turn_amb_mgr(abm)


@utils_app.command(
    short_help="Get devices found connected to a given ABM (DMC by default)"
)
def get_devices(
    abm: Optional[str] = typer.Option("DMC", help="ABM name for AmbManager"),
):
    initCCL_HIL.get_devices(abm)
