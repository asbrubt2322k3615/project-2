from pathlib import Path

from src.policy_builder import (
    PolicyValidationError,
    build_terraform_input,
    build_zpa_payload,
    load_applications,
    load_policies,
    validate_policies,
    write_json,
)


def main() -> int:
    root = Path(__file__).resolve().parent
    applications_path = root / "config" / "applications.yaml"
    policies_path = root / "config" / "policies.yaml"
    out_dir = root / "build"

    try:
        applications = load_applications(applications_path)
        policies = load_policies(policies_path)
        validate_policies(applications, policies)
    except PolicyValidationError as exc:
        print(f"Validation failed: {exc}")
        return 1

    payload = build_zpa_payload(applications, policies)
    terraform_input = build_terraform_input(payload)

    write_json(payload, out_dir / "zpa_access_policies.json")
    write_json(terraform_input, out_dir / "zpa_terraform_policy_input.json")

    print("Build completed.")
    print(f"- {out_dir / 'zpa_access_policies.json'}")
    print(f"- {out_dir / 'zpa_terraform_policy_input.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
