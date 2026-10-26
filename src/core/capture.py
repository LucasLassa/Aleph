
from __future__ import annotations

import datetime
import re
import unicodedata
from pathlib import Path

from PySide6.QtCore import QStandardPaths
from PySide6.QtGui import QColor, QImage, QPainter

from src.core import guides, rules
from src.core.state import State
from src.platform.capture import ScreenGrabber


def default_capture_dir() -> Path:
    loc = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
    return Path(loc) if loc else Path.home() / "Downloads"

def capture_dir(state: State) -> Path:
    if state.capture_dir:
        return Path(state.capture_dir)
    return default_capture_dir()

def _slug_guide(state: State) -> str:
    if 0 <= state.guide_index < len(guides.POOL):
        name = guides.POOL[state.guide_index]
    else:
        name = "vacio"
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    name = re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_").lower()
    return name or "vacio"

def capture_filename(
    state: State,
    moment: datetime.datetime | None = None,
    counter: int = 1,
) -> str:
    moment = moment or datetime.datetime.now()
    return f"aleph_{_slug_guide(state)}_{moment.strftime('%Y-%m-%d_%H-%M-%S')}_{counter:03d}.png"

def overlay_on_image(
    image: QImage, state: State, color: QColor | None = None
) -> QImage:
    if color is None:
        color = QColor(0, 0, 0) if state.line_dark else QColor(255, 255, 255)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    guides.draw(painter, image.width(), image.height(), state, color=color)
    rules.draw(painter, image.width(), image.height(), state.rules, color)
    painter.end()
    return image

def capture_with_guides(
    grabber: ScreenGrabber, state: State
) -> tuple[QImage | None, Path | None]:
    pixmap = grabber.grab()
    if pixmap is None:
        return None, None
    image = pixmap if isinstance(pixmap, QImage) else pixmap.toImage()
    if image.isNull():
        return None, None
    overlay_on_image(image, state)
    target_dir = capture_dir(state)
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None, None
    moment = datetime.datetime.now()
    # Contador por día y guía: dos capturas en segundos distintos avanzan.
    day_prefix = f"aleph_{_slug_guide(state)}_{moment.strftime('%Y-%m-%d')}_"
    # Máximo existente + 1: un hueco en la serie no reutiliza números
    # (evita sobrescribir si el usuario borra una captura intermedia).
    max_counter = 0
    for p in target_dir.glob(f"{day_prefix}*.png"):
        try:
            num = int(p.stem.split("_")[-1])
        except ValueError:
            continue
        max_counter = max(max_counter, num)
    counter = max_counter + 1
    path = target_dir / capture_filename(state, moment, counter)
    if not image.save(str(path), "PNG"):
        return None, None
    return image, path
