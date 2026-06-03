# Rule: Code Quality Standards

ALWAYS apply these rules. No exceptions.

## Output standards
- NEVER leave commented-out code in final output
- NEVER use console.log in production code — use structured logging (JSON, with level + timestamp)
- NEVER hardcode ports, URLs, API keys, or secrets — use environment variables
- NEVER create a file over 200 lines — split by responsibility
- NEVER use magic numbers — name your constants

## Design standards
- ALWAYS give functions a single clear responsibility
- ALWAYS prefer explicit over clever — readable code beats smart code
- ALWAYS use named exports (exception: React components may use default export)
- NEVER use deep relative imports (../../..) — use path aliases configured in tsconfig/vite
- NEVER create circular dependencies

## TypeScript-specific (always on TypeScript projects)
- ALWAYS use strict mode — no exceptions
- NEVER use `any` — use `unknown` and narrow with type guards
- ALWAYS add explicit return types on public functions
- ALWAYS use `readonly` for data that should not be mutated
- NEVER return null and undefined from the same function — pick one
