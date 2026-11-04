"""Highscores screen: the best scores."""

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen
import json


class HighscoresScreen(Screen):
    """Show the top 10 scores."""

    def handle_event(self, event: InputEvent) -> None:
        """Go back to the menu on Escape."""
        if event.kind == KEY_DOWN and event.key == "escape":
            self._app.show_menu()

    def draw(self, renderer: Renderer) -> None:
        """Draw the scores (placeholder text until the highscore table)."""
        title = "HIGHSCORES"
        middle = int(self._app.width / 2)
        renderer._font
        renderer.string_put(
            int(middle - (len(title) / 2) * self._app.character),
            50,
            0xFFFFFF,
            title
            )
        try:
            with open(self._app.config.path_to_highscore) as f:
                file = json.load(f)
                scores = sorted(file["highscores"],
                key=lambda entry: entry["score"], reverse=True)[:10]
        except Exception as e:
            scores = None
        if not scores:
            renderer.string_put(
                int(middle - 4 * self._app.character),
                150,
                0xFFFFFF,
                "No score yet")
            return
        i = 1
        for element in scores:
            height = 50 + i * 100
            renderer.string_put(
                int(middle - 20 * self._app.character),
                height,
                0xFFFFFF,
                f"{element["name"]} : "
                )
            renderer.string_put(
                int(middle + 15 * self._app.character),
                height,
                0xFFFFFF,
                f"{element["score"]}"
                )
            i += 1
            if i > 10:
                break
        super().draw(renderer)
