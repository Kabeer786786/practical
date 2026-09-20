"""Job Detail Page — GitHub Actions-style pipeline execution timeline for AI Invoice Auditor."""

import json
from typing import Optional, Callable
import streamlit as st
from components.icons import get_icon, icon_badge
from components.citation_panel import render_citations
from components.evidence_viewer import render_evidence_viewer
from components.reflection_panel import render_reflection_panel
from services.jobs_client import JobsClient


def render_job_detail(
    invoice_id: Optional[str] = None,
    jobs_client: Optional[JobsClient] = None,
    on_back: Optional[Callable[[], None]] = None,
):
    """Render the GitHub Actions-style pipeline execution timeline for the selected invoice."""
    client = jobs_client or JobsClient()

    # Resolve invoice ID from query param, argument, or session state
    target_id = st.query_params.get("id") or invoice_id or st.session_state.get("selected_invoice_id", "INV-1042")
    inv = client.get_invoice(target_id)

    if not inv:
        st.error(f"Invoice '{target_id}' not found.")
        if st.button("Back to Dashboard", icon=":material/arrow_back:"):
            st.query_params.clear()
            if on_back:
                on_back()
            else:
                st.session_state.page = "Dashboard"
                st.rerun()
        return

    # Top Navigation: Solo Back to Dashboard Button
    if st.button("Back to Dashboard", icon=":material/arrow_back:", key="job_detail_back_btn"):
        st.query_params.clear()
        if on_back:
            on_back()
        else:
            st.session_state.page = "Dashboard"
            st.rerun()

    # Invoice Audit Banner with Status Colors, Animated Loader & Real Invoice Data
    status = inv.get("status", "Requires Review")
    conf = int(inv.get("confidence", 0.9) * 100)
    conf_color = "#10b981" if conf >= 90 else ("#f59e0b" if conf >= 75 else "#ef4444")

    if status in ("Completed", "Validated"):
        banner_status_cls = "status-validated"
        border_col = "#10b981"
        status_right_html = (
            f'<div style="display: flex; flex-direction: column; align-items: flex-end; gap: 5px;">'
            f'<span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 9999px; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); color: #10b981; font-size: 0.82rem; font-weight: 700;">'
            f'{get_icon("check-circle", size=15, color="#10b981")}'
            f'<span>Passed</span>'
            f'</span>'
            f'<span style="font-size: 0.74rem; color: #10b981; font-weight: 500;">100% PO & Tax Compliant</span>'
            f'</div>'
        )
    elif status == "Requires Review":
        banner_status_cls = "status-review"
        border_col = "#f59e0b"
        status_right_html = (
            f'<div style="display: flex; flex-direction: column; align-items: flex-end; gap: 5px;">'
            f'<span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 9999px; background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.35); color: #f59e0b; font-size: 0.82rem; font-weight: 700;">'
            f'{get_icon("alert-triangle", size=15, color="#f59e0b")}'
            f'<span>Requires Review</span>'
            f'</span>'
            f'<span style="font-size: 0.9rem; color: #f59e0b; font-weight: 500;">HITL Gate Triggered</span>'
            f'</div>'
        )
    elif status in ("In Progress", "Processing"):
        banner_status_cls = "status-processing"
        border_col = "#3b82f6"
        status_right_html = (
            f'<div style="display: flex; flex-direction: column; align-items: flex-end; gap: 5px;">'
            f'<span style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 9999px; background: rgba(59, 130, 246, 0.12); border: 1px solid rgba(59, 130, 246, 0.35); color: #3b82f6; font-size: 0.82rem; font-weight: 700; letter-spacing: 0.02em;">'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="animation: spinStepProgress 1.2s linear infinite;">'
            f'<path d="M21 12a9 9 0 1 1-6.219-8.56"/>'
            f'</svg>'
            f'<span>In Progress</span>'
            f'</span>'
            f'<span style="font-size: 0.9rem; color: #3b82f6; font-weight: 500; font-family: monospace;">Pipeline Active</span>'
            f'</div>'
        )
    else:
        banner_status_cls = "status-failed"
        border_col = "#ef4444"
        status_right_html = (
            f'<div style="display: flex; flex-direction: column; align-items: flex-end; gap: 5px;">'
            f'<span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 9999px; background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.35); color: #ef4444; font-size: 0.82rem; font-weight: 700;">'
            f'{get_icon("x-circle", size=15, color="#ef4444")}'
            f'<span>Validation Failed</span>'
            f'</span>'
            f'<span style="font-size: 0.9rem; color: #ef4444; font-weight: 500;">Policy Violations</span>'
            f'</div>'
        )

    category_str = inv.get("category", "General Supplies")
    gstin_str = inv.get("vendor_gstin", inv.get("vendor_id", "N/A"))
    date_str = inv.get("date", "N/A")
    due_date_str = inv.get("due_date", "N/A")
    amt_str = f"{inv['currency']} {inv['amount']:,.2f}"

    st.markdown(
        f'<div class="pipeline-banner {banner_status_cls}" style="border-left: 4px solid {border_col} !important; border-left-color: {border_col} !important; box-shadow: none !important; margin-top:12px;">'
        f'<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">'
        f'<div>'
        f'<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px; flex-wrap: wrap;">'
        f'<span style="padding: 7px; background: rgba(99, 102, 241, 0.12); border-radius: 8px; display: inline-flex;">'
        f'{get_icon("file-text", size=20, color="#6366f1")}'
        f'</span>'
        f'<h2 class="audit-title" style="font-size: 1.35rem; margin: 0;">{inv["id"]} &mdash; {inv["vendor"]}</h2>'
        f'<span class="pipeline-tag">{inv["number"]}</span>'
        f'</div>'
        f'<div style="font-size: 1rem; color: var(--st-text-muted, #94a3b8); margin-bottom: 10px;">'
        f'Category: <span style="color: var(--st-text-secondary)"><strong>{category_str}</strong></span> &nbsp;&nbsp;&nbsp; &bull; &nbsp; Vendor GSTIN / Tax ID: <span style="color: var(--st-text-secondary)"><strong>{gstin_str}</strong  ></span> &nbsp;&nbsp;&nbsp; &bull; &nbsp; Invoice Date: <span style="color: var(--st-text-secondary)"><strong>{date_str}</strong></span>'
        f'</div>'
        f'<div style="font-size: 1rem; color: var(--st-text-secondary, #64748b); display: flex; align-items: center; gap: 18px; flex-wrap: wrap;">'
        f'<span>PO Ref: <strong style="color: #6366f1;">{inv["po_number"]}</strong></span>'
        f'<span>Total Amount: <strong class="inv-cell-primary" style="font-family: monospace;">{amt_str}</strong></span>'
        f'<span>Extraction Confidence: <strong style="color: {conf_color}; font-weight: 700;">{conf}%</strong></span>'
        f'<span>Audit Duration: <strong class="inv-cell-secondary">{inv["total_duration"]}</strong></span>'
        f'<span>Due Date: <strong class="inv-cell-secondary">{due_date_str}</strong></span>'
        f'</div>'
        f'</div>'
        f'{status_right_html}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Discrepancy Highlight / Alert Box if applicable
    if status in ("Requires Review", "Validation Failed"):
        alert_class = "audit-alert-warning" if status == "Requires Review" else "audit-alert-danger"
        alert_border = "#f59e0b" if status == "Requires Review" else "#ef4444"
        alert_icon = "alert-triangle" if status == "Requires Review" else "x-circle"
        alert_title = "Compliance Flagged for Human Review" if status == "Requires Review" else "Compliance Validation Failed"

        st.markdown(
            f'<div class="{alert_class}">'
            f'<div style="display: flex; align-items: center; gap: 8px; font-weight: 700; color: {alert_border}; font-size: 0.92rem; margin-bottom: 4px;">'
            f'{get_icon(alert_icon, size=18, color=alert_border)} {alert_title}'
            f'</div>'
            f'<div style="font-size: 0.9rem; line-height: 1.45;">{inv["discrepancy_summary"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Steps Execution Timeline Header
    st.markdown(
        f'<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">'
        f'{get_icon("layers", size=18, color="#4f46e5")}'
        f'<h3 class="audit-title" style="font-size: 1.15rem;">Pipeline Step Execution Timeline</h3>'
        f'</div>',
        unsafe_allow_html=True,
    )

    steps = client.get_job_steps(target_id)

    with st.container():
        st.markdown('<div id="steps-timeline-marker"></div>', unsafe_allow_html=True)
        for i, step in enumerate(steps, 1):
            step_status = step["status"]
            dur = step.get("duration", "--")

            if step_status == "success":
                step_icon = ":material/check_circle:"
                status_tag = "success"
                dur_display = dur
            elif step_status in ("warning", "waiting_review"):
                step_icon = ":material/warning:"
                status_tag = "warning"
                dur_display = dur
            elif step_status == "failed":
                step_icon = ":material/error:"
                status_tag = "failed"
                dur_display = dur
            elif step_status == "in_progress":
                step_icon = ":material/refresh:"
                status_tag = "in_progress"
                dur_display = dur
            else:
                step_icon = ":material/schedule:"
                status_tag = "waiting"
                dur_display = dur

            expanded_default = (step_status in ("warning", "waiting_review", "failed"))
            expander_label = f"{step['name']} `{dur_display}`"

            # Preceding marker guarantees expander left border & badge color match even when collapsed
            st.markdown(f'<div class="step-marker" data-status="{status_tag}" style="display:none;"></div>', unsafe_allow_html=True)

            with st.expander(expander_label, expanded=expanded_default, icon=step_icon):
                st.markdown(f'<div class="step-status-tag" data-status="{status_tag}"></div>', unsafe_allow_html=True)
                tab_logs, tab_io, tab_artifacts = st.tabs(["Terminal Console Logs", "Inputs & Outputs", "Artifacts & Evidence"])

                # Tab 1: Console Logs
                with tab_logs:
                    logs_formatted = "\n".join(step["logs"])
                    st.markdown(
                        f'<div style="background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 14px; font-family: monospace; font-size: 0.8rem; line-height: 1.6; max-height: 300px; overflow-y: auto; border: 1px solid #334155;margin-bottom:16px; ">'
                        f'<pre style="margin: 0; white-space: pre-wrap;">{logs_formatted}</pre>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                # Tab 2: Inputs & Outputs JSON
                with tab_io:
                    io_c1, io_c2 = st.columns(2)
                    with io_c1:
                        st.markdown("<strong>Step Input Payload</strong>", unsafe_allow_html=True)
                        st.json(step["inputs_outputs"].get("input", {}))
                    with io_c2:
                        st.markdown("<strong>Step Output Results</strong>", unsafe_allow_html=True)
                        st.json(step["inputs_outputs"].get("output", {}))

                # Tab 3: Artifacts & Evidence
                with tab_artifacts:
                    art_list = step.get("artifacts", [])
                    if art_list:
                        st.markdown("<strong>Generated Artifacts</strong>", unsafe_allow_html=True)
                        for art in art_list:
                            st.markdown(
                                f'<div class="artifact-item">'
                                f'<span style="font-family: monospace; font-size: 0.8rem; display: inline-flex; align-items: center; gap: 6px;">{get_icon("file-text", size=14, color="#6366f1")} {art["name"]}</span>'
                                f'<span class="inv-cell-muted">{art["size"]}</span>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )

                    bboxes = step.get("bounding_boxes", [])
                    if bboxes:
                        render_evidence_viewer([
                            {"source": b["label"], "snippet": b["text"], "bbox": b["bbox"], "confidence": inv["confidence"]}
                            for b in bboxes
                        ])
                    st.markdown(f'<div style="margin-bottom: 2px;"></div>', unsafe_allow_html=True )

    # Human-in-the-Loop Review Decision Gate
    st.markdown(
        f'<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">'
        f'{get_icon("user-check", size=20, color="#4f46e5")}'
        f'<h3 class="audit-title" style="font-size: 1.15rem;">Human-in-the-Loop (HITL) Decision Gate</h3>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if inv.get("review_decision"):
        rec = inv["review_decision"]
        st.success(
            f"Decision recorded: **{rec.get('decision', 'Approved')}** by {rec.get('user', 'Compliance Officer')} "
            f"at {rec.get('timestamp', 'recent')}. Notes: {rec.get('notes', 'None')}"
        )
    else:
        with st.form(key=f"hitl_form_{target_id}"):
            st.markdown(
                '<p style="font-size: 0.86rem; color: var(--st-text-secondary, #64748b); margin-bottom: 14px;">'
                'As an authorized Compliance Officer, submit your determination to either override tolerance thresholds, '
                'reject the invoice, or request an amended credit memo from the vendor.'
                '</p>',
                unsafe_allow_html=True,
            )

            notes = st.text_area("Audit Rationale & Justification Notes", placeholder="e.g. Rate variance confirmed with procurement manager via email ticket #9924...")
            officer_name = st.text_input("Reviewer Identity", value="Compliance Officer (compliance.desk@enterprise.internal)")

            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                approve_sub = st.form_submit_button("Approve with Override", icon=":material/check_circle:", use_container_width=True)
            with btn_col2:
                reject_sub = st.form_submit_button("Reject Invoice", icon=":material/cancel:", use_container_width=True)
            with btn_col3:
                correct_sub = st.form_submit_button("Request Correction", icon=":material/sync:", use_container_width=True)

            if approve_sub:
                client.update_decision(target_id, "Approve with Override", notes or "Approved by Compliance Officer.", user=officer_name)
                st.success("Invoice approved with override. Queued for ERP accounts payable payment batch.")
                st.rerun()
            elif reject_sub:
                client.update_decision(target_id, "Reject Invoice", notes or "Rejected due to policy violation.", user=officer_name)
                st.error("Invoice marked as Rejected. Automated notification dispatched to vendor accounts team.")
                st.rerun()
            elif correct_sub:
                client.update_decision(target_id, "Request Correction", notes or "Revision requested from vendor.", user=officer_name)
                st.warning("Invoice placed on hold. Request for correction ticket created.")
                st.rerun()

