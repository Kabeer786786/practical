"""Evidence Viewer Component for OCR text snippets, bounding boxes, and validation proof."""

from typing import List, Dict, Any
import streamlit as st
from .icons import get_icon


def render_evidence_viewer(evidence_items: List[Dict[str, Any]]):
    """Display extracted document evidence, OCR snippets, and validation proof cards."""
    if not evidence_items:
        return

    st.markdown(
        f'<div style="font-size: 0.9rem; font-weight: 500; color: var(--st-text-secondary, #64748b); margin: 12px 0 12px 0; display: flex; align-items: center; gap: 6px;">'
        f'{get_icon("file-text", size=14, color="#6366f1")} Extracted Evidence & OCR Records'
        f'</div>',
        unsafe_allow_html=True,
    )

    for item in evidence_items:
        source = item.get("source", "Document Snippet")
        snippet = item.get("snippet", item.get("text", ""))
        category = item.get("type", "Invoice OCR")
        confidence = item.get("confidence", 0.95)
        bbox = item.get("bbox", None)

        conf_pct = int(confidence * 100) if isinstance(confidence, float) else confidence
        conf_color = "#10b981" if conf_pct >= 90 else ("#f59e0b" if conf_pct >= 75 else "#ef4444")

        bbox_html = ""
        if bbox:
            bbox_html = (
                f'<span style="font-size: 0.7rem; color: var(--st-text-secondary, #64748b); font-family: monospace; background: var(--st-code-background-color, rgba(100,116,139,0.12)); border: 1px solid var(--st-border-color, rgba(100,116,139,0.2)); padding: 2px 6px; border-radius: 4px;">'
                f'BBox: [{bbox.get("x", 0)}, {bbox.get("y", 0)}, {bbox.get("w", 0)}, {bbox.get("h", 0)}]'
                f'</span>'
            )

        st.markdown(
            f'<div class="audit-card">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">'
            f'<span class="inv-cell-primary">{source}</span>'
            f'<div style="display: flex; align-items: center; gap: 8px;">'
            f'{bbox_html}'
            f'<span style="font-size: 0.72rem; font-weight: 700; color: {conf_color}; background: {conf_color}18; padding: 2px 8px; border-radius: 9999px;">'
            f'{conf_pct}% confidence'
            f'</span>'
            f'</div>'
            f'</div>'
            f'<div class="audit-card-code">'
            f'{snippet}'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.markdown(f'<div style="margin-bottom: 4px;"></div>', unsafe_allow_html=True)
