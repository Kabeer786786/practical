"""Agent Trace Component for displaying step-by-step reasoning and LangGraph node executions."""

from typing import List, Dict, Any, Union
import streamlit as st
from .icons import get_icon


def render_agent_trace(trace_steps: List[Union[str, Dict[str, Any]]], expanded: bool = False):
    """Render agent reasoning steps as clean numbered breadcrumbs with expander."""
    if not trace_steps:
        return

    step_count = len(trace_steps)
    summary_label = f"Agent Reasoning Trace ({step_count} steps executed)"

    with st.expander(summary_label, expanded=expanded):
        st.markdown(
            f'<div style="font-size: 0.9rem; color: var(--st-text-secondary, #64748b);margin-top:10px; margin-bottom: 10px;">'
            f'LangGraph orchestration trace & tool invocations:'
            f'</div>',
            unsafe_allow_html=True,
        )

        for i, step in enumerate(trace_steps, 1):
            if isinstance(step, dict):
                title = step.get("title", step.get("step", f"Step {i}"))
                desc = step.get("detail", "")
                status = step.get("status", "completed")
                duration = step.get("duration", "")
            else:
                title = str(step)
                desc = ""
                status = "completed"
                duration = ""

            status_icon = get_icon("check-circle", size=14, color="#10b981") if status == "completed" else get_icon("clock", size=14, color="#3b82f6")
            time_badge = f'<span style="font-size: 0.72rem; color: var(--st-text-muted, #94a3b8); margin-left: auto; font-family: monospace;">{duration}</span>' if duration else ""

            desc_html = f'<div style="font-size: 0.8rem; color: var(--st-text-secondary, #64748b); margin-top: 2px; margin-left: 26px;">{desc}</div>' if desc else ""

            st.markdown(
                f'<div class="agent-trace-step">'
                f'<div style="display: flex; align-items: center; gap: 8px;">'
                f'<span style="display: inline-flex; align-items: center; justify-content: center; width: 20px; height: 20px; border-radius: 50%; background: rgba(99, 102, 241, 0.15); color: #818cf8; font-size: 0.72rem; font-weight: 700;">{i}</span>'
                f'<span class="inv-cell-primary" style="font-size: 0.85rem;">{title}</span>'
                f'{status_icon}'
                f'{time_badge}'
                f'</div>'
                f'{desc_html}'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown(f'<div style="padding-bottom: 4px;"></div>', unsafe_allow_html=True)
