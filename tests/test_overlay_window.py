
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication

from src.core import keymap
from src.core.state import State
from src.platform.base import Platform
from src.ui.overlay_window import OverlayWindow


class FakePlatform(Platform):

    def __init__(self) -> None:
        super().__init__(window=None)
        self.click_through: list[bool] = []

    def set_click_through(self, enabled: bool) -> None:
        self.click_through.append(enabled)

    def set_always_on_top(self, enabled: bool) -> None:
        pass

    def get_screen_geometry(self):
        return None

@pytest.fixture(scope="module")
def app() -> QApplication:
    yield QApplication.instance() or QApplication([])

def _toggle(window: OverlayWindow, state: State) -> None:
    assert keymap.handle("M", state, shift=True) == "toggle_frame"
    window.apply_frame_mode()

def test_frame_toggle_keeps_visible_and_fullscreen(app: QApplication):
    state = State()
    platform = FakePlatform()
    window = OverlayWindow(state, platform)
    window.showFullScreen()
    assert window.isVisible()
    assert window.isFullScreen()

    for click_through in (True, False, True, False):
        _toggle(window, state)
        assert window.isVisible(), "setWindowFlag oculta la ventana: falta show()"
        assert window.isFullScreen(), "alternar el marco no debe salir de fullscreen"
        assert state.frame_mode is not click_through
        assert platform.click_through[-1] is click_through

    assert platform.click_through == [True, False, True, False]

def _window(state: State) -> OverlayWindow:
    window = OverlayWindow(state, FakePlatform())
    window.resize(800, 600)
    return window

def _esc(window: OverlayWindow) -> None:
    window.keyPressEvent(
        QKeyEvent(
            QEvent.Type.KeyPress,
            Qt.Key.Key_Escape,
            Qt.KeyboardModifier.NoModifier,
        )
    )

def test_esc_closes_manual_before_anything(app: QApplication):
    window = _window(State())
    window.show()
    window.show_manual()
    assert window._manual is not None and window._manual.isVisible()
    _esc(window)
    assert not window._manual.isVisible(), "el Esc debe cerrar primero el manual"
    assert window.isVisible(), "con el manual abierto no debe cerrar Aleph"
    window.close()

def test_esc_disarms_an_armed_rule(app: QApplication):
    window = _window(State())
    window.show()
    window._armed_rule = ("h", -1)
    _esc(window)
    assert window._armed_rule is None, "el Esc debe desarmar la regla"
    assert window.isVisible()
    window.close()

def test_esc_closes_the_panel_before_quitting(app: QApplication):
    window = _window(State())
    window.show()
    window.toggle_panel()
    assert window._panel_open is True
    _esc(window)
    assert window._panel_open is False, "el Esc debe cerrar el panel antes de salir"
    assert window.isVisible()
    window.close()

def test_esc_leaves_movie_mode_before_quitting(app: QApplication):
    state = State(frame_mode=False)
    window = _window(state)
    window.show()
    _esc(window)
    assert state.frame_mode is True, "debe salir del modo película antes de cerrar"
    assert window.isVisible()
    window.close()

def test_esc_quits_when_nothing_is_open(app: QApplication):
    window = _window(State())
    window.show()
    _esc(window)
    assert not window.isVisible(), "Esc con todo cerrado cierra Aleph"
