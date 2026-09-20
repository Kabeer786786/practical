"""Jobs and Invoice Pipeline Client with live API support and rich enterprise mocks."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from .api_client import APIClient


class JobsClient:
    """Provides invoice records, GitHub Actions-style pipeline execution steps, and HITL decision workflows."""

    def __init__(self, api_client: Optional[APIClient] = None):
        self.api = api_client or APIClient()

        # Seed realistic enterprise invoice mock dataset
        self._invoices: Dict[str, Dict[str, Any]] = {
            "INV-1042": {
                "id": "INV-1042",
                "number": "INV-2026-1042",
                "vendor": "CloudSphere Tech Solutions",
                "vendor_id": "VEND-842",
                "vendor_gstin": "27AABCC1234D1Z8",
                "amount": 14250.00,
                "currency": "USD",
                "po_number": "PO-7781",
                "date": "2026-09-15",
                "due_date": "2026-10-15",
                "confidence": 0.94,
                "status": "Requires Review",
                "category": "Cloud Infrastructure",
                "discrepancy_summary": "Unit price mismatch on compute node hours ($0.48 billed vs $0.42 contracted in PO-7781).",
                "workflow_file": "invoice-audit-pipeline.yml",
                "run_id": "#84920",
                "branch": "main",
                "commit": "a7e1f4b",
                "total_duration": "1m 42s",
                "line_items": [
                    {"desc": "Standard Compute Nodes (Hours)", "qty": 25000, "unit_price": 0.48, "po_price": 0.42, "total": 12000.00, "flagged": True},
                    {"desc": "Premium SSD Block Storage (TB)", "qty": 15, "unit_price": 150.00, "po_price": 150.00, "total": 2250.00, "flagged": False},
                ],
                "tax_breakdown": {"subtotal": 14250.00, "tax_rate": "0%", "tax_amount": 0.00, "total": 14250.00},
                "review_decision": None,
            },
            "INV-1039": {
                "id": "INV-1039",
                "number": "INV-2026-1039",
                "vendor": "Apex Logistics Global",
                "vendor_id": "VEND-319",
                "vendor_gstin": "29XYZAB5678E2Z1",
                "amount": 8920.50,
                "currency": "USD",
                "po_number": "PO-7620",
                "date": "2026-09-17",
                "due_date": "2026-10-02",
                "confidence": 0.99,
                "status": "Completed",
                "category": "Freight & Shipping",
                "discrepancy_summary": "All 3-way match checks passed. PO rates and GST codes fully aligned.",
                "workflow_file": "invoice-audit-pipeline.yml",
                "run_id": "#84918",
                "branch": "main",
                "commit": "8c33d2a",
                "total_duration": "48s",
                "line_items": [
                    {"desc": "Air Freight Expedited (kg)", "qty": 1200, "unit_price": 6.50, "po_price": 6.50, "total": 7800.00, "flagged": False},
                    {"desc": "Customs Clearance & Documentation", "qty": 1, "unit_price": 1120.50, "po_price": 1120.50, "total": 1120.50, "flagged": False},
                ],
                "tax_breakdown": {"subtotal": 8920.50, "tax_rate": "0%", "tax_amount": 0.00, "total": 8920.50},
                "review_decision": {"status": "Auto-Approved", "notes": "3-way match passed with 99% confidence.", "date": "2026-09-17"},
            },
            "INV-1044": {
                "id": "INV-1044",
                "number": "INV-2026-1044",
                "vendor": "Matrix Micro Devices",
                "vendor_id": "VEND-104",
                "vendor_gstin": "33AABCM9988F1Z4",
                "amount": 34800.00,
                "currency": "USD",
                "po_number": "PO-7802",
                "date": "2026-09-19",
                "due_date": "2026-10-19",
                "confidence": 0.81,
                "status": "Validation Failed",
                "category": "Hardware & Chips",
                "discrepancy_summary": "Unregistered GSTIN number; PO-7802 maximum allocation limit exceeded by $9,800.00.",
                "workflow_file": "invoice-audit-pipeline.yml",
                "run_id": "#84924",
                "branch": "main",
                "commit": "3e9b11c",
                "total_duration": "1m 15s",
                "line_items": [
                    {"desc": "Edge Processing Microcontrollers", "qty": 200, "unit_price": 174.00, "po_price": 125.00, "total": 34800.00, "flagged": True},
                ],
                "tax_breakdown": {"subtotal": 34800.00, "tax_rate": "18%", "tax_amount": 6264.00, "total": 41064.00},
                "review_decision": None,
            },
            "INV-1045": {
                "id": "INV-1045",
                "number": "INV-2026-1045",
                "vendor": "Sentinel Cybersecurity Labs",
                "vendor_id": "VEND-512",
                "vendor_gstin": "07AAACS4432G1Z9",
                "amount": 18500.00,
                "currency": "USD",
                "po_number": "PO-7840",
                "date": "2026-09-20",
                "due_date": "2026-10-20",
                "confidence": 0.89,
                "status": "In Progress",
                "category": "Security Software",
                "discrepancy_summary": "Step 3 Business & Tax Rule Match is executing against ERP registry.",
                "workflow_file": "invoice-audit-pipeline.yml",
                "run_id": "#84931",
                "branch": "main",
                "commit": "f9024ab",
                "total_duration": "35s",
                "line_items": [
                    {"desc": "SOC 2 Type II Surveillance Agent", "qty": 500, "unit_price": 37.00, "po_price": 37.00, "total": 18500.00, "flagged": False},
                ],
                "tax_breakdown": {"subtotal": 18500.00, "tax_rate": "0%", "tax_amount": 0.00, "total": 18500.00},
                "review_decision": None,
            },
            "INV-1036": {
                "id": "INV-1036",
                "number": "INV-2026-1036",
                "vendor": "HyperScale Office Interiors",
                "vendor_id": "VEND-901",
                "vendor_gstin": "06AABCH8765K1Z3",
                "amount": 6450.00,
                "currency": "USD",
                "po_number": "PO-7590",
                "date": "2026-09-12",
                "due_date": "2026-10-12",
                "confidence": 0.98,
                "status": "Completed",
                "category": "Facilities",
                "discrepancy_summary": "PO matched, delivery receipt confirmed in ERP.",
                "workflow_file": "invoice-audit-pipeline.yml",
                "run_id": "#84890",
                "branch": "main",
                "commit": "4d12c8a",
                "total_duration": "42s",
                "line_items": [
                    {"desc": "Ergonomic Task Chairs", "qty": 15, "unit_price": 430.00, "po_price": 430.00, "total": 6450.00, "flagged": False},
                ],
                "tax_breakdown": {"subtotal": 6450.00, "tax_rate": "0%", "tax_amount": 0.00, "total": 6450.00},
                "review_decision": {"status": "Auto-Approved", "notes": "Valid PO and receipt.", "date": "2026-09-12"},
            },
        }

    def list_invoices(self) -> List[Dict[str, Any]]:
        """List all invoices summary."""
        live_data = self.api.get("/invoices")
        if live_data and isinstance(live_data, list):
            return live_data
        return list(self._invoices.values())

    def get_invoice(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """Get invoice detail by ID."""
        live_data = self.api.get(f"/invoices/{invoice_id}")
        if live_data and isinstance(live_data, dict):
            return live_data
        return self._invoices.get(invoice_id)

    def get_job_steps(self, invoice_id: str) -> List[Dict[str, Any]]:
        """Return 4 GitHub Actions-style pipeline execution steps for the invoice."""
        inv = self.get_invoice(invoice_id) or self._invoices["INV-1042"]
        status = inv.get("status", "Requires Review")

        # Step 1 status & duration
        s1_status = "success"
        s1_duration = "14s"

        # Step 2 status & duration
        s2_status = "success"
        s2_duration = "22s"

        # Step 3 status & duration
        if status == "Validation Failed":
            s3_status = "failed"
            s3_duration = "39s"
        elif status == "In Progress":
            s3_status = "in_progress"
            s3_duration = "35s"
        elif status == "Requires Review":
            s3_status = "warning"
            s3_duration = "44s"
        else:
            s3_status = "success"
            s3_duration = "12s"

        # Step 4 status & duration
        if status == "In Progress":
            s4_status = "waiting"
            s4_duration = "--"
        elif status == "Requires Review":
            s4_status = "waiting_review"
            s4_duration = "22s"
        elif status == "Validation Failed":
            s4_status = "failed"
            s4_duration = "15s"
        else:
            s4_status = "success"
            s4_duration = "10s"

        steps = [
            {
                "id": "step_1",
                "name": "Step 1: Document Ingestion & OCR",
                "duration": s1_duration,
                "status": s1_status,
                "logs": [
                    f"[00:00:01] [INFO] Triggered by ingestion worker for file: {inv['id']}_raw.pdf",
                    "[00:00:03] [INFO] Extracting raw text layout and visual token boundaries...",
                    "[00:00:07] [INFO] OCR engine: Hybrid Tesseract + Document Layout Transformer",
                    f"[00:00:11] [SUCCESS] Document layout parsed. 2 pages, 142 layout blocks identified.",
                    f"[00:00:14] [SUCCESS] Optical character confidence rated at {int(inv['confidence'] * 100)}%.",
                ],
                "inputs_outputs": {
                    "input": {
                        "document_id": f"DOC-{inv['id']}",
                        "file_name": f"{inv['id']}_raw.pdf",
                        "mime_type": "application/pdf",
                        "size_bytes": 482104,
                    },
                    "output": {
                        "ocr_status": "COMPLETED",
                        "confidence_score": inv["confidence"],
                        "total_pages": 2,
                        "token_count": 1420,
                    },
                },
                "artifacts": [
                    {"name": "ocr_raw_tokens.json", "size": "45 KB", "type": "tokens"},
                    {"name": "page_layout_bbox.png", "size": "180 KB", "type": "image"},
                ],
                "bounding_boxes": [
                    {"label": "Vendor Header", "bbox": {"x": 45, "y": 60, "w": 320, "h": 80}, "text": inv["vendor"]},
                    {"label": "Invoice Total", "bbox": {"x": 420, "y": 680, "w": 180, "h": 40}, "text": f"{inv['currency']} {inv['amount']:,.2f}"},
                ],
            },
            {
                "id": "step_2",
                "name": "Step 2: Schema & Entity Extraction",
                "duration": s2_duration,
                "status": s2_status,
                "logs": [
                    "[00:00:15] [INFO] Running entity extraction with NormalizedInvoiceSchema...",
                    f"[00:00:18] [INFO] Detected Vendor: {inv['vendor']} (GSTIN: {inv['vendor_gstin']})",
                    f"[00:00:21] [INFO] Associated PO reference extracted: {inv['po_number']}",
                    f"[00:00:29] [INFO] Extracted {len(inv['line_items'])} line items with quantity and unit rates.",
                    "[00:00:36] [SUCCESS] Entity mapping normalization completed with zero schema violations.",
                ],
                "inputs_outputs": {
                    "input": {"token_stream_id": f"TOK-{inv['id']}"},
                    "output": {
                        "invoice_number": inv["number"],
                        "vendor_name": inv["vendor"],
                        "vendor_gstin": inv["vendor_gstin"],
                        "po_number": inv["po_number"],
                        "currency": inv["currency"],
                        "subtotal": inv["tax_breakdown"]["subtotal"],
                        "line_items_count": len(inv["line_items"]),
                    },
                },
                "artifacts": [
                    {"name": "normalized_invoice.json", "size": "12 KB", "type": "json"},
                    {"name": "extracted_tables.csv", "size": "4 KB", "type": "csv"},
                ],
                "bounding_boxes": [
                    {"label": "Line Item 1", "bbox": {"x": 50, "y": 280, "w": 500, "h": 35}, "text": inv["line_items"][0]["desc"]},
                ],
            },
            {
                "id": "step_3",
                "name": "Step 3: Business & Tax Rule Match",
                "duration": s3_duration,
                "status": s3_status,
                "logs": [
                    f"[00:00:38] [INFO] Querying ERP backend for PO reference {inv['po_number']}...",
                    f"[00:00:41] [INFO] Performing 3-way match: PO vs Goods Receipt vs Invoice...",
                    f"[00:00:54] [INFO] Verifying GST compliance and vendor registration in government portal...",
                ]
                + (
                    [
                        f"[00:01:10] [WARN] Rate Discrepancy Found: Contract specifies $0.42/unit, invoice bills $0.48/unit.",
                        "[00:01:22] [WARN] Rule VIOLATION: tolerance threshold (2.0%) exceeded (+14.28%).",
                    ]
                    if status == "Requires Review"
                    else (
                        [
                            "[00:01:12] [ERROR] Unregistered GSTIN: Vendor GST status is marked CANCELLED in GST portal.",
                            "[00:01:15] [ERROR] PO limit exceeded: $34,800.00 billed against remaining balance of $25,000.00.",
                        ]
                        if status == "Validation Failed"
                        else [
                            "[00:01:02] [SUCCESS] All rates match PO within 0.00% variance.",
                            "[00:01:05] [SUCCESS] Active vendor registration confirmed in Master Registry.",
                        ]
                    )
                ),
                "inputs_outputs": {
                    "input": {
                        "erp_po_id": inv["po_number"],
                        "vendor_id": inv["vendor_id"],
                        "tolerance_threshold": "2.0%",
                    },
                    "output": {
                        "rule_checks_run": 8,
                        "rule_checks_passed": 7 if status == "Requires Review" else (5 if status == "Validation Failed" else 8),
                        "discrepancies_detected": [inv["discrepancy_summary"]] if status != "Completed" else [],
                    },
                },
                "artifacts": [
                    {"name": "rule_audit_report.json", "size": "8 KB", "type": "json"},
                    {"name": "po_comparison_matrix.json", "size": "15 KB", "type": "json"},
                ],
                "bounding_boxes": [],
            },
            {
                "id": "step_4",
                "name": "Step 4: Synthesis & Human Decision Gate",
                "duration": s4_duration,
                "status": s4_status,
                "logs": [
                    "[00:01:25] [INFO] Synthesizing audit findings through Self-Reflective RAG...",
                    "[00:01:31] [INFO] Grounding citations against validation_rules/po_match.md and erp_contracts/...",
                ]
                + (
                    [
                        "[00:01:42] [WAITING] Human review required: Anomaly flagged in unit pricing.",
                        "[00:01:42] [INFO] Routed to Compliance Officer Review Queue.",
                    ]
                    if status == "Requires Review"
                    else (
                        [
                            "[00:01:35] [FATAL] Validation failed. Automated rejection triggered.",
                        ]
                        if status == "Validation Failed"
                        else [
                            "[00:01:38] [SUCCESS] Automated approval granted. Queued for payment batch.",
                        ]
                    )
                ),
                "inputs_outputs": {
                    "input": {
                        "invoice_status": status,
                        "requires_human_signoff": (status == "Requires Review"),
                    },
                    "output": {
                        "decision_state": "WAITING_HUMAN_INTERVENTION" if status == "Requires Review" else "AUTO_RESOLVED",
                        "audit_trail_id": f"AUD-{inv['id']}-FINAL",
                    },
                },
                "artifacts": [
                    {"name": "compliance_summary.md", "size": "6 KB", "type": "markdown"},
                ],
                "bounding_boxes": [],
            },
        ]
        return steps

    def update_decision(self, invoice_id: str, decision: str, notes: str, user: str = "Compliance Officer") -> bool:
        """Submit Human-in-the-Loop decision (Approve / Reject / Request Correction)."""
        if invoice_id in self._invoices:
            self._invoices[invoice_id]["review_decision"] = {
                "decision": decision,
                "notes": notes,
                "user": user,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            if decision == "Approve with Override":
                self._invoices[invoice_id]["status"] = "Completed"
            elif decision == "Reject Invoice":
                self._invoices[invoice_id]["status"] = "Validation Failed"
            elif decision == "Request Correction":
                self._invoices[invoice_id]["status"] = "Requires Review"
            return True
        return False
