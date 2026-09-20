"""Reflection Panel Component for self-reflective RAG confidence and evaluation breakdown."""

from typing import Dict, Any
import streamlit as st
from .icons import get_icon


def render_reflection_panel(reflection: Dict[str, Any], expanded: bool = False):
    """Render self-reflection metrics: Relevance, Correctness, Groundedness, Completeness."""
    if not reflection:
        return

    rel = int(reflection.get("relevance", 0.95) * 100)
    corr = int(reflection.get("correctness", 0.95) * 100)
    grd = int(reflection.get("groundedness", 0.98) * 100)
    comp = int(reflection.get("completeness", 0.92) * 100)
    passed = reflection.get("passed", True)
    action = reflection.get("action", "ACCEPT")
    issues = reflection.get("issues", [])

    action_color = "#10b981" if action == "ACCEPT" else ("#f59e0b" if "REVIEW" in action else "#ef4444")

    with st.expander("Agent Self-Reflection & Quality Evaluation", expanded=expanded):
        st.markdown(
            f'<div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 8px; margin-top: 12px;">'
            f'<div style="display: flex; align-items: center; gap: 6px;">'
            f'{get_icon("sparkles", size=15, color="#6366f1")}'
            f'<span class="inv-cell-primary" style="font-size: 0.9rem;">Self-Evaluation Status:</span>'
            f'<span style="font-size: 0.85rem; font-weight: 700; color: {action_color}; background: {action_color}18; padding: 2px 8px; border-radius: 6px;">{action}</span>'
            f'</div>'
            f'<span style="font-size: 0.9rem; color: var(--st-text-secondary, #64748b);">LangGraph Reflection Node</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4, gap="xsmall")
        with c1:
            st.metric("Groundedness", f"{grd}%")
        with c2:
            st.metric("Relevance", f"{rel}%")
        with c3:
            st.metric("Correctness", f"{corr}%")
        with c4:
            st.metric("Completeness", f"{comp}%")

        if issues:
            st.markdown(
                f'<div class="audit-alert-warning" style="margin-top: 8px; font-size: 0.9rem; padding: 6px 10px; border-radius: 6px;">'
                f'<strong>Identified Concerns:</strong> {", ".join(issues)}'
                f'</div>',
                unsafe_allow_html=True,
            )
