from textual.widgets import ListItem, ListView, Label

labels = ["focal", "jammy", "noble", "plucky"]


class ImageView(ListView):
    def _on_mount(self) -> None:
        return self._refresh()

    def _refresh(self) -> None:
        # First clear the entire view
        self.clear()

        # Dummy load all images under the currently selected project
        for image in labels:
            self.append(ListItem(Label(image)))
