import re
from ipaddress import AddressValueError, IPv4Address

import typer

from cli.core.find import create_find_table, search_devices

app = typer.Typer()


def validate_mac(value: str) -> str:
    if len(value) not in [4, 12]:
        raise typer.BadParameter("Please enter the full or last 4 characters of the MAC address")
    mac = re.match(rf"^[a-fA-F0-9]{{{len(value)}}}$", value)
    if not mac:
        raise typer.BadParameter(f"Invalid MAC: {value}")
    return "-".join([value[i : i + 2] for i in range(0, len(value), 2)])


def validate_ip(value: str) -> str:
    try:
        str(IPv4Address(value))
    except AddressValueError:
        raise typer.BadParameter("Please enter a valid IP address")
    return value


@app.command()
def mac(
    mac: str = typer.Argument(..., callback=validate_mac, help="Full or last 4 characters of the MAC address"),
    username: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True),
):
    """
    Find Desktop/Phone by MAC Address
    """
    devices = search_devices(mac, username, password)
    create_find_table(devices)


@app.command()
def ip(
    ip: str = typer.Argument(..., callback=validate_ip, help="IP Address"),
    username: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True),
):
    """
    Find Desktop/Phone by IP Address
    """
    devices = search_devices(ip, username, password)
    create_find_table(devices)
