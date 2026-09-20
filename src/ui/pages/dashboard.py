"""Dashboard Page for AI Invoice Auditor.

Presents high-level KPI cards, instant search and status filters, and an interactive
invoices table with vertically centered rows and deep-link routing.
"""

from typing import Optional, Callable
import streamlit as st
from components.icons import get_icon, icon_badge
from services.jobs_client import JobsClient


def render_dashboard(
    jobs_client: Optional[JobsClient] = None,
    on_select_invoice: Optional[Callable[[str], None]] = None,
):
    """Render the main invoice audit monitoring dashboard."""
    client = jobs_client or JobsClient()
    invoices = client.list_invoices()

    # Calculate metrics
    total = len(invoices)
    completed_count = sum(1 for inv in invoices if inv["status"] == "Completed")
    review_count = sum(1 for inv in invoices if inv["status"] == "Requires Review")
    progress_count = sum(1 for inv in invoices if inv["status"] == "In Progress")
    failed_count = sum(1 for inv in invoices if inv["status"] == "Validation Failed")

    # Header section
    st.markdown(
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px;">'
        f'<div>'
        f'<div style="display: flex; align-items: center; gap: 10px;">'
        f'<span style="padding: 8px; background: rgba(99, 102, 241, 0.1); border-radius: 10px; display: inline-flex;">'
        f'{get_icon("shield-check", size=26, color="#4f46e5")}'
        f'</span>'
        f'<span class="audit-title">AI Invoice Audit Dashboard</span>'
        f'</div>'
        f'<p class="audit-subtitle">Enterprise compliance verification, PO reconciliation & autonomous RAG audit trails.</p>'
        f'</div>'
        f'<div style="display: flex; align-items: center; gap: 12px;">'
        f'<span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.28); border-radius: 9999px; font-size: 0.8rem; font-weight: 600; color: #10b981;">'
        f'<span style="width: 8px; height: 8px; border-radius: 50%; background: #10b981; display: inline-block;"></span> 4 Pipeline Workers Active'
        f'</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 4 KPI Metric Cards
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    with kpi_col1:
        st.markdown(
            f'<div class="kpi-card kpi-card-success">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
            f'<span class="kpi-label">Completed</span>'
            f'{get_icon("check-circle", size=20, color="#10b981")}'
            f'</div>'
            f'<div class="kpi-val">{completed_count}</div>'
            f'<div style="margin-top: 6px; font-size: 0.85rem; color: #10b981; font-weight: 600;">100% PO & GST compliant</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with kpi_col2:
        st.markdown(
            f'<div class="kpi-card kpi-card-warning">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
            f'<span class="kpi-label">Requires Review</span>'
            f'{get_icon("alert-triangle", size=20, color="#f59e0b")}'
            f'</div>'
            f'<div class="kpi-val">{review_count}</div>'
            f'<div style="margin-top: 6px; font-size: 0.85rem; color: #d97706; font-weight: 600;">Action required (HITL gate)</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with kpi_col3:
        st.markdown(
            f'<div class="kpi-card kpi-card-info">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
            f'<span class="kpi-label">In Progress</span>'
            f'{get_icon("refresh-cw", size=20, color="#3b82f6")}'
            f'</div>'
            f'<div class="kpi-val">{progress_count}</div>'
            f'<div style="margin-top: 6px; font-size: 0.85rem; color: #2563eb; font-weight: 600;">Processing OCR & rules</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with kpi_col4:
        st.markdown(
            f'<div class="kpi-card kpi-card-danger">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
            f'<span class="kpi-label">Validation Failed</span>'
            f'{get_icon("x-circle", size=20, color="#ef4444")}'
            f'</div>'
            f'<div class="kpi-val">{failed_count}</div>'
            f'<div style="margin-top: 6px; font-size: 0.85rem; color: #dc2626; font-weight: 600;">Unrecoverable violations</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Space after KPIs
    st.markdown("<div style='height: 48px; min-height:40px;'></div>", unsafe_allow_html=True)

    # Search and Filter Bar
    filter_c1, filter_c2, filter_c3 = st.columns([3, 2, 1.2], vertical_alignment="center")

    with filter_c1:
        search_term = st.text_input(
            "Search Invoices",
            placeholder="Search by invoice #, vendor name, or PO number...",
            label_visibility="collapsed",
            key="dashboard_search_input",
        )

    with filter_c2:
        status_options = ["All Statuses", "Completed", "Requires Review", "In Progress", "Validation Failed"]
        selected_status = st.selectbox(
            "Status Filter",
            options=status_options,
            index=0,
            label_visibility="collapsed",
            key="dashboard_status_select",
        )

    with filter_c3:
        if st.button("Refresh", icon=":material/refresh:", use_container_width=True, key="dashboard_refresh_btn"):
            st.rerun()

    # Filter logic
    filtered_invoices = invoices
    if search_term:
        term = search_term.strip().lower()
        filtered_invoices = [
            inv for inv in filtered_invoices
            if term in inv["id"].lower()
            or term in inv["number"].lower()
            or term in inv["vendor"].lower()
            or term in inv["po_number"].lower()
        ]

    if selected_status != "All Statuses":
        filtered_invoices = [inv for inv in filtered_invoices if inv["status"] == selected_status]

    # Space after Search and Filter Bar
    st.markdown("<div style='height: 26px; min-height: 26px;'></div>", unsafe_allow_html=True)

    # Table Header Row
    st.markdown(
        f'<div class="inv-table-header">'
        f'<div>Invoice</div>'
        f'<div>Vendor & PO</div>'
        f'<div style="text-align: right;">Amount</div>'
        f'<div style="text-align: center;">Confidence</div>'
        f'<div style="text-align: center;">Status</div>'
        f'<div style="text-align: center;">Action</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Space after the Table Heading Row
    st.markdown("<div style='height: 14px; min-height: 14px;'></div>", unsafe_allow_html=True)

    if not filtered_invoices:
        st.markdown(
            f'<div class="inv-empty-state">'
            f'{get_icon("search", size=28, color="#94a3b8")}<br><br>'
            f'No invoices matched your filter criteria.'
            f'</div>',
            unsafe_allow_html=True,
        )
        return

    # Render Invoice Rows with total borders, bottom borders, and perfect vertical centering
    table_body = st.container()
    with table_body:
        st.markdown('<div id="inv-table-body-marker" style="display:none;"></div>', unsafe_allow_html=True)
        total_invs = len(filtered_invoices)
        for i, inv in enumerate(filtered_invoices):
            inv_id = inv["id"]
            inv_num = inv["number"]
            vendor = inv["vendor"]
            po_num = inv["po_number"]
            amt = f"{inv['currency']} {inv['amount']:,.2f}"
            conf = int(inv["confidence"] * 100)
            status = inv["status"]

            is_first = (i == 0)
            is_last = (i == total_invs - 1)
            first_id_attr = ' id="table-first-row-marker"' if is_first else ''
            last_id_attr = ' id="table-last-row-marker"' if is_last else ''

            # Status badge mapping
            if status == "Completed":
                badge = icon_badge("check-circle", "Passed", badge_type="success")
            elif status == "Requires Review":
                badge = icon_badge("alert-triangle", "Review Needed", badge_type="warning")
            elif status == "In Progress":
                badge = icon_badge("refresh-cw", "Processing", badge_type="info")
            else:
                badge = icon_badge("x-circle", "Failed", badge_type="danger")

            # Confidence color
            conf_color = "#10b981" if conf >= 90 else ("#f59e0b" if conf >= 75 else "#ef4444")

            # Row container with 6 columns vertically centered to perfection
            r1, r2, r3, r4, r5, r6 = st.columns([1.5, 2.4, 1.4, 1.2, 1.7, 1.4], vertical_alignment="center")

            with r1:
                st.markdown(
                    f'<span class="inv-table-row-marker"{first_id_attr}{last_id_attr} style="display:none;"></span>'
                    f'<div style="display: flex; flex-direction: column; justify-content: center; min-height: 48px;">'
                    f'<span class="inv-cell-primary">{inv_id}</span>'
                    f'<span class="inv-cell-muted">{inv_num}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            with r2:
                st.markdown(
                    f'<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; min-height: 48px; width: 100%;">'
                    f'<span class="inv-cell-secondary" style="text-align: center;">{vendor}</span>'
                    f'<span style="font-size: 0.8rem; color: #6366f1; font-weight: 500; display: inline-flex; align-items: center; justify-content: center; gap: 4px; margin-top: 3px; text-align: center;">'
                    f'{get_icon("layers", size=12, color="#6366f1")} {po_num}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            with r3:
                st.markdown(
                    f'<div class="inv-cell-amount" style="display: flex; align-items: center; justify-content: flex-end; min-height: 48px;">'
                    f'{amt}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            with r4:
                st.markdown(
                    f'<div style="display: flex; align-items: center; justify-content: center; min-height: 48px;">'
                    f'<span style="font-weight: 600; color: {conf_color}; font-size: 1rem; background: {conf_color}18; padding: 4px 10px; border-radius: 6px;">'
                    f'{conf}%'
                    f'</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            with r5:
                st.markdown(
                    f'<div style="display: flex; align-items: center; justify-content: center; min-height: 48px;">'
                    f'{badge}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            with r6:
                if st.button("View Pipeline", icon=":material/arrow_forward:", key=f"btn_view_{inv_id}", use_container_width=True):
                    st.query_params["id"] = inv_id
                    st.session_state.selected_invoice_id = inv_id
                    if on_select_invoice:
                        on_select_invoice(inv_id)
                    else:
                        st.session_state.page = "Invoice Detail"
                        st.rerun()


