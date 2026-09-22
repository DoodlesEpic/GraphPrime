# Repository workflow

- Start each task from an up-to-date `dev` and create a dedicated task branch before making changes.
- Integrate completed tasks into `dev`, push to both `origin` and `gitlab`, and verify the CI build and performance checks using `gh`.
- Promote `dev` to `main` only when the user confirms that the day's work is complete and CI has passed. Do not move release tags for ordinary tasks.
- Use English Conventional Commits without a parenthesized scope.
- Never commit `RELEASE_PLAN.md`.
- Explain progress to the user throughout the work.
- See `docs/performance.md` for benchmark execution and baseline changes.

# Code and documentation

- Keep code simple, concise, and easy for humans to read. Avoid unnecessary abstractions without sacrificing performance.
- Write direct, concise documentation. Avoid em dashes, excessive semicolons, filler, and verbose AI-style prose.
- Never change `README.md` without the programmer's explicit authorization.
- Name implementation reports and plans in `docs` as `YYYY-MM-DD-topic.md` and include the date in a heading.
- Use the actual date of the documented event or result. Do not present historical results as current checks.
- Keep versioned release-note filenames. Permanent guides may also keep their existing names.
