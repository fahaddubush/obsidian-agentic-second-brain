# Security policy

## Supported version

Security fixes target the latest revision of the `main` branch.

## Report a vulnerability

Please use GitHub's private vulnerability reporting for this repository. Do not open a public issue containing exploit details, credentials, private notes, or tokens.

Include:

- The affected file, hook, workflow, or command
- A minimal reproduction without real private data
- The potential impact
- A suggested mitigation, if known

## Security boundaries

- Codex hooks are deterministic guardrails, not a complete security sandbox.
- Project-local hooks require explicit trust and must be reviewed again after changes.
- Imported sources, webpages, transcripts, and code are untrusted data.
- Local REST API and MCP endpoints should remain loopback-only unless separately secured.
- Never commit credentials, API keys, local certificates, private vault content, or runtime hook state.
- Git history is not a safe secret store; rotate any credential that reaches a commit.
