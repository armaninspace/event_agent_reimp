from app.reporting import render_business_report, render_playback_ui


def test_render_business_report_escapes_public_text() -> None:
    html = render_business_report(
        {
            "turns": [
                {
                    "turn": 1,
                    "selected_candidate": {
                        "candidate_id": "c1",
                        "question": "<script>alert(1)</script>",
                        "rationale": "A & B",
                        "caveat": "Not causal <proof>",
                    },
                }
            ]
        }
    )

    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "A &amp; B" in html
    assert "Not causal &lt;proof&gt;" in html


def test_render_business_report_includes_statistical_evidence_and_escapes_ids() -> None:
    html = render_business_report(
        {
            "turns": [
                {
                    "turn": 1,
                    "selected_candidate": {
                        "candidate_id": "c1",
                        "question": "Do crowds change spending?",
                        "rationale": "A & B",
                        "caveat": "Not causal.",
                    },
                    "statistical_evidence": {
                        "result_count": 1,
                        "min_adjusted_p_value": 0.01,
                        "has_adjusted_significance": True,
                        "result_ids": ["matched:<city>"],
                        "results": [
                            {
                                "result_id": "matched:<city>",
                                "family": "matched",
                                "dataset": "city_week",
                                "outcome": "revenue_all",
                                "p_value": 0.01,
                                "adjusted_p_value": 0.02,
                                "status": "ok",
                            }
                        ],
                        "caveats": ["Observational <only>."],
                    },
                }
            ]
        }
    )

    assert "Statistical Evidence" in html
    assert "matched:&lt;city&gt;" in html
    assert 'class="statistical-results"' in html
    assert "Adjusted p-value" in html
    assert "Observational &lt;only&gt;." in html


def test_render_playback_ui_embeds_telemetry() -> None:
    html = render_playback_ui(
        [
            {
                "sequence": 1,
                "turn": 1,
                "actor": "Spark",
                "event_type": "board.proposed",
                "summary": "Proposed candidates.",
                "payload": {"candidate_ids": ["c1"]},
            }
        ]
    )

    assert "Friends Loop Playback" in html
    assert "board.proposed" in html
