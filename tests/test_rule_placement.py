
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from src.core.state import State
from src.platform.base import Platform
from src.ui import overlay_window as ow
from src.ui.overlay_window import OverlayWindow


class FakePlatform(Platform):

    def set_click_through(self, enabled: bool) -> None:
        pass

    def set_always_on_top(self, enabled: bool) -> None:
        pass

    def get_screen_geometry(self):
        return None

@pytest.fixture(scope="module")
def app() -> QApplication:
    yield QApplication.instance() or QApplication([])

def _window(state: State) -> OverlayWindow:
    window = OverlayWindow(state, FakePlatform(None))
    window.resize(800, 600)
    return window

def _click(window: OverlayWindow, x: float, y: float, shift: bool = True) -> None:
    mods = (
        Qt.KeyboardModifier.ShiftModifier if shift else Qt.KeyboardModifier.NoModifier
    )
    event = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPointF(x, y),
        QPointF(x, y),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        mods,
    )
    window.mousePressEvent(event)
    # Los botones del panel ejecutan su acción tras el flash de 80 ms.
    QTest.qWait(110)

def _release(window: OverlayWindow) -> None:
    event = QMouseEvent(
        QEvent.Type.MouseButtonRelease,
        QPointF(0, 0),
        QPointF(0, 0),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )
    window.mouseReleaseEvent(event)

def _drag(window: OverlayWindow, x: float, y: float) -> None:
    event = QMouseEvent(
        QEvent.Type.MouseMove,
        QPointF(x, y),
        QPointF(x, y),
        Qt.MouseButton.NoButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.ShiftModifier,
    )
    window.mouseMoveEvent(event)

def _button_center(window: OverlayWindow, name: str) -> QPointF:
    window._panel_open = True
    window._panel_offset = float(ow.PANEL_WIDTH)
    for btn_name, rect in window._panel_buttons():
        if btn_name == name:
            return QPointF(rect.center().x(), rect.center().y())
    raise AssertionError(f"no existe el botón {name}")

def test_shift_click_without_armed_rule_creates_nothing(app: QApplication):
    state = State()
    window = _window(state)
    _click(window, 400, 300)
    assert state.rules == [], "Shift + click sin botón previo no debe crear reglas"

def test_click_on_rule_button_only_arms_the_rule(app: QApplication):
    state = State()
    window = _window(state)
    center = _button_center(window, "rule_h")
    _click(window, center.x(), center.y())
    assert window._armed_rule == ("h", -1)
    assert state.rules == [], "el click en el botón solo arma, no crea"

    _click(window, 250, 300, shift=False)
    assert len(state.rules) == 1
    assert state.rules[0].kind == "h"
    assert window._armed_rule is None, "sin Shift debe desarmarse al colocar"

def test_click_on_rect_button_then_canvas_places_that_rect(app: QApplication):
    state = State()
    window = _window(state)
    center = _button_center(window, "rule_rect_id")
    _click(window, center.x(), center.y())
    assert window._armed_rule == ("rect", 3)
    assert state.rules == []

    _click(window, 250, 300, shift=False)
    assert len(state.rules) == 1
    assert state.rules[0].kind == "rect"
    assert state.rules[0].corner == 3

def test_shift_keeps_the_rule_armed_for_several_in_a_row(app: QApplication):
    state = State()
    window = _window(state)
    center = _button_center(window, "rule_v")
    _click(window, center.x(), center.y(), shift=False)
    assert window._armed_rule == ("v", -1)
    assert state.rules == [], "el click en el botón solo arma, no crea"

    _click(window, 250, 300)
    assert len(state.rules) == 1
    assert state.rules[0].kind == "v"
    assert window._armed_rule == ("v", -1), "con Shift sigue armada"

    _click(window, 300, 400)
    assert len(state.rules) == 2, "Shift + clics seguidos dibujan varias"

def test_release_finishes_placement(app: QApplication):
    state = State()
    window = _window(state)
    center = _button_center(window, "rule_h")
    _click(window, center.x(), center.y())
    _click(window, 250, 300, shift=False)
    assert window._placing is not None, "al colocar queda en gesto de arrastre"
    _release(window)
    assert window._placing is None
    assert len(state.rules) == 1

def test_fuga_button_arms_and_shift_click_places_vanishing_point(app: QApplication):
    state = State()
    window = _window(state)
    center = _button_center(window, "rule_fuga")
    _click(window, center.x(), center.y(), shift=False)
    assert window._armed_rule == ("fuga", -1)
    assert state.rules == [], "el click en el botón solo arma, no crea"

    _click(window, 300, 200)
    assert len(state.rules) == 1
    assert state.rules[0].kind == "fuga"
    rule = state.rules[0]
    assert abs(rule.x - 300 / 800) < 0.01
    assert abs(rule.y - 200 / 600) < 0.01

    _drag(window, 100, 500)
    assert abs(rule.x - 100 / 800) < 0.01
    assert abs(rule.y - 500 / 600) < 0.01

def test_vertex_follows_the_drag(app: QApplication):
    state = State()
    window = _window(state)
    center = _button_center(window, "rule_h")
    _click(window, center.x(), center.y())
    _click(window, 250, 300)
    assert len(state.rules) == 1

    _drag(window, 200, 150)
    rule = state.rules[0]
    assert abs(rule.x - 200 / 800) < 0.01
    assert abs(rule.y - 150 / 600) < 0.01
