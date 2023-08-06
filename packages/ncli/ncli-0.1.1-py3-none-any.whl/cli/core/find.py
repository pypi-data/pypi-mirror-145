from ipaddress import AddressValueError, IPv4Address, IPv4Network

from rich.console import Console
from rich.table import Table
from scrapli.driver.core import IOSXEDriver

from cli.settings import Settings, load_settings
from cli.utils import query_sw

settings: Settings = load_settings()


queries = {
    "get_by_mac": """
        SELECT IPNode.IpNodeId as nodeid, IPNode.IPAddress as ip, Subnet.Address as network, Subnet.CIDR as cidr, IPNode.MAC as mac, IPNode.DhcpClientName as hostname
        FROM IPAM.IPNode
        INNER JOIN IPAM.Subnet ON IPNode.SubnetId = Subnet.SubnetId
        WHERE MAC LIKE @i
    """,
    "get_by_ip": """
        SELECT IPNode.IpNodeId as nodeid, IPNode.IPAddress as ip, Subnet.Address as network, Subnet.CIDR as cidr, IPNode.MAC as mac, IPNode.DhcpClientName as hostname
        FROM IPAM.IPNode
        INNER JOIN IPAM.Subnet ON IPNode.SubnetId = Subnet.SubnetId
        WHERE IPAddress LIKE @i
    """,
}


def search_devices(identifier: str, username: str, password: str) -> list[dict[str, str | int]]:
    devices = get_devices(identifier)
    for device in devices:
        get_device_switch(device)
        get_device_switch_port(device, username, password)
    return devices


def get_devices(identifier: str):
    try:
        str(IPv4Address(identifier))
        query = queries.get("get_by_ip")
        parameters = {"i": identifier}
    except AddressValueError:
        query = queries.get("get_by_mac")
        parameters = {"i": f"%{identifier}%"}

    if settings.ENVIRONMENT == "test":
        devices = [
            {
                "nodeid": 1,
                "ip": "10.10.1.1",
                "network": "10.10.1.0",
                "cidr": 24,
                "mac": "52-54-00-18-8B-85",
                "hostname": "PC1011",
            }
        ]
    else:
        devices = query_sw(query, parameters)
        for device in devices:
            device["hostname"] = device["hostname"].split(".")[0]
    return devices


def get_device_switch(device: dict):
    if settings.ENVIRONMENT == "test":
        device.update({"ip": "10.10.1.254", "hostname": "SW1011"})
    else:
        query = """
            SELECT Nodes.NodeId as nodeid, Nodes.IPAddress as ip, Nodes.SysName as hostname
            FROM Orion.Nodes
            INNER JOIN Orion.NodeIPAddresses ON Nodes.NodeId = NodeIPAddresses.NodeId
            WHERE NodeIPAddresses.IPAddress = @i
        """
        parameters = {
            "i": str(IPv4Network(f"{device['network']}/{device['cidr']}")[-2]),
        }
        switch = query_sw(query, parameters)[0]
        device.update({"switch": switch["hostname"].split(".")[0], "switch_ip": switch["ip"]})


def get_device_switch_port(device_dict: dict, username: str, password: str):
    device = {
        "host": device_dict["switch_ip"],
        "auth_username": username,
        "auth_password": password,
        "auth_strict_key": False,
        "transport": "ssh2",
    }

    with IOSXEDriver(**device) as conn:
        result = conn.send_command("show mac address-table")

        port = next(
            res["destination_port"][0]
            for res in result.textfsm_parse_output()
            if "".join(device_dict["mac"].split("-")).lower()[-4:] == res["destination_address"][-4:]
        )
        result = conn.send_command(f"show interface {port}").textfsm_parse_output()[0]

    device_dict.update(
        {
            "port": port,
            "link": result["link_status"],
            "protocol": result["protocol_status"].split(" ")[0],
            "last_input": result["last_input"],
            "last_output": result["last_output"],
            "input_errors": result["input_errors"],
            "output_errors": result["output_errors"],
        }
    )


def create_find_table(devices: dict):
    table = Table(title="Devices")
    table.add_column("Hostname")
    table.add_column("IP Address")
    table.add_column("MAC Address")
    table.add_column("Switch")
    table.add_column("Switch IP")
    table.add_column("Port")
    table.add_column("Link")
    table.add_column("Protocol")
    table.add_column("Last Input")
    table.add_column("Last Output")
    table.add_column("Input Errors")
    table.add_column("Output Errors")

    for device in devices:
        table.add_row(
            device["hostname"],
            device["ip"],
            device["mac"],
            device["switch"],
            device["switch_ip"],
            device["port"],
            device["link"],
            device["protocol"],
            device["last_input"],
            device["last_output"],
            device["input_errors"],
            device["output_errors"],
        )

    console = Console()
    console.print(table)
