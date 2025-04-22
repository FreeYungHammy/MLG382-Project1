# package outline for dash
from .home      import layout as home_layout
from .analytics import layout as analytics_layout
from .info      import layout as info_layout
from .predict   import layout as predict_layout
from .feedback  import layout as feedback_layout

__all__ = [
    "home_layout",
    "analytics_layout",
    "info_layout",
    "predict_layout",
    "feedback_layout",
]
