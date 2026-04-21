# Customer Interview Guide

Use this guide for 30-minute discovery calls with B2B API teams.

## Target Profile

Best-fit interviewees:

- B2B SaaS teams with public or partner APIs
- teams seeing customers use AI agents or automation scripts
- APIs with high-risk actions such as purchasing, refunds, data export, account changes, or workflow execution
- backend, platform, security, or developer experience owners

Avoid spending early cycles on:

- teams that only need LLM observability
- teams without external APIs
- teams looking only for token cost tracking
- teams that require full enterprise IAM before any trial

## Opening

TrustMesh is exploring an authorization layer for AI agents calling B2B APIs. The goal is to let APIs verify which agent is calling, who authorized it, what it can do, and whether the current request is outside scope.

## Discovery Questions

- Do your customers or internal teams use AI agents or automation to call your API today?
- How do you identify automated callers right now?
- Are API keys enough for agent-based workflows?
- What actions in your API would be risky if an agent performed them incorrectly?
- Do you need to know who authorized an agent?
- Do you need per-action or per-resource scopes?
- Do you need limits such as per-operation amount caps?
- How do you revoke agent access today?
- How do you audit what an automation did after the fact?
- What would make you comfortable allowing third-party agents to call your API?

## Demo Prompts

After showing the procurement demo, ask:

- Does the credential model match how you think about API access?
- Are `audience`, `allowed_actions`, `resource_scope`, and `spending_limit_usd` enough for a first integration?
- Which claim is missing?
- Which deny reason would your team need to see in logs?
- Would you rather call a hosted verify API or use a local SDK/middleware?
- Where would this sit in your stack?

## Buying Signal Questions

- Would you connect this to a staging API?
- Who else on your team would need to approve it?
- What security review would this need?
- If this worked, what problem would it replace?
- Would this be a developer tool, security tool, or platform tool for your team?
- What would you pay for: verification volume, agents, credentials, or seats?

## Strong Signals

Strong positive signals:

- They already see agent/API automation.
- They have high-risk API actions.
- They dislike shared API keys for agents.
- They need auditability.
- They ask about staging integration.
- They describe a concrete workflow and actions.

Weak signals:

- They only ask for observability.
- They have no external API.
- They see this as theoretical.
- They need a full IAM suite immediately.

## Notes Template

```text
Company:
Role:
API domain:
Agent use case:
Risky actions:
Current auth method:
Revocation needs:
Audit needs:
Required claims:
Integration preference:
Main objection:
Staging interest:
Follow-up:
```
