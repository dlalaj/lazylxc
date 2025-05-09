from textual.widgets import ListItem, ListView, Label

instances = ["dev", "stg", "prod"]


class InstanceView(ListView):
    BINDINGS = [
        ("s", "start_instance", "Start"),
        ("p", "pause_instance", "Pause"),
        ("d", "delete_instance", "Delete"),
        ("r", "restart_instance", "Restart"),
    ]

    def _on_mount(self) -> None:
        return self._refresh()

    def _refresh(self) -> None:
        # First clear the entire view
        self.clear()

        # Dummy load all projects
        for instance in instances:
            self.append(ListItem(Label(instance)))

    def action_start_instance(self) -> None:
        print("Fake start")

    def action_pause_instance(self) -> None:
        print("Fake stop")

    def action_delete_instance(self) -> None:
        print("Fake delete")

    def action_restart_instance(self) -> None:
        print("Fake restart")
