from yaml import safe_load

from app.constants import DeviceConstants
from app.schemas import DeviceConfigForm


def load_config() -> DeviceConfigForm:
    with open(DeviceConstants.BASE_DEVICE_CONFIG) as f:
        data = f.read()

    data = safe_load(data)

    env = data.get("env")
    if env:
        del data["env"]

    env = [f"{k}={v}" for k, v in env.items()]

    config = DeviceConfigForm(env=env, **data)

    return config
