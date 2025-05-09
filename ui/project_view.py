from textual.widgets import ListItem, ListView, Label
from textual import log

from ui.common.input import NamedInput
from cmds.project_commands import (
    list_projects,
    create_project,
    delete_project,
)

# TODO: Also add functionality to send message to app so it updates images and instances when highlight changes


class ProjectView(ListView):
    BINDINGS = [
        ("c", "create_project", "Create project"),
        ("d", "delete_project", "Delete project"),
    ]

    def _on_mount(self) -> None:
        return self._refresh()

    def _refresh(self) -> None:
        """
        Refreshes the project list by retrieving updates from the LXD REST API client.
        """
        self.clear()
        for project in list_projects():
            self.append(ListItem(Label(project)))

    def action_create_project(self) -> None:
        """
        Creates a new project based on the name provided by the user.
        """

        # Show the NamedInput screen to get the project name
        def handle_project_creation(name: str) -> None:
            """
            Callback to help capture input from the Screen
            """
            # Do no raise errors on escape press
            if name is None:
                return
            error = create_project(name)
            if error:
                self.notify(
                    message=str(error), title="1: Error creating project", timeout=2
                )
            else:
                log("Project created successfully")
            self._refresh()

        self.app.push_screen(NamedInput(), handle_project_creation)

    def action_delete_project(self) -> None:
        """
        Deletes the selected/highlighted project from the project view or logs a
        notification if the project cannot be deleted.
        """
        selected_project = self.highlighted_child
        if selected_project is None:
            return

        try:
            project_name = selected_project.children[0].renderable
        except (IndexError, AttributeError) as e:
            log(f"Error retrieving project name: {e}")
            return

        error = delete_project(project_name)
        if error:
            self.notify(message=str(error), title="Error deleting project", timeout=2)
            log(error)
        else:
            log("Project deleted successfully")
        self._refresh()

        # TODO: Complete logic to replace highlighted item
        # self.action_select_cursor()

    # def on_list_view_highlighted()
