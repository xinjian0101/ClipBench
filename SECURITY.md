# Security Policy

## Supported versions

Security fixes target the current `main` branch and current result contracts. Older snapshots and unsupported forks may not receive updates.

## Reporting a vulnerability

Do not publish private benchmark media, confidential annotations, internal paths, credentials, or working exploit details in a public issue.

Use GitHub private vulnerability reporting when available. If it is unavailable, open a minimal public issue identifying the affected commit and component without sensitive details.

Include:

- affected commit;
- minimal synthetic truth and prediction files;
- threshold or manifest settings;
- impact summary;
- expected and actual metrics;
- operating system and Python version.

## Security boundaries

ClipBench reads local benchmark files and writes local reports. Users remain responsible for protecting benchmark media, annotation data, source paths, manifests, and generated reports.

Metric validation does not verify the authorization, confidentiality, or safety of the underlying media or annotations.

## Out of scope

- private benchmark content posted publicly by users;
- security of unrelated media storage systems;
- annotation-policy disputes without a software defect;
- unsupported local modifications;
- claims about content quality or commercial outcomes.

## Disclosure

Allow maintainers reasonable time to reproduce, correct, test, and document a confirmed issue before public disclosure.
