from textual.screen import ModalScreen
from textual.widgets import Input
from textual.events import Key

from textual import log


class NamedInput(ModalScreen[str]):
    def compose(self):
        yield Input(placeholder="Enter name...", id="named_input", classes="textinput")

    # def on_mount(self):
    #     self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        log(event.value)
        self.dismiss(event.value)

    def on_key(self, event: Key):
        if event.key == "escape":
            self.dismiss(None)
