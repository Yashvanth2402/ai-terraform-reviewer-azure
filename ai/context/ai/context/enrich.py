import json
import sys
from pathlib import Path


def infer_environment(plan_path: str) -> str:
    # Simple environment inference
    if "prod" in plan_path.lower():
        return "prod"
    return "dev"


def classify_resource(address: str) -> str:
    # Simple but powerful signal
    if "shared" in address.lower():
        return "shared-infra"
    return "app-infra"


def enrich_plan(plan_file: str, output_file: str):
    print("DEBUG: enrich.py started")

    plan_path = Path(plan_file)
    if not plan_path.exists():
        raise FileNotFoundError(f"{plan_file} not found")

    with open(plan_file, "r") as f:
        plan = json.load(f)

    enriched = {
        "environment": infer_environment(plan_file),
        "summary": {
            "create": 0,
            "update": 0,
            "delete": 0
        },
        "resources": []
    }

    resource_changes = plan.get("resource_changes", [])
    print(f"DEBUG: Found {len(resource_changes)} resource changes")

    for rc in resource_changes:
        actions = rc.get("change", {}).get("actions", [])

        for action in actions:
            if action in enriched["summary"]:
                enriched["summary"][action] += 1

        enriched["resources"].append({
            "address": rc.get("address"),
            "type": rc.get("type"),
            "actions": actions,
            "classification": classify_resource(rc.get("address", ""))
        })

    with open(output_file, "w") as f:
        json.dump(enriched, f, indent=2)

    print(f"Enriched context written to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python enrich.py <tfplan.json> <output.json>")
        sys.exit(1)

    enrich_plan(sys.argv[1], sys.argv[2])
