from textual.widgets import ListItem, ListView, Label
from textual import log

from cmds.image_commands import (
    list_images,
    delete_image,
    ImageRepr,
)


class ImageView(ListView):
    BINDINGS = [
        ("d", "delete_image", "Delete image"),
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
        self.images = []

    def _on_mount(self) -> None:
        return self._refresh()

    def _refresh(self):
        self.clear()
        self.images: list[ImageRepr] = list_images()

        for image in self.images:
            # An image label is formatted like so: `<RELEASE> -- <SERIAL> -- <FINGERPRINT>`
            pretty_label = f"{image.release} -- {image.serial} -- {image.fingerprint}"
            self.append(ListItem(Label(pretty_label)))

    def action_delete_image(self) -> None:
        """
        Deletes the selected/highlighted project from the project view or logs a
        notification if the project cannot be deleted.
        """
        selected_image = self.highlighted_child
        if selected_image is None:
            return

        try:
            image_line = selected_image.children[0].renderable
        except (IndexError, AttributeError) as e:
            log(f"Error retrieving image name: {e}")
            return

        # Extract fingerprint from `<RELEASE> -- <SERIAL> -- <FINGERPRINT>`
        fingerprint = image_line.split()[-1].strip()
        error = delete_image(fingerprint)
        if error:
            self.notify(message=str(error), title="Error deleting image", timeout=2)
            log(error)
        else:
            log("Image deleted successfully")
        self._refresh()

        # TODO: Complete logic to replace highlighted item
        # self.action_select_cursor()
