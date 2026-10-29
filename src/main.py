from src.imn_monitor.upload.region import upload_region
from src.imn_monitor.extraction.extract_station import get_station
from src.imn_monitor.extraction.raw_data import raw_content

get_station(raw_content)
upload_region()
