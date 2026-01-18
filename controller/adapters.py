from db.supabase_client import supabase


def load_snapshot_from_supabase(business_id: str) -> str:
    """
    Adapter: Supabase → raw text snapshot
    """

    business = (
        supabase.table("businesses")
        .select("description, target_audience")
        .eq("id", business_id)
        .single()
        .execute()
        .data
    )

    competitors = (
        supabase.table("competitors")
        .select("name, context")
        .eq("business_id", business_id)
        .execute()
        .data
    )

    lines = ["Business context:"]

    if business.get("description"):
        lines.append(business["description"])

    if business.get("target_audience"):
        lines.append(f"Target audience: {business['target_audience']}")

    lines.append("")

    for c in competitors:
        lines.append(f"Competitor: {c['name']}")
        lines.append(c["context"])
        lines.append("")

    return "\n".join(lines)


def to_strategy_context(extracted):
    """
    Phase 2 → Phase 1 adapter.

    This is intentionally a pass-through because
    decide_strategy already accepts ExtractedContext.
    """
    return extracted
