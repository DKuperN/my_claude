# Skill: React

## Component rules
- One component per file
- Keep components under 150 lines — split if larger
- Components do one thing — separate concerns
- Use functional components — no class components in new code
- Name components with PascalCase
- Name files same as component

## Props
- Define prop types explicitly with TypeScript interface
- Destructure props in function signature
- Avoid prop drilling more than 2 levels — use context or state management
- Never mutate props
- Use children prop for composition over configuration

## State management
- Use local state for UI-only state
- Lift state only as high as needed
- Use context for state shared across many components
- Keep state minimal — derive values instead of storing them
- Do not store derived data in state

## Hooks
- Follow rules of hooks — no conditional hook calls
- Custom hooks for reusable stateful logic
- Name custom hooks with use prefix
- useEffect dependencies must be complete and correct
- Clean up effects that create subscriptions or timers
- Avoid useEffect for data transformations — use useMemo

## Data fetching
- Handle loading, error, and empty states in every component that fetches
- Do not fetch in useEffect when a library (React Query, SWR) can handle it
- Cancel or ignore stale requests on cleanup
- Never store server state in Redux or context — use dedicated data fetching library

## Performance
- Do not premature optimise — profile first
- Use React.memo only when profiling shows it helps
- Use useCallback and useMemo only for expensive operations or stable references
- Avoid anonymous functions in JSX for stable references
- Use key prop correctly — never use array index as key for dynamic lists

## Accessibility
- Use semantic HTML elements
- Every interactive element must be keyboard accessible
- Images must have alt text
- Forms must have labels associated with inputs

## Security
- Never use dangerouslySetInnerHTML with user content
- If dangerouslySetInnerHTML is needed — sanitise first with DOMPurify
- Never store sensitive data in localStorage
