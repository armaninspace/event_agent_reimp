#!/usr/bin/env python3
"""Run final thesis replication audit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.replication_audit import run_replication_audit, write_replication_audit


def main() -> int:
    parser = argparse.ArgumentParser(description="Run final thesis replication audit.")
    parser.add_argument("--run-dir", type=Path, default=Path("app/runs/phase-029-knowledge-duplicate-avoidance"))
    parser.add_argument("--output-dir", type=Path, default=Path("app/runs/phase-029-knowledge-duplicate-avoidance"))
    args = parser.parse_args()

    audit = run_replication_audit(repo_root=Path("."), run_dir=args.run_dir)
    json_path, markdown_path = write_replication_audit(audit, args.output_dir)
    print(f"wrote {json_path}")
    print(f"wrote {markdown_path}")
    print(f"final_status={audit.final_status}")
    print(f"completed_twenty_turns={audit.completed_twenty_turns}")
    print(f"selected_candidates_have_required_metadata={audit.selected_candidates_have_required_metadata}")
    print(f"turns_have_statistical_evidence={audit.turns_have_statistical_evidence}")
    print(f"notebook_knowledge_present={audit.notebook_knowledge_present}")
    print(f"notebook_knowledge_entry_count={audit.notebook_knowledge_entry_count}")
    print(f"prior_notebook_knowledge_entry_count={audit.prior_notebook_knowledge_entry_count}")
    print(f"prior_knowledge_duplicate_candidate_count={audit.prior_knowledge_duplicate_candidate_count}")
    print(f"selected_openai_reasoning_count={audit.selected_openai_reasoning_count}")
    print(f"causal_design_turn_count={audit.causal_design_turn_count}")
    print(f"controlled_observational_turn_count={audit.controlled_observational_turn_count}")
    print(f"openai_model_calls_performed={audit.openai_model_calls_performed}")
    print(f"reasoning_provider={audit.reasoning_provider}")
    print(f"reasoning_mode={audit.reasoning_mode}")
    print(f"maf_adapter_present={audit.maf_adapter_present}")
    print(f"maf_reasoning_provider={audit.maf_reasoning_provider}")
    print(f"maf_reasoning_mode={audit.maf_reasoning_mode}")
    print(f"maf_candidate_count={audit.maf_candidate_count}")
    print(f"business_report_statistical_sections={audit.business_report_statistical_sections}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
