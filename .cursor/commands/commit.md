# Commit Guidelines

## Tasks

- Run `git status`
- Run `git diff --cached`
- Run `uv run ruff check --fix`
- Run `uv run ruff format`
- Run `uv run mypy sndtk`
- Run `git add` to necessary files
- Run `git commit`

## Commit Message Convention

For git commits, write a single, emoji-prefixed, imperative commit subject. Keep the subject under ~60 characters, no trailing period. Prefer small, focused commits and human-friendly language. Use lowercase after the emoji.

Format:

- Write commit messages in English
- Subject line only for simple changes: `EMOJI short imperative summary`
- Use actual emoji characters (not `:sparkles:`, but ✨)
- Optional body only when it adds necessary context (what/why, not how). Wrap body at ~72 chars. Avoid boilerplate.
- Do not add scope tags like `feat:` or `fix:`; use the emoji as the category indicator.
- Don’t end the subject with punctuation.
- Prefer multiple atomic commits over one omnibus commit.

Emoji categories to choose from:

| Emoji | Description                                                   |
| ----- | ------------------------------------------------------------- |
| 🩹    | Simple fix for a non-critical issue.                          |
| ⚗️    | Perform experiments.                                          |
| 👽️   | Update code due to external API changes.                      |
| 🚑️   | Critical hotfix.                                              |
| ⬇️    | Downgrade dependencies.                                       |
| ⬆️    | Upgrade dependencies.                                         |
| 🎨    | Improve structure / format of the code.                       |
| 🍻    | Write code drunkenly.                                         |
| 🍱    | Add or update assets.                                         |
| 🔖    | Release / Version tags.                                       |
| 💥    | Introduce breaking changes.                                   |
| 🧱    | Infrastructure related changes.                               |
| 🐛    | Fix a bug.                                                    |
| 🏗️    | Make architectural changes.                                   |
| 💡    | Add or update comments in source code.                        |
| 👥    | Add or update contributor(s).                                 |
| 📸    | Add or update snapshots.                                      |
| 🗃️    | Perform database related changes.                             |
| 📈    | Add or update analytics or track code.                        |
| 🚸    | Improve user experience / usability.                          |
| 🔐    | Add or update secrets.                                        |
| 🤡    | Mock things.                                                  |
| ⚰️    | Remove dead code.                                             |
| 🚧    | Work in progress.                                             |
| 👷    | Add or update CI build system.                                |
| 💫    | Add or update animations and transitions.                     |
| 🥚    | Add or update an easter egg.                                  |
| 🔥    | Remove code or files.                                         |
| 🌐    | Internationalization and localization.                        |
| 🥅    | Catch errors.                                                 |
| 💚    | Fix CI Build.                                                 |
| 🔨    | Add or update development scripts.                            |
| ➖    | Remove a dependency.                                          |
| ➕    | Add a dependency.                                             |
| 📱    | Work on responsive design.                                    |
| 🏷️    | Add or update types.                                          |
| 💄    | Add or update the UI and style files.                         |
| 🔒️   | Fix security or privacy issues.                               |
| 🔊    | Add or update logs.                                           |
| 🔍️   | Improve SEO.                                                  |
| 📝    | Add or update documentation.                                  |
| 💸    | Add sponsorships or money related infrastructure.             |
| 🧐    | Data exploration/inspection.                                  |
| 🔇    | Remove logs.                                                  |
| 👔    | Add or update business logic.                                 |
| 📦️   | Add or update compiled files or packages.                     |
| 📄    | Add or update license.                                        |
| 🛂    | Work on code related to authorization, roles and permissions. |
| ✏️    | Fix typos.                                                    |
| 💩    | Write bad code that needs to be improved.                     |
| 📌    | Pin dependencies to specific versions.                        |
| ♻️    | Refactor code.                                                |
| ⏪️   | Revert changes.                                               |
| 🚀    | Deploy stuff.                                                 |
| 🚨    | Fix compiler / linter warnings.                               |
| 🦺    | Add or update code related to validation.                     |
| 🙈    | Add or update a .gitignore file.                              |
| 🌱    | Add or update seed files.                                     |
| ✨    | Introduce new features.                                       |
| 💬    | Add or update text and literals.                              |
| 🩺    | Add or update healthcheck.                                    |
| 🎉    | Begin a project.                                              |
| 🧑‍💻    | Improve developer experience.                                 |
| 🧪    | Add a failing test.                                           |
| 🧵    | Add or update code related to multithreading or concurrency.  |
| 🚩    | Add, update, or remove feature flags.                         |
| 🚚    | Move or rename resources (e.g.: files, paths, routes).        |
| 🔀    | Merge branches.                                               |
| 🗑️    | Deprecate code that needs to be cleaned up.                   |
| ♿️   | Improve accessibility.                                        |
| ✅    | Add, update, or pass tests.                                   |
| 🔧    | Add or update configuration files.                            |
| ⚡️   | Improve performance.                                          |

Subjects should look like these real examples from the repo:

- `🔖 release 4.9.4`
- `🚀 deploy 4.9.2`
- `🐛 fix sorting on colormatch results page`
- `🐛 fix history issue and regaining lost tray`
- `🐛 fix collection mode exiting when searching`
- `💄 fix grab / grabbing cursor`
- `🚧 testing and moving computers`
- `⬆️ Bump django-htmx from 1.23.2 to 1.24.1`

Guidelines for dependency bumps:

- Use `⬆️ Bump <package> from <old> to <new>` in the subject.
- If you include a body, briefly note changelog/links and whether it’s major/minor.

Guidelines for releases/deploys:

- `🔖 release X.Y.Z` for tagging a new version.
- `🚀 deploy X.Y.Z` for pushing that version to production.

Tone and style:

- Imperative mood: “add”, “fix”, “update”, “bump”, “remove”.
- Keep it concise and specific; mention the user-visible area if relevant.
- Lowercase after the emoji unless a proper noun or version string requires caps.

Templates:

```
EMOJI short imperative summary

[Optional body: what changed and why; wrap at ~72 chars.]
```

```
🚀 release X.Y.Z
```

```
⬆️ Bump package-name from A.B.C to D.E.F

- optional: one-line reason or link to changelog
```

```
🐛 fix <specific bug or behavior>

- optional: brief why the bug happened or test added
```

Decision hints:

- Is it a user-facing bug fix? → 🐛
- Is it a release or deploy with a version? → 🚀
- Is it only a dependency version change? → ⬆️
- Is it purely visual/CSS/UI? → 💄
- Is it partial or exploratory work? → 🚧
- Otherwise choose the best-fit from the additional emojis.

More example subjects to emulate:

- `✨ add quick filter to inventory table`
- `♻️ refactor swatch query for readability`
- `🧪 add tests for library search pagination`
- `📝 document test settings and make targets`
- `🔧 update pytest config for coverage html`
- `🔥 remove unused static vendor files`

Do not:

- Do not use trailing periods or exclamation marks.
- Do not include scopes like `(app):` or `feat:` prefixes.
- Do not write long, multi-paragraph bodies unless truly necessary.
- Do not bundle unrelated changes under one commit.
