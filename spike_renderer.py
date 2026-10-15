"""Throwaway test of the Renderer (not part of the game)."""

from src.graphical.renderer import Renderer, RendererError

renderer = Renderer(640, 480, "Test renderer")
wall = renderer.new_filled_image(32, 32, 0x2121DE)   # carré bleu

running = True
while running:
    for event in renderer.poll_events():
        print(event)
        if event.kind == "quit" or event.key == "escape":
            running = False

    renderer.clear()
    renderer.put_image(wall, 100, 100)
    renderer.string_put(20, 20, 0xFFFF00, "Pac-Man")
    renderer.present()

renderer.close()
