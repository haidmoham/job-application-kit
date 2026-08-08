# Privacy and state separation

The repository is reusable infrastructure. A candidate profile is not reusable infrastructure.

## Keep in Git

- schemas and example config;
- routing logic;
- dedupe logic;
- telemetry code and schema;
- onboarding and execution contracts;
- tests.

## Keep local by default

- name, address, phone, email;
- resume files and resume URLs that identify the candidate;
- employers and exact work-history dates when privacy matters;
- demographic data;
- immigration/work-authorization detail beyond what the candidate chooses to persist;
- compensation answers;
- screenshots and form answers;
- inbox evidence;
- application history;
- credentials and security answers.

The example files contain only placeholders. `scripts/bootstrap.py` copies them to ignored local files.
