from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Footer, Static, TabbedContent, TabPane, Markdown

from .project_view import ProjectView
from .image_view import ImageView
from .instance_view import InstanceView

LETO = """
Duke Leto I Atreides

Head of House Atreides.
"""

JESSICA = """
Lady Jessica

Bene Gesserit and concubine of Leto, and mother of Paul and Alia.
"""

PAUL = """
Paul Atreides

Son of Leto and Jessica.
"""


class TitledWidget(Vertical):
    def __init__(self, title: str, enclosed: Widget, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.enclosed = enclosed

    def compose(self):
        yield Static(self.title, classes="title")
        yield self.enclosed


class LazyLxcApp(App):
    """A TUI based application that allows a way to interface with LXC containers"""

    CSS_PATH = "./styles.tcss"

    BINDINGS = [
        ("1", "focus_projects", "Projects"),
        ("2", "focus_images", "Images"),
        ("3", "focus_instances", "Instances"),
        ("4", "focus_right", "Info"),
        ("q", "exit_application", "Exit"),
    ]

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
                    title="Images", enclosed=ImageView(id="images", classes="listing")
                )
                yield TitledWidget(
                    title="Instances",
                    enclosed=InstanceView(id="instances", classes="listing"),
                )

            # Right panel to get information about a selected item
            with TabbedContent(id="right_panel"):
                with TabPane("Leto", id="leto"):
                    yield Markdown(LETO)
                with TabPane("Jessica", id="jessica"):
                    yield Markdown(JESSICA)
                with TabPane("Paul", id="paul"):
                    yield Markdown(PAUL)
        yield Footer()

    def action_focus_projects(self) -> None:
        item = self.query_one("#projects")
        self.set_focus(item)

    def action_focus_images(self) -> None:
        item = self.query_one("#images")
        self.set_focus(item)

    def action_focus_instances(self) -> None:
        item = self.query_one("#instances")
        self.set_focus(item)

    def action_focus_right(self) -> None:
        right_panel = self.query_one("#right_panel", TabbedContent)
        self.set_focus(right_panel)  # Set focus on the TabbedContent widget
        active_tab_id = right_panel.active  # Get the ID of the active tab
        if active_tab_id:
            right_panel.switch_tab(
                active_tab_id
            )  # Programmatically switch to the active tab

    def action_exit_application(self) -> None:
        self.exit("Exiting lazylxc")
