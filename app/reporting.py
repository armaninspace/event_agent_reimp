"""Static HTML report and telemetry playback rendering."""

from __future__ import annotations

import html
import json


def render_business_report(session: dict[str, object]) -> str:
    """Render stakeholder-readable business evidence HTML."""
    turns = session["turns"]
    assert isinstance(turns, list)
    items = []
    for turn in turns:
        selected = turn["selected_candidate"]
        assert isinstance(selected, dict)
        statistical_html = _render_statistical_evidence(turn.get("statistical_evidence"))
        items.append(
            "<section>"
            f"<h2>Turn {html.escape(str(turn['turn']))}: {html.escape(str(selected['question']))}</h2>"
            f"<p><strong>Selected candidate:</strong> {html.escape(str(selected['candidate_id']))}</p>"
            f"<p><strong>Public rationale:</strong> {html.escape(str(selected['rationale']))}</p>"
            f"<p><strong>Caveat:</strong> {html.escape(str(selected['caveat']))}</p>"
            "<p><strong>Evidence strength:</strong> exploratory workflow evidence; not causal proof.</p>"
            f"{statistical_html}"
            "</section>"
        )
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        "<title>Business Evidence Report</title>"
        "<style>body{font-family:system-ui,sans-serif;max-width:920px;margin:40px auto;line-height:1.5}"
        "section{border-top:1px solid #ddd;padding:18px 0}code{background:#f4f4f4;padding:2px 4px}</style>"
        "</head><body>"
        "<h1>Business Evidence Report</h1>"
        "<p>This report summarizes exploratory event-evidence workflow decisions. "
        "It preserves caveats and does not claim causal proof.</p>"
        f"{''.join(items)}"
        "</body></html>\n"
    )


def _render_statistical_evidence(value: object) -> str:
    if not isinstance(value, dict):
        return ""
    result_ids = value.get("result_ids", [])
    if not isinstance(result_ids, list):
        result_ids = []
    caveats = value.get("caveats", [])
    if not isinstance(caveats, list):
        caveats = []
    return (
        "<div><h3>Statistical Evidence</h3>"
        f"<p><strong>Result count:</strong> {html.escape(str(value.get('result_count')))}</p>"
        f"<p><strong>Minimum adjusted p-value:</strong> {html.escape(str(value.get('min_adjusted_p_value')))}</p>"
        f"<p><strong>Adjusted-significance flag:</strong> {html.escape(str(value.get('has_adjusted_significance')))}</p>"
        "<p><strong>Result IDs:</strong></p>"
        f"<ul>{''.join(f'<li><code>{html.escape(str(result_id))}</code></li>' for result_id in result_ids)}</ul>"
        "<p><strong>Statistical caveats:</strong></p>"
        f"<ul>{''.join(f'<li>{html.escape(str(caveat))}</li>' for caveat in caveats)}</ul>"
        "</div>"
    )


def render_playback_ui(telemetry_events: list[dict[str, object]]) -> str:
    """Render static playback UI with embedded telemetry."""
    payload = json.dumps(telemetry_events).replace("</", "<\\/")
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        "<title>Friends Loop Playback</title>"
        "<style>body{font-family:system-ui,sans-serif;margin:32px;line-height:1.4}"
        "table{border-collapse:collapse;width:100%}td,th{border:1px solid #ddd;padding:6px;vertical-align:top}"
        "pre{white-space:pre-wrap;margin:0}</style>"
        "</head><body>"
        "<h1>Friends Loop Playback</h1>"
        "<table><thead><tr><th>Seq</th><th>Turn</th><th>Actor</th><th>Type</th><th>Summary</th><th>Payload</th></tr></thead>"
        "<tbody id=\"events\"></tbody></table>"
        f"<script>const telemetry = {payload};"
        "const esc = (v) => String(v).replace(/[&<>\"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c]));"
        "document.getElementById('events').innerHTML = telemetry.map(e => "
        "`<tr><td>${esc(e.sequence)}</td><td>${esc(e.turn)}</td><td>${esc(e.actor)}</td>"
        "<td>${esc(e.event_type)}</td><td>${esc(e.summary)}</td><td><pre>${esc(JSON.stringify(e.payload,null,2))}</pre></td></tr>`"
        ").join('');</script>"
        "</body></html>\n"
    )
