from pygame import Surface, Rect
from pygame.font import Font, SysFont


FONT16 = SysFont(None, 16)
FONT24 = SysFont(None, 24)
FONT32 = SysFont(None, 32)


class Label:
    def __init__(self, text, topleft, font: Font = FONT32, text_color=(0, 0, 0)):
        self.text = text
        self.font = font
        self.text_color = text_color
        self._surf, self._rect = _render_text(text, topleft, font, text_color)

    def set_text(self, text):
        self._surf, self._rect = _render_text(text, self._rect.topleft, self.font, self.text_color)

    def draw(self, surface: Surface):
        surface.blit(self._surf, self._rect)


def _render_text(text: str, topleft, font: Font, text_color=(0, 0, 0)) -> (Surface, Rect):
    surf = font.render(text, True, text_color)
    rect = surf.get_rect(topleft=topleft)
    return surf, rect
