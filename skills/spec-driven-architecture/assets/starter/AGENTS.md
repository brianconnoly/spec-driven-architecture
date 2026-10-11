# Agent notes

Architecture facts have one home:

- LikeC4 under `specs/` — elements, relationships, technology, and names
- TypeSpec `specs/**/*.tsp` — public types and operations
- Mermaid `specs/**/*.mmd` — flows, sequences, and states
- `specs/adr/` — why, when the model does not already show the reason

`specs/workspace.c4` stays the shell: actors, the system, and person-to-system links. Containers and components go in `specs/architecture/model/`.

The module that owns a boundary starts with:

```text
Architecture: specs/architecture/model/app.c4 -> app.appApi.httpApi
Contract: specs/app/app-api.tsp
Flow: specs/app/request-flow.mmd
```

After a spec or link change, run `npm run specs:links`, `npm run likec4:check`, and `npm run typespec:check`.

Install the `spec-driven-architecture` skill for the full rules. The sample `app` service exists so those checks pass on a new tree. Replace it with the real product in the same session you adopt this starter.
