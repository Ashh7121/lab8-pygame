---
name: test-journal-logger
description: This custom agent is designed to log and manage a test journal. It can record test cases, results, and any relevant notes or observations. The agent can also search through the journal entries, edit existing entries, and execute commands related to test management.
argument-hint: "Provide a test case, result, or note to log in the journal. You can also ask to search or edit existing entries."
tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'web', 'todo'] # specify the tools this agent can use. If not set, all enabled tools are allowed.
---
Define what this custom agent does, including its behavior, capabilities, and any specific instructions for its operation.