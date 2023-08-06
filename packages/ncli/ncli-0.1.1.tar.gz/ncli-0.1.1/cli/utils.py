import re
from pathlib import Path

from httpx import Client, Response

from cli.settings import Settings, load_settings

settings: Settings = load_settings()


def query_sw(query: str, parameters: dict) -> list[dict[str, str | int]]:
    headers = {"Content-Type": "application/json"}
    data = {
        "query": query,
        "parameters": parameters,
    }

    with Client(verify=False) as client:
        response: Response = client.post(
            f"https://{settings.SW_HOST}:17778/SolarWinds/InformationService/v3/Json/Query",
            headers=headers,
            auth=(settings.SW_USER, settings.SW_PASS),
            json=data,
        )

    if response.status_code != 200:
        return None

    return response.json()["results"]


def get_version() -> str:
    pyproject_file = Path(Path(__file__).parent.parent / "pyproject.toml")
    with open(pyproject_file, "r") as file:
        content = file.read()
    version = re.search(r"\s*version\s*=\s*[\"']\s*([.\w]{3,})\s*[\"']\s", content)[1]
    return version
