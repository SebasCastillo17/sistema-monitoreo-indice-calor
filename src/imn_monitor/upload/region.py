from src.db.region.region_service import Create
from src.imn_monitor.extraction.extract_region import get_regions
from src.imn_monitor.extraction.raw_data import raw_content

def upload_region():
    for name in get_regions(raw_content):
        Create(name)
