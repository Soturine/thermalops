# ADR-0002: Separate temporary privileged helper

- Status: Accepted in principle; implementation details require M2 threat-model review
- Date: 2026-09-07

## Context

Some support actions require administrative privilege, but keeping the entire desktop application elevated increases attack surface and conflicts with least privilege and portable safety.

## Decision

Portable Pro will keep the main UI/application process at standard-user integrity and launch a temporary elevated helper only for an approved repair plan.

The helper exposes a small, versioned, strongly typed local IPC protocol containing only allowlisted capabilities.

## Required properties

- UAC only when needed;
- no persistent service in portable mode;
- no arbitrary command/shell/script execution;
- restrictive local IPC ACL;
- session binding/nonce;
- caller validation where practical;
- helper revalidates resource identity and policy;
- bounded request sizes;
- per-action timeout;
- structured response;
- termination and cleanup after use;
- audit trail linking plan/request/result.

## Rejected design

Running the entire UI permanently as administrator.

Reason: unnecessary privilege for read-only diagnosis and much larger attack surface.

## Rejected capability

`ExecuteCommand(string)` or equivalent generic privileged method.

Reason: converts a narrow repair helper into an arbitrary local privilege execution service.

## Follow-up questions for M2

- exact IPC technology (named pipe is preferred candidate);
- ACL and integrity-level requirements;
- process/caller identity verification details;
- nonce/token lifecycle;
- helper binary extraction/location strategy for single-file Portable;
- crash recovery and orphan cleanup;
- signing/verification relationship between UI and helper.
