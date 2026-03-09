from pathlib import Path

from flask import Flask, jsonify, render_template

from src.policy_builder import (
    PolicyValidationError,
    build_terraform_input,
    build_zpa_payload,
    load_applications,
    load_policies,
    validate_policies,
)


ROOT = Path(__file__).resolve().parent
app = Flask(__name__, template_folder="web/templates", static_folder="web/static")


def _load_dashboard_data():
    applications = load_applications(ROOT / "config" / "applications.yaml")
    policies = load_policies(ROOT / "config" / "policies.yaml")
    validate_policies(applications, policies)
    payload = build_zpa_payload(applications, policies)
    terraform_input = build_terraform_input(payload)
    return applications, policies, payload, terraform_input


@app.get("/")
def index():
    try:
        applications, policies, payload, terraform_input = _load_dashboard_data()
    except PolicyValidationError as exc:
        return render_template("error.html", error=str(exc)), 400

    app_list = [applications[name] for name in sorted(applications.keys())]
    sorted_policies = sorted(policies, key=lambda p: p.priority)
    return render_template(
        "index.html",
        applications=app_list,
        policies=sorted_policies,
        rule_count=len(payload["rules"]),
        terraform_count=len(terraform_input["zpa_policy_rules"]),
    )


@app.get("/api/payload")
def api_payload():
    _, _, payload, _ = _load_dashboard_data()
    return jsonify(payload)


@app.get("/api/terraform")
def api_terraform():
    _, _, _, terraform_input = _load_dashboard_data()
    return jsonify(terraform_input)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
