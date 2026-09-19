# HAC Demo Assets

This folder holds diagram and visual assets for the HAC narrative deck and demo walkthrough.

## Included assets

- `HAC_attack_chain.mmd`: attack-chain diagram showing the sequence of legitimate actions leading to an unauthorized capability.
- `HAC_state_transition.mmd`: state transition diagram showing action -> state -> capability -> invariant -> allow/block.

## Repo-aligned narrative

The diagrams reflect the implemented prototype behavior documented in the project README and threat model:
- early actions are allowed
- encryption and chunking preserve provenance
- the final external upload is blocked because it creates a secret-to-external violation

Use these assets in slides or product demos without claiming broader guarantees than the repository supports.
