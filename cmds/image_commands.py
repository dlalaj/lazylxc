import pylxd
from pylxd.exceptions import LXDAPIException
from pylxd.models.image import Image
from dataclasses import dataclass


@dataclass
class ImageRepr:
    fingerprint: str
    arch: str
    serial: str
    release: str


def list_images(project: str = "default") -> list[str]:
    client = pylxd.Client(project=project)
    all_images = Image.all(client)
    image_data = []
    for image in all_images:
        fingerprint = image.fingerprint
        arch = image.properties.get("architecture", "")
        serial = image.properties.get("serial", "")
        release = image.properties.get("version", "")
        image_data.append(ImageRepr(fingerprint, arch, serial, release))
    return image_data


def delete_image(fingerprint: str):
    client = pylxd.Client()
    try:
        img = Image.get(client, fingerprint)
        img.delete(wait=True)
        return None
    except LXDAPIException as err:
        return err
