from os import wait

from src.imn_monitor.extraction.raw_data import raw_content
from .extract_region import get_regions

class RegionData:
    def __init__(self, region: str, name: str, active: bool, location: str, url: str):
        self.region = region
        self.name = name
        self.active = active
        self.location = location
        self.url = url

def get_stations(raw_content) -> list[RegionData]:
    regions = get_regions(raw_content)
    stations = []
    region_name = 0

    for table in raw_content.find_all("table"):
        paragraphs = table.find_all("p")

        for i in range(0, len(paragraphs), 4):
            block = paragraphs[i:i + 4]

            if len(block) < 4:
                continue

            name = block[0].get_text(strip=True)
            location = block[1].get_text(strip=True)
            active_text = block[2].get_text(strip=True)
            link = block[3].find("a")
            url = link.get("href", "") if link else ""

            if name == "Nombre":
                continue

            station = RegionData(
                region=regions[region_name],
                name=name,
                active=active_text.lower() == "activa",
                location=location,
                url=url
            )

            stations.append(station)

        if region_name < len(regions) - 1:
            region_name += 1

    return stations
