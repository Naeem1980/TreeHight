# main.py
import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.graphics import Color, Ellipse


class TreeHeightApp(App):
    def build(self):
        self.points = []
        self.vertical_fov_deg = 60  # typical phone estimate; improve later per device

        root = BoxLayout(orientation="vertical")

        self.filechooser = FileChooserIconView(filters=["*.jpg", "*.jpeg", "*.png"])
        self.filechooser.bind(on_submit=self.load_image)
        root.add_widget(self.filechooser)

        self.image = Image(allow_stretch=True, keep_ratio=True)
        self.image.bind(on_touch_down=self.on_image_touch)
        root.add_widget(self.image)

        self.distance_input = TextInput(
            hint_text="Distance to tree in metres",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=45,
        )
        root.add_widget(self.distance_input)

        calc_btn = Button(text="Calculate height", size_hint_y=None, height=45)
        calc_btn.bind(on_press=self.calculate_height)
        root.add_widget(calc_btn)

        self.result = Label(text="Select photo, tap base then top of tree.")
        root.add_widget(self.result)

        return root

    def load_image(self, chooser, selection, touch):
        if selection:
            self.image.source = selection[0]
            self.points = []
            self.result.text = "Tap base of tree, then top of tree."

    def on_image_touch(self, widget, touch):
        if widget.collide_point(*touch.pos) and self.image.source:
            if len(self.points) < 2:
                self.points.append((touch.x, touch.y))
                with widget.canvas.after:
                    Color(1, 0, 0)
                    Ellipse(pos=(touch.x - 5, touch.y - 5), size=(10, 10))

                if len(self.points) == 1:
                    self.result.text = "Now tap the top of the tree."
                else:
                    self.result.text = "Enter distance and press Calculate."

    def calculate_height(self, instance):
        if len(self.points) != 2:
            self.result.text = "Please tap base and top of tree first."
            return

        try:
            distance = float(self.distance_input.text)
        except ValueError:
            self.result.text = "Please enter a valid distance."
            return

        y1 = self.points[0][1]
        y2 = self.points[1][1]
        tree_pixel_height = abs(y2 - y1)

        image_display_height = self.image.height
        fraction_of_frame = tree_pixel_height / image_display_height

        vertical_fov_rad = math.radians(self.vertical_fov_deg)
        real_frame_height = 2 * distance * math.tan(vertical_fov_rad / 2)

        estimated_height = real_frame_height * fraction_of_frame

        self.result.text = f"Estimated tree height: {estimated_height:.2f} m"


if __name__ == "__main__":
    TreeHeightApp().run()
