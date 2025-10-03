import pylxd
from pylxd.exceptions import LXDAPIException
from pylxd.models.project import Project

# TODO: This entire module requires proper error handling but I will
# deal with it later


def list_projects() -> list[str]:
    client = pylxd.Client()
    all_projects = Project.all(client)
    return [p.name for p in all_projects]


def create_project(name: str):
    client = pylxd.Client()
    try:
        Project.create(client, name)
        return None
    except LXDAPIException as err:
        return err


def delete_project(name: str):
    client = pylxd.Client()
    try:
        proj = Project.get(client, name)
        proj.delete(wait=True)
        return None
    except LXDAPIException as err:
        return err
