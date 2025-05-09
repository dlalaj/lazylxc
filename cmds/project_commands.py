import pylxd
from pylxd.exceptions import LXDAPIException
from pylxd.models.project import Project

# TODO: This entire module requires proper error handling but I will
# deal with it later


def list_projects() -> list[str]:
    client = pylxd.Client()
    return [p.name for p in client.projects.all()]


def create_project(name: str) -> str:
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
        proj.delete()
        return None
    except LXDAPIException as err:
        return err
