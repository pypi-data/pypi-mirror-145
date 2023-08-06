API_KEY = "eyJ0eXAiOiJBUElLRVkifQ.QzAwMDAwMi5Db21tVERDLmE1NzljMTBlNWIwZmE1NzY"
DOMAIN = "hpdemo.thingsmatrix.io"
API_VERSION = "v2"
COMPANY = "HP"
BASE_URL = f"https://{DOMAIN}/api/{API_VERSION}"

DEVICE_URL = f"{BASE_URL}/devices"
MODEL_BYNAME_URL = f"{BASE_URL}/modules/name/"
GROUP_URL = f"{BASE_URL}/groups"
GROUP_BY_NAME_URL = f"{BASE_URL}/groups/name/"
GROUP_BY_ID_URL = f"{BASE_URL}/groups/"
DATA_URL = f"{BASE_URL}/module/data/events"

TEMPLATE_URL = f"{BASE_URL}/configs"

INVENTORY_URL = f"{BASE_URL}/module"