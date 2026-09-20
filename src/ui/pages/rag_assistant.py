"""Floating RAG Copilot Chatbot Drawer.

Layout (all sizing is done by CSS flexbox in app.py, no hardcoded heights):
  ┌──────────────────────────────────────────────┐
  │ [+ New] [History] [ Thread title ...... ] [✕]│  <- copilot_top    (fixed)
  ├──────────────────────────────────────────────┤
  │  chat messages ...                           │  <- copilot_body   (fills, scrolls)
  ├──────────────────────────────────────────────┤
  │  [ input ................................ ]  │  <- copilot_bottom (fixed)
  │  [ scope selector ]           [ Send ]       │
  └──────────────────────────────────────────────┘

The dialog panel itself is docked bottom-right and styled entirely by CSS in
app.py, using structural :has() selectors keyed off the `.st-key-copilot_root`
container below. There is no JS "tag the DOM" step — CSS matches the panel
synchronously on first paint, so there's no flash of Streamlit's default
centered dialog before the styling applies.
"""

import html
import time
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

from components.icons import get_icon
from components.citation_panel import render_citations
from components.agent_trace import render_agent_trace
from components.reflection_panel import render_reflection_panel
from components.evidence_viewer import render_evidence_viewer
from services.rag_client import RAGClient
from services.jobs_client import JobsClient


def request_scroll_to_bottom():
    """Ask the next render of the drawer to scroll the chat to the latest message."""
    st.session_state.copilot_scroll_bottom = True


def _inject_scroll_to_bottom():
    """Smooth-scroll the chat body to the bottom via a zero-height iframe."""
    components.html(
        f"""
        <script>
        // run id: {time.time_ns()}
        (function () {{
            const doc = window.parent.document;
            let tries = 0;
            function scrollDown() {{
                const el = doc.querySelector('.st-key-copilot_body');
                if (el) {{
                    el.scrollTo({{ top: el.scrollHeight, behavior: 'smooth' }});
                }}
                if (++tries < 4) setTimeout(scrollDown, 150);
            }}
            scrollDown();
        }})();
        </script>
        """,
        height=0,
    )


def close_drawer():
    """Close the chat drawer."""
    st.session_state.show_chat = False


def _render_empty_state():
    st.markdown(
        f'<div class="copilot-empty-state">'
        f'<div style="width: 64px; height: 64px; border-radius: 50%; '
        f'background: linear-gradient(135deg, rgba(99,102,241,0.18) 0%, rgba(129,140,248,0.08) 100%); '
        f'display: flex; align-items: center; justify-content: center; margin-bottom: 16px; '
        f'box-shadow: 0 4px 20px rgba(99,102,241,0.2);">'
        f'{get_icon("sparkles", size=36, color="#6366f1")}'
        f'</div>'
        f'<h3 style="font-size: 1.5rem; font-weight: 600; color: inherit; margin: 0 0 8px 0; '
        f'letter-spacing: 0.01em; line-height: 1.3;">How can I assist with your audit?</h3>'
        f'<p style="font-size: 0.95rem; color: var(--st-text-secondary, #94a3b8); max-width: 380px; '
        f'line-height: 1.5; margin: 0 0 20px 0;">'
        f'Ask about PO variances, GST compliance, line item pricing, or policy rules.</p>'
        f'<div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; max-width: 420px;">'
        f'<span style="font-size: 0.85rem; font-weight: 500; padding: 5px 12px; border-radius: 9999px; '
        f'background: rgba(99,102,241,0.08); color: #818cf8; border: 1px solid rgba(99,102,241,0.2);">PO matching rules</span>'
        f'<span style="font-size: 0.85rem; font-weight: 500; padding: 5px 12px; border-radius: 9999px; '
        f'background: rgba(16,185,129,0.08); color: #34d399; border: 1px solid rgba(16,185,129,0.2);">Tax code checks</span>'
        f'<span style="font-size: 0.85rem; font-weight: 500; padding: 5px 12px; border-radius: 9999px; '
        f'background: rgba(245,158,11,0.08); color: #fbbf24; border: 1px solid rgba(245,158,11,0.2);">Vendor variance</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_user_message(content: str):
    st.markdown(
        f'<div class="chat-user-bubble">{html.escape(str(content))}</div>',
        unsafe_allow_html=True,
    )


def _render_bot_message(index: int, msg: dict):
    """One assistant response = one card: header, answer, sources, trace, reflection, evidence."""
    content = str(msg.get("content", ""))
    # "$" would start LaTeX in st.markdown, so escape it (prices like $0.42 / $1,500.00)
    content = content.replace("$", "\\$")

    header = (
        '<div class="bot-head">'
        f'<span class="bot-avatar">{get_icon("bot", size=13, color="#ffffff")}</span>'
        '<span class="bot-name">AI Copilot</span>'
        '</div>'
    )

    with st.container(key=f"bot_msg_{index}"):
        st.markdown(header, unsafe_allow_html=True)

        with st.container(key=f"bot_answer_{index}"):
            st.markdown(content)

        if msg.get("citations"):
            render_citations(msg["citations"])
        if msg.get("trace"):
            render_agent_trace(msg["trace"])
        if msg.get("reflection"):
            render_reflection_panel(msg["reflection"])
        if msg.get("evidence"):
            render_evidence_viewer(msg["evidence"])


@st.dialog("Audit Copilot", width="large")
def render_rag_drawer(
    rag_client: Optional[RAGClient] = None,
    jobs_client: Optional[JobsClient] = None,
):
    """Render the floating conversational copilot drawer."""
    client = rag_client or RAGClient()
    j_client = jobs_client or JobsClient()
    invoices = j_client.list_invoices()

    # ------------------------------------------------------------------
    # Thread state
    # ------------------------------------------------------------------
    threads = client.list_threads()
    if (
        "active_thread_id" not in st.session_state
        or not client.get_thread(st.session_state.active_thread_id)
    ):
        st.session_state.active_thread_id = (
            threads[0]["id"] if threads else client.create_thread()
        )

    active_thread = client.get_thread(st.session_state.active_thread_id)

    # This container is the anchor CSS uses (via :has()) to find and style
    # the real dialog panel structurally — no JS tagging required.
    root = st.container(key="copilot_root")

    # ==================================================================
    # 1. TOP SECTION: New | History (thread title) | Close (far right)
    # ==================================================================
    with root.container(key="copilot_top"):
        top_c1, top_c2, top_c3 = st.columns(
            [1, 6, 1],
            vertical_alignment="center",
        )

        with top_c1:
            if st.button(
                "New",
                icon=":material/add:",
                key="copilot_btn_new",
                help="Start new thread",
            ):
                new_id = client.create_thread(title="New Audit Inquiry")
                st.session_state.active_thread_id = new_id
                st.rerun(scope="fragment")

        with top_c2:
            title_text = html.escape(
                active_thread["title"] if active_thread else "Copilot Thread"
            )
            with st.popover(
                title_text,
                icon=":material/history:",
                help="Recent audit threads",
            ):
                st.markdown(
                    "<div style='font-size: 0.75rem; font-weight: 700; "
                    "color: var(--st-text-secondary, #64748b); text-transform: uppercase; "
                    "letter-spacing: 0.05em; margin: 4px 0 20px 2px;'>Recent Audit Threads</div>",
                    unsafe_allow_html=True,
                )
                if not threads:
                    st.markdown(
                        "<div style='font-size: 0.8rem; color: var(--st-text-muted, #94a3b8); "
                        "padding: 8px 0;'>No threads yet. Click New to start one.</div>",
                        unsafe_allow_html=True,
                    )
                for t in threads:
                    is_active = t["id"] == st.session_state.active_thread_id
                    t_c1, t_c2 = st.columns([3.8, 1], vertical_alignment="center")
                    with t_c1:
                        prefix_icon = (
                            ":material/radio_button_checked:"
                            if is_active
                            else ":material/chat:"
                        )
                        if st.button(
                            t["title"],
                            icon=prefix_icon,
                            key=f"pop_t_{t['id']}",
                            use_container_width=True,
                        ):
                            st.session_state.active_thread_id = t["id"]
                            request_scroll_to_bottom()
                            st.rerun(scope="fragment")
                    with t_c2:
                        if st.button(
                            "",
                            icon=":material/delete:",
                            key=f"del_t_{t['id']}",
                            help="Delete thread",
                            use_container_width=True,
                        ):
                            client.delete_thread(t["id"])
                            remaining = client.list_threads()
                            if st.session_state.active_thread_id == t["id"]:
                                st.session_state.active_thread_id = (
                                    remaining[0]["id"]
                                    if remaining
                                    else client.create_thread()
                                )
                            st.rerun(scope="fragment")

        with top_c3:
            # Close button aligned right
            if st.button(
                "",
                icon=":material/close:",
                key="copilot_btn_close",
                help="Close Copilot",
                use_container_width=True,
            ):
                close_drawer()
                st.rerun()

    # ==================================================================
    # 2. MIDDLE SECTION: fills the remaining height, scrolls smoothly
    # ==================================================================
    messages = active_thread.get("messages", []) if active_thread else []

    with root.container(key="copilot_body"):
        if not messages:
            _render_empty_state()

        for i, msg in enumerate(messages):
            if msg.get("role", "assistant") == "user":
                _render_user_message(msg.get("content", ""))
            else:
                _render_bot_message(i, msg)

        if st.session_state.pop("copilot_scroll_bottom", False):
            _inject_scroll_to_bottom()

    # ==================================================================
    # 3. BOTTOM SECTION: input box pinned to the bottom of the dialog
    # ==================================================================
    with root.container(key="copilot_bottom"):
        with st.form(
            key=f"fixed_chat_form_{st.session_state.active_thread_id}",
            clear_on_submit=True,
        ):
            user_query = st.text_input(
                "Audit Inquiry",
                placeholder="Ask question grounded in PO & tax policy...",
                label_visibility="collapsed",
            )

            b_c1, b_c2 = st.columns([2.6, 1], vertical_alignment="center")

            with b_c1:
                scope_options = ["All Invoices (Global Scope)"] + [
                    f"{inv['id']} ({inv['vendor'][:12]}..)" for inv in invoices
                ]
                current_scope_idx = 0
                if "selected_invoice_id" in st.session_state:
                    for idx, opt in enumerate(scope_options):
                        if opt.startswith(st.session_state.selected_invoice_id):
                            current_scope_idx = idx
                            break

                chosen_scope = st.selectbox(
                    "Scope",
                    options=scope_options,
                    index=current_scope_idx,
                    label_visibility="collapsed",
                )

            with b_c2:
                send_btn = st.form_submit_button(
                    "Send", icon=":material/send:", use_container_width=True
                )

            if send_btn and user_query:
                inv_scope_id = None
                if chosen_scope != "All Invoices (Global Scope)":
                    inv_scope_id = chosen_scope.split(" ")[0]

                active_thread["messages"].append(
                    {"role": "user", "content": user_query}
                )

                response = client.ask(
                    question=user_query,
                    invoice_id=inv_scope_id,
                    thread_id=active_thread["id"],
                )

                active_thread["messages"].append(
                    {
                        "role": "assistant",
                        "content": response.get("answer", "Response synthesized."),
                        "citations": response.get("citations", []),
                        "trace": response.get("trace", []),
                        "reflection": response.get("reflection", {}),
                        "evidence": response.get("evidence", []),
                    }
                )
                active_thread["updated_at"] = "Just now"

                if len(active_thread["messages"]) <= 2:
                    active_thread["title"] = user_query[:26] + (
                        "..." if len(user_query) > 26 else ""
                    )

                request_scroll_to_bottom()
                st.rerun(scope="fragment")