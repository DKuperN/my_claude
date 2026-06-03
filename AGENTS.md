# My Claude Agent System

## How to start

**New to the system?** Run the interactive guide:
  codemie-claude
  > /guide

**Ready to work?** Use a slash command:
  codemie-claude
  > /task Build a CMS app with React frontend and Express backend
  > /onboard C:/PROJECTS/myapp
  > /review-branch PROJ-123 in project at C:/PROJECTS/myapp

**Or the full manual way:**
  codemie-claude
  > Read AGENTS.md and agents/orchestrator.md. You are the orchestrator. Task: <your task here>

## Agents
- orchestrator.md — reads your task, manages all agents
- analyst.md — writes spec and acceptance criteria, consults, accepts result
- developer.md — writes all code
- qa.md — tests and reports bugs

## Permissions
Pre-approved for this folder. No confirmations needed.

## Project output
Each project gets its own folder:
  C:/PROJECTS/my_claude/<project-name>/
  C:/PROJECTS/my_claude/<project-name>/_agent_context/
