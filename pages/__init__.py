from .home      import layout as home_layout
from .analytics import layout as analytics_layout
from .info      import layout as info_layout
from .predict   import layout as predict_layout, register_callbacks as register_predict
from .feedback  import layout as feedback_layout, register_callbacks as register_feedback

__all__ = [
    "home_layout",
    "analytics_layout",
    "info_layout",
    "predict_layout","register_predict",
    "feedback_layout","register_feedback",
]
