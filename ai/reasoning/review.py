import json
import sys


def assess_risk(enriched_context: dict) -> dict:
    risk = "LOW"
    reasons = []
    comments = []

    environment = enriched_context.get("environment", "unknown")
    resources = enriched_context.get("resources", [])
    summary = enriched_context.get("summary", {})

    # Signal 1: Shared infrastructure modified
    shared_changes = [
        r for r in resources if r.get("classification") == "shared-infra"
    ]
    if shared_changes:
        risk = "MEDIUM"
        reasons.append(
            "Shared infrastructure resources are being modified, increasing blast radius."
        )
        comments.append(
            "⚠️ Shared infrastructure change detected. "
            "Changes to shared components can impact multiple services."
        )

    # Signal 2: Network-related resources
    network_types = ["azurerm_virtual_network", "azurerm_subnet"]
    network_changes = [
        r for r in resources if r.get("type") in network_types
    ]
    if network_changes:
        if risk == "MEDIUM":
            risk = "HIGH"
        else:
            risk = "MEDIUM"
        reasons.append(
            "Network resources are being modified, which can affect connectivity."
        )
        comments.append(
            "⚠️ Network-level changes detected. "
            "Ensure no workloads are unintentionally impacted."
        )

    # Signal 3: Large number of changes
    if summary.get("create", 0) + summary.get("update", 0) + summary.get("delete", 0) >= 5:
        risk = "HIGH"
        reasons.append(
            "Multiple infrastructure changes in a single deployment increase operational risk."
        )
        comments.append(
            "⚠️ High number of infrastructure changes detected in one plan."
        )

    return {
        "environment": environment,
        "risk_level": risk,
        "reasons": reasons,
        "review_comments": comments
    }


def main(input_file: str, output_file: str):
    with open(input_file, "r") as f:
        enriched_context = json.load(f)

    review = assess_risk(enriched_context)

    with open(output_file, "w") as f:
        json.dump(review, f, indent=2)

    print("SUCCESS: AI review generated")
    print(json.dumps(review, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python review.py <enriched_context.json> <ai_review.json>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
