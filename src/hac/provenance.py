from __future__ import annotations

from hac.models import Artifact, Classification, Provenance, Resource


def provenance_from_resource(resource: Resource) -> Provenance:
    return Provenance(
        source_ids=(resource.resource_id,),
        classifications=(resource.classification,),
        derived_from_external=resource.trust_level.value == "EXTERNAL"
        or resource.classification in {Classification.EXTERNAL, Classification.UNTRUSTED},
    )


def inherit_provenance(parents: list[Artifact]) -> Provenance:
    source_ids: set[str] = set()
    classifications: set[Classification] = set()
    derived_from_external = False
    for parent in parents:
        if not parent.provenance.source_ids:
            raise ValueError(f"artifact {parent.artifact_id} has missing provenance")
        source_ids.update(parent.provenance.source_ids)
        classifications.update(parent.provenance.classifications)
        derived_from_external = derived_from_external or parent.provenance.derived_from_external
    return Provenance(
        source_ids=tuple(sorted(source_ids)),
        classifications=tuple(sorted(classifications, key=lambda c: c.value)),
        derived_from_external=derived_from_external,
        declassified=False,
    )


def join_classification(provenance: Provenance, fallback: Classification) -> Classification:
    if Classification.HIGHLY_SENSITIVE in provenance.classifications:
        return Classification.HIGHLY_SENSITIVE
    if Classification.SECRET in provenance.classifications:
        return Classification.SECRET
    if Classification.UNTRUSTED in provenance.classifications or provenance.derived_from_external:
        return Classification.UNTRUSTED
    if Classification.INTERNAL in provenance.classifications:
        return Classification.INTERNAL
    if Classification.EXTERNAL in provenance.classifications:
        return Classification.EXTERNAL
    if Classification.PUBLIC in provenance.classifications:
        return Classification.PUBLIC
    return fallback