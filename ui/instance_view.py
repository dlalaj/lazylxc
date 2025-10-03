from textual.widgets import ListItem, ListView, Label
from textual import log

from cmds.instance_commands import (
    list_instances,
    start_instance,
    stop_instance,
    restart_instance,
    delete_instance,
    InstanceRepr
)


class InstanceView(ListView):
    BINDINGS = [
        ("s", "start_instance", "Start"),
        ("p", "pause_instance", "Pause"),
        ("d", "delete_instance", "Delete"),
        ("r", "restart_instance", "Restart"),
    ]

    def __init__(
        self,
        *children,
        initial_index=0,
        name=None,
        id=None,
        classes=None,
        disabled=False,
    ):
        super().__init__(
            *children,
            initial_index=initial_index,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.instances = []
        self.current_project = 'default'

    def _on_mount(self) -> None:
        return self._refresh(self.current_project)

    def _refresh(self, project: str = 'default') -> None:
        self.clear()
        self.instances: list[InstanceRepr] = list_instances(project)

        for instance in self.instances:
            # An instance label format: `<NAME> -- <TYPE> -- <STATUS>`
            pretty_label = f"{instance.name} -- {instance.type} -- {instance.status}"
            self.append(ListItem(Label(pretty_label)))

    def handle_project_selected(self, project_name: str) -> None:
        # Refresh projects on a newly selected project
        self._refresh(project_name)
        self.current_project = project_name


    def action_start_instance(self) -> None:
        selected_instance = self.highlighted_child
        if selected_instance is None:
            return
        
        try:
            instance_info = selected_instance.children[0].renderable
        except (IndexError, AttributeError) as e:
            log(f"Error retrieving instance information: {e}")
            return
        
        # Extract name from `<NAME> -- <TYPE> -- <STATUS>`
        name = instance_info.split()[0].strip()
        error = start_instance(name, self.current_project)
        if error:
            self.notify(message=str(error), title=f"Error starting instance {name}", timeout=2)
            log(error)
        else:
            log("Instance started successfully")
        self._refresh(self.current_project)

    def action_pause_instance(self) -> None:
        selected_instance = self.highlighted_child
        if selected_instance is None:
            return

        try:
            instance_info = selected_instance.children[0].renderable
        except (IndexError, AttributeError) as e:
            log(f"Error retrieving instance information: {e}")
            return

        # Extract name from `<NAME> -- <TYPE> -- <STATUS>`
        name = instance_info.split()[0].strip()
        error = stop_instance(name, self.current_project)
        if error:
            self.notify(message=str(error), title=f"Error pausing instance {name}", timeout=2)
            log(error)
        else:
            log("Instance paused successfully")
        self._refresh(self.current_project)

    def action_delete_instance(self) -> None:
        selected_instance = self.highlighted_child
        if selected_instance is None:
            return

        try:
            instance_info = selected_instance.children[0].renderable
        except (IndexError, AttributeError) as e:
            log(f"Error retrieving instance information: {e}")
            return

        # Extract name from `<NAME> -- <TYPE> -- <STATUS>`
        name = instance_info.split()[0].strip()
        error = delete_instance(name, self.current_project)
        if error:
            self.notify(message=str(error), title=f"Error deleting instance {name}", timeout=2)
            log(error)
        else:
            log("Instance deleted successfully")
        self._refresh(self.current_project)

    def action_restart_instance(self) -> None:
        selected_instance = self.highlighted_child
        if selected_instance is None:
            return

        try:
            instance_info = selected_instance.children[0].renderable
        except (IndexError, AttributeError) as e:
            log(f"Error retrieving instance information: {e}")
            return

        # Extract name from `<NAME> -- <TYPE> -- <STATUS>`
        name = instance_info.split()[0].strip()
        error = restart_instance(name, self.current_project)
        if error:
            self.notify(message=str(error), title=f"Error restarting instance {name}", timeout=2)
            log(error)
        else:
            log("Instance restarted successfully")
        self._refresh(self.current_project)
