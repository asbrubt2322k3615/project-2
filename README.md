# ZPA Application-Specific Access Policy Project

This project provides a policy-as-code workflow for application-specific access policies with Zscaler Private Access (ZPA).

It lets you:
- Define applications and access rules in YAML.
- Validate policy structure and rule precedence.
- Generate deployment-ready JSON artifacts that can be used with ZPA API or Terraform variable handoff.
- View policies in a local web dashboard.

## Project Structure

- `config/applications.yaml`: application inventory (segment, domain, ports, server groups)
- `config/policies.yaml`: access policy definitions by application
- `src/policy_builder.py`: parser, validator, and artifact generator
- `build.py`: CLI entry point for project build
- `app.py`: Flask web app for policy dashboard
- `web/templates/`: dashboard templates
- `web/static/`: dashboard styles
- `tests/test_policy_builder.py`: unit tests for validation and generation
- `build/`: generated output folder

## Prerequisites

- Python 3.10+

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python build.py
```

On success, generated files:
- `build/zpa_access_policies.json`
- `build/zpa_terraform_policy_input.json`

## Run Website

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:
- `http://127.0.0.1:5000`
- Raw JSON APIs:
  - `http://127.0.0.1:5000/api/payload`
  - `http://127.0.0.1:5000/api/terraform`

## Policy Model

Each policy includes:
- `name`
- `application`
- `priority` (lower number = evaluated first)
- `action` (`allow` or `deny`)
- `conditions`:
  - `idp_groups`
  - `device_posture`
  - `client_types`
  - optional `time_window`

## Notes

- Output payload is designed for practical integration and may require field mapping for your exact ZPA tenant or provider version.
- Start with the sample YAML files and adjust to match your production naming conventions.
