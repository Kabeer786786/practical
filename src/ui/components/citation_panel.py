"""Citation Panel Component for displaying grounded source references and policy documents."""

from typing import List, Dict, Any, Union
import streamlit as st
from .icons import get_icon


def format_citation_pill(citation: Union[str, Dict[str, Any]]) -> str:
    """Format a single citation into a modern pill badge."""
    if isinstance(citation, dict):
        path = citation.get("path", "source_document")
        label = citation.get("title", path.split("/")[-1])
        doc_type = citation.get("type", "policy")
    else:
        path = str(citation)
        label = path.split("/")[-1]
        doc_type = "policy" if "rule" in path or ".md" in path else "record"

    bg_color = "rgba(99, 102, 241, 0.08)" if doc_type == "policy" else "rgba(16, 185, 129, 0.08)"
    border_color = "rgba(99, 102, 241, 0.25)" if doc_type == "policy" else "rgba(16, 185, 129, 0.25)"
    text_color = "#6366f1" if doc_type == "policy" else "#059669"
    icon_name = "shield-check" if doc_type == "policy" else "file-text"

    icon_svg = get_icon(icon_name, size=13, color=text_color)
    return (
        f'<span style="display: inline-flex; align-items: center; gap: 5px;'
        f'padding: 3px 10px; margin: 3px 4px 3px 0; border-radius: 6px; '
        f'background-color: {bg_color}; border: 1px solid {border_color}; '
        f'color: {text_color}; font-size: 0.72rem; font-weight: 500; font-family: monospace;" '
        f'title="Source: {path}">'
        f'{icon_svg} {label}'
        f'</span>'
    )


def render_citations(citations: List[Union[str, Dict[str, Any]]], title: str = "Grounding Sources & Citations"):
    """Render a clean row or expander of citation pills."""
    if not citations:
        return

    pills_html = "".join([format_citation_pill(c) for c in citations])
    st.markdown(
        f'<div style="margin-top: 16px; margin-bottom: 16px;">'
        f'<div style="font-size: 0.9rem; font-weight: 500; color: var(--st-text-secondary, #64748b); margin: 12px 0 3px 0; display: flex; align-items: center; gap: 6px;">'
        f'{get_icon("layers", size=13, color="#94a3b8")} {title}'
        f'</div>'
        f'<div style="display: flex; flex-wrap: wrap; align-items: center;">'
        f'{pills_html}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
