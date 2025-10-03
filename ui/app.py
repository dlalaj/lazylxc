from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Footer, Static, TabbedContent, TabPane

from .project_view import ProjectView, ProjectSelected
from .image_view import ImageView
from .instance_view import InstanceView


class TitledWidget(Vertical):
    def __init__(self, title: str, enclosed: Widget, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.enclosed = enclosed

    def compose(self):
        yield Static(self.title, classes="title")
        yield self.enclosed


class LazyLxcApp(App):
    """A TUI based application that allows interfacing with LXC containers"""

    CSS_PATH = "./styles.tcss"

    BINDINGS = [
        ("1", "focus_projects", "Projects"),
        ("2", "focus_images", "Images"),
        ("3", "focus_instances", "Instances"),
        ("4", "focus_right", "Info"),
        ("q", "exit_application", "Exit"),
    ]

    TAB_MAP = {
        "projects": [("Info", "project-info"), ("Settings", "project-settings")],
        "images": [("Info", "image-info"), ("Config", "image-config")],
        "instances": [("Info", "instance-info"), ("Logs", "instance-logs"), ("Config", "instance-config")],
    }

    def compose(self) -> ComposeResult:
        self.theme = "textual-dark"
        with Horizontal():
            # Left pannel to navigate projects, images, and containers
            with Vertical(id="left_panel"):
                yield TitledWidget(
                    title="Projects",
                    enclosed=ProjectView(id="projects", classes="listing"),
                )
                yield TitledWidget(
                    title="Images",
                    enclosed=ImageView(id="images", classes="listing"),
                )
                yield TitledWidget(
                    title="Instances",
                    enclosed=InstanceView(id="instances", classes="listing"),
                )

            # Right panel to get information about a selected item
            yield TabbedContent(id="right_panel")
        yield Footer()

    def on_mount(self) -> None:
        self.action_focus_projects()
    
    def on_project_selected(self, message: ProjectSelected) -> None:
        # Refresh views on a newly selected project
        project_name = message.project_name
        
        instance_view = self.query_exactly_one("#instances", InstanceView)
        instance_view.handle_project_selected(project_name)

        image_view = self.query_exactly_one("#images", ImageView)
        image_view.handle_project_selected(project_name)


    def update_tabbed_content(self, widget_id: str):
        right_pannel = self.query_one("#right_panel", TabbedContent)
        right_pannel.clear_panes()  # Remove old tab panes

        for title, id in self.TAB_MAP[widget_id]:
            right_pannel.add_pane(TabPane(title, id=id))

    def action_focus_projects(self) -> None:
        item = self.query_one("#projects")
        self.set_focus(item)
        self.update_tabbed_content("projects")

    def action_focus_images(self) -> None:
        item = self.query_one("#images")
        self.set_focus(item)
        self.update_tabbed_content("images")

    def action_focus_instances(self) -> None:
        item = self.query_one("#instances")
        self.set_focus(item)
        self.update_tabbed_content("instances")

    def action_exit_application(self) -> None:
        self.exit("Exiting lazylxc")
