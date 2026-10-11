# spec-driven-architecture

Спека до кода: LikeC4 держит топологию, TypeSpec — контракты, Mermaid — поведение во времени, а код и спеки ссылаются друг на друга. Скилл ниже переносит этот принцип в любой новый репозиторий.

Spec before code. LikeC4 holds topology, TypeSpec holds contracts, Mermaid holds behavior over time, and code links back to those specs. The skill teaches an agent to start and extend a repository that way. The split comes from a production multi-service game repository; the skill does not depend on that repository.

The worked sample is [skills/spec-driven-architecture/assets/starter](skills/spec-driven-architecture/assets/starter). The rules are [skills/spec-driven-architecture/SKILL.md](skills/spec-driven-architecture/SKILL.md).

## Install

The skill directory is `skills/spec-driven-architecture`.

```bash
npx skills add brianconnoly/spec-driven-architecture
```

Pick agents with `-a` when you do not want the default set:

```bash
npx skills add brianconnoly/spec-driven-architecture -a claude-code -a codex -a cursor -a github-copilot
```

Claude Code can also add this repo as a plugin marketplace:

```text
/plugin marketplace add brianconnoly/spec-driven-architecture
/plugin install spec-driven-architecture@spec-driven-architecture
```

Grok reads `SKILL.md` from `~/.grok/skills/` or from `<repo>/.grok/skills/`. Copy the skill directory there. The skills CLI agent list does not include Grok.

```bash
mkdir -p ~/.grok/skills
cp -R skills/spec-driven-architecture ~/.grok/skills/spec-driven-architecture
```

## Where else this can live

One public GitHub repository is the source. The stores below read that repository or accept a pointer to it. Nothing here uploads the skill to a second host.

| Place | What to do |
| --- | --- |
| skills.sh | `npx skills add brianconnoly/spec-driven-architecture` fetches this repo. The directory lists a skill after clients install it. There is no separate upload. |
| Claude Code | Marketplace file is already in `.claude-plugin/marketplace.json`. Users add the GitHub repo. Anthropic does not review third-party marketplaces. |
| Codex, Cursor, Copilot, VS Code, Gemini CLI, and the other agents on skills.sh | Same `npx skills add` command with `-a <agent>`. |
| Grok | Copy the skill folder, as above. |
| LobeHub, SkillGild, awesome-lists | A listing is a pull request or a form on that site. Do that only when you want the extra directory. The install path stays this repo. |

## Check

```bash
python3 -m unittest skills/spec-driven-architecture/scripts/test_check_spec_links.py
```

The starter also validates with LikeC4 and TypeSpec after `npm install` in a copy of `assets/starter`:

```bash
npm run specs:links
npm run likec4:check
npm run typespec:check
```
