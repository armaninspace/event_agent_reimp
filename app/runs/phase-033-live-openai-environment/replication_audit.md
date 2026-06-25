# Thesis Replication Audit

Schema: phase-019.replication-audit.v1
Run directory: `app/runs/phase-033-live-openai-environment`
Final status: `replicated_with_known_limits`

## Acceptance Checks

- Required source files present: True
- Completed 20 turns: True
- Stopped early: False
- Workflow-task statistical misroutes: 0
- Selected candidates have required metadata: True
- Turns have statistical evidence: True
- Data snapshot complete: True
- Data snapshot combined SHA-256: `eb78bb3a0b2f0116c3f03349f4b077781419789f22fb4e2df5de22d58df3c3c1`
- Correction notebook present: True
- Correction notebook executed: True
- Notebook knowledge present: True
- Notebook knowledge entry count: 20
- Prior notebook knowledge entry count: 20
- Prior-knowledge duplicate candidate count: 0
- Prior-knowledge evolved duplicate candidate count: 0
- Selected semantic slot counts: {'city_week_event_spending': 7, 'identification_risk': 7, 'msa_week_coverage': 6}
- Selected unique semantic slot count: 3
- Forum metadata count: 20
- Tournament metadata count: 20
- Reflection metadata count: 20
- Evolution metadata count: 20
- Evolution variant count: 20
- OpenAI reasoning metadata count: 20
- Causal-design turn count: 20
- Controlled-observational turn count: 20
- OpenAI model calls performed: True
- Reasoning provider: openai
- Reasoning mode: openai
- MAF adapter present: True
- MAF reasoning provider: openai
- MAF reasoning mode: openai
- MAF model calls performed: True
- MAF candidate count: 3
- Statistical evidence turn count: 20
- Business report statistical sections: 20
- Business report statistical tables: 20
- Notebook workspace present: True

## Known Limits

- Statistical evidence is controlled observational where matched controls exist, but not causal proof.
