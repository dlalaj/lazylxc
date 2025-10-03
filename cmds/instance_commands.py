import pylxd
from pylxd.exceptions import LXDAPIException
from pylxd.models.instance import Instance
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class InstanceRepr:
    name: str
    arch: str
    type: str
    status: str
    config: dict

def get_client(project : str = 'default') -> pylxd.Client:
    return pylxd.Client(project=project)

def list_instances(project: str = 'default') -> List[InstanceRepr]:
    client = get_client(project)
    # Hacky string processing to deal with the weird naming from non-default project
    return [
        InstanceRepr(
            instance.name.split('?')[0],
            instance.architecture,
            instance.type,
            instance.status,
            instance.config
        )
        for instance in Instance.all(client)
    ]

def start_instance(name: str, project: str = 'default') -> Optional[Exception]:
    client = get_client(project=project)
    try:
        if Instance.exists(client, name) and Instance.status:
            Instance.get(client, name).start(wait=True)
        return None
    except LXDAPIException as err:
        return err

def stop_instance(name: str, project: str = 'default') -> Optional[Exception]:
    client = get_client(project=project)
    try:
        if Instance.exists(client, name):
            Instance.get(client, name).stop(wait=True)
        return None
    except LXDAPIException as err:
        return err

def restart_instance(name: str, project: str = 'default') -> Optional[Exception]:
    client = get_client(project=project)
    try:
        if Instance.exists(client, name):
            Instance.get(client, name).restart(wait=True)
        return None
    except LXDAPIException as err:
        return err

def delete_instance(name: str, project: str = 'default') -> Optional[Exception]:
    client = get_client(project=project)
    try:
        if Instance.exists(client, name):
            Instance.get(client, name).delete(wait=True)
        return None
    except LXDAPIException as err:
        return err
