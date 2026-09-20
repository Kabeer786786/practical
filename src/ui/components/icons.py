"""Pure SVG vector icon system for enterprise UI styling.

Eliminates platform-dependent emoji rendering and provides crisp,
themeable SVG vector icons with customizable size, color, and CSS classes.
"""

from typing import Optional

ICONS = {
    "shield-check": (
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "file-text": (
        '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<line x1="16" x2="8" y1="13" y2="13"/>'
        '<line x1="16" x2="8" y1="17" y2="17"/>'
        '<line x1="10" x2="8" y1="9" y2="9"/>'
    ),
    "sparkles": (
        '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>'
        '<path d="M5 3v4"/>'
        '<path d="M19 17v4"/>'
        '<path d="M3 5h4"/>'
        '<path d="M17 19h4"/>'
    ),
    "git-branch": (
        '<line x1="6" x2="6" y1="3" y2="15"/>'
        '<circle cx="18" cy="6" r="3"/>'
        '<circle cx="6" cy="18" r="3"/>'
        '<path d="M18 9a9 9 0 0 1-9 9"/>'
    ),
    "layers": (
        '<polygon points="12 2 2 7 12 12 22 7 12 2"/>'
        '<polyline points="2 17 12 22 22 17"/>'
        '<polyline points="2 12 12 17 22 12"/>'
    ),
    "clock": (
        '<circle cx="12" cy="12" r="10"/>'
        '<polyline points="12 6 12 12 16 14"/>'
    ),
    "alert-triangle": (
        '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>'
        '<line x1="12" x2="12" y1="9" y2="13"/>'
        '<line x1="12" x2="12.01" y1="17" y2="17"/>'
    ),
    "check-circle": (
        '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>'
        '<polyline points="22 4 12 14.01 9 11.01"/>'
    ),
    "x-circle": (
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="15" x2="9" y1="9" y2="15"/>'
        '<line x1="9" x2="15" y1="9" y2="15"/>'
    ),
    "refresh-cw": (
        '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>'
        '<path d="M21 3v5h-5"/>'
        '<path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>'
        '<path d="M8 16H3v5"/>'
    ),
    "search": (
        '<circle cx="11" cy="11" r="8"/>'
        '<line x1="21" x2="16.65" y1="21" y2="16.65"/>'
    ),
    "filter": (
        '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>'
    ),
    "bot": (
        '<rect x="3" y="11" width="18" height="10" rx="2"/>'
        '<circle cx="12" cy="5" r="2"/>'
        '<path d="M12 7v4"/>'
        '<line x1="8" x2="8" y1="16" y2="16"/>'
        '<line x1="16" x2="16" y1="16" y2="16"/>'
    ),
    "plus": (
        '<line x1="12" x2="12" y1="5" y2="19"/>'
        '<line x1="5" x2="19" y1="12" y2="12"/>'
    ),
    "history": (
        '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>'
        '<path d="M3 3v5h5"/>'
        '<polyline points="12 7 12 12 15 15"/>'
    ),
    "send": (
        '<line x1="22" x2="11" y1="2" y2="13"/>'
        '<polygon points="22 2 15 22 11 13 2 9 22 2"/>'
    ),
    "x": (
        '<line x1="18" x2="6" y1="6" y2="18"/>'
        '<line x1="6" x2="18" y1="6" y2="18"/>'
    ),
    "chevron-right": (
        '<polyline points="9 18 15 12 9 6"/>'
    ),
    "arrow-left": (
        '<line x1="19" x2="5" y1="12" y2="12"/>'
        '<polyline points="12 19 5 12 12 5"/>'
    ),
    "terminal": (
        '<polyline points="4 17 10 11 4 5"/>'
        '<line x1="12" x2="20" y1="19" y2="19"/>'
    ),
    "database": (
        '<ellipse cx="12" cy="5" rx="9" ry="3"/>'
        '<path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>'
        '<path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>'
    ),
    "user-check": (
        '<path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>'
        '<circle cx="8.5" cy="7" r="4"/>'
        '<polyline points="17 11 19 13 23 9"/>'
    ),
    "external-link": (
        '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'
        '<polyline points="15 3 21 3 21 9"/>'
        '<line x1="10" x2="21" y1="14" y2="3"/>'
    ),
    "eye": (
        '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>'
        '<circle cx="12" cy="12" r="3"/>'
    ),
    "download": (
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="7 10 12 15 17 10"/>'
        '<line x1="12" x2="12" y1="15" y2="3"/>'
    ),
    "check": (
        '<polyline points="20 6 9 17 4 12"/>'
    ),
    "arrow-right": (
        '<line x1="5" y1="12" x2="19" y2="12"/>'
        '<polyline points="12 5 19 12 12 19"/>'
    ),
    "layout-dashboard": (
        '<rect width="7" height="9" x="3" y="3" rx="1"/>'
        '<rect width="7" height="5" x="14" y="3" rx="1"/>'
        '<rect width="7" height="9" x="14" y="12" rx="1"/>'
        '<rect width="7" height="5" x="3" y="16" rx="1"/>'
    ),
    "receipt": (
        '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/>'
        '<path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/>'
        '<path d="M12 17.5v-11"/>'
    ),
    "message-square": (
        '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'
    ),
    "activity": (
        '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>'
    ),
}


def get_icon(
    name: str,
    size: int = 16,
    color: str = "currentColor",
    extra_class: str = "",
    stroke_width: float = 2.0,
) -> str:
    """Return inline SVG HTML string for the requested icon name.

    If name is not found, defaults to 'file-text'.
    """
    path_data = ICONS.get(name, ICONS.get("file-text"))
    cls_attr = f' class="svg-icon {extra_class}"' if extra_class else ' class="svg-icon"'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
        f'width="{size}" height="{size}" fill="none" stroke="{color}" '
        f'stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"'
        f'{cls_attr} style="vertical-align: -0.15em; display: inline-block;">'
        f'{path_data}'
        f'</svg>'
    )


def icon_badge(
    name: str,
    label: str,
    badge_type: str = "default",
    size: int = 14,
) -> str:
    """Return an interactive/clean styled badge containing the icon and text label."""
    color_map = {
        "success": ("#10b981", "rgba(16, 185, 129, 0.12)", "#059669"),
        "warning": ("#f59e0b", "rgba(245, 158, 11, 0.12)", "#d97706"),
        "danger": ("#ef4444", "rgba(239, 68, 68, 0.12)", "#dc2626"),
        "info": ("#3b82f6", "rgba(59, 130, 246, 0.12)", "#2563eb"),
        "purple": ("#8b5cf6", "rgba(139, 92, 246, 0.12)", "#7c3aed"),
        "default": ("#64748b", "rgba(100, 116, 139, 0.12)", "#475569"),
    }
    stroke_color, bg_color, _ = color_map.get(badge_type, color_map["default"])
    icon_svg = get_icon(name, size=size, color=stroke_color)
    return (
        f'<span style="display: inline-flex; align-items: center; gap: 6px; '
        f'padding: 3px 10px; border-radius: 9999px; background-color: {bg_color}; '
        f'color: {stroke_color}; font-size: 0.78rem; font-weight: 600; '
        f'border: 1px solid {bg_color}; letter-spacing: 0.02em;">'
        f'{icon_svg}<span>{label}</span>'
        f'</span>'
    )
