import pylxd
from pylxd.exceptions import LXDAPIException
from pylxd.models.image import Image
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ImageRepr:
    fingerprint: str
    arch: str
    serial: str
    release: str

def get_client(project : str = 'default') -> pylxd.Client:
    return pylxd.Client(project=project)

def list_images(project: str = "default") -> List[ImageRepr]:
    """
    List all images in the specified LXD project.
    """
    client = get_client(project)
    images = Image.all(client)
    return [
        ImageRepr(
            fingerprint=img.fingerprint,
            arch=img.properties.get("architecture", ""),
            serial=img.properties.get("serial", ""),
            release=img.properties.get("version", "")
        )
        for img in images
    ]


def delete_image(fingerprint: str, project: str = "default") -> Optional[Exception]:
    """
    Delete an image by fingerprint. Returns None if successful, or the exception if failed.
    """
    client = get_client(project)
    try:
        img = Image.get(client, fingerprint)
        img.delete(wait=True)
        return None
    except LXDAPIException as err:
        return err
