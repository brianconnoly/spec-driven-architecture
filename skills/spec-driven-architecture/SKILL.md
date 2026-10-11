---
name: spec-driven-architecture
description: >
  Use when starting a repository, adding or changing a service, public API,
  schema, protocol, store, or cross-component flow, or when the user mentions
  spec-driven development, LikeC4, TypeSpec, Mermaid, .c4, .tsp, or .mmd.
  Places topology in LikeC4, contracts in TypeSpec, and behavior over time
  in Mermaid, and keeps links from those specs to code and back.
license: MIT
compatibility: Requires Node.js for LikeC4 and TypeSpec checks, and Python 3 for the link checker.
metadata:
  author: brianconnoly
  version: "0.1.0"
---

# Spec-driven architecture

Topology, contracts, and behavior over time each have one home. Code implements those homes and points back at them.

| Home | Path | Owns |
| --- | --- | --- |
| LikeC4 | `specs/**/*.c4` | Elements, relationships, technology, and the names code uses |
| TypeSpec | `specs/**/*.tsp` | Public operations, message models, persistence shapes |
| Mermaid | `specs/**/*.mmd` | Flows, sequences, and states |
| ADR | `specs/adr/` | Why a choice was made, when the model does not already show it |
| Code | implementation tree | Behavior of the elements above |

A README or wiki may explain the product. Link it from the element. Do not paste `.c4` or `.tsp` into it. A hand-written OpenAPI file is not a second contract: when a `.tsp` exists, OpenAPI is compiler output.

`specs/workspace.c4` is only the shell: actors, the system, and person-to-system links. Containers, components, and stores go in `specs/architecture/model/`.

## When to open the model

Open the model before editing code when the change adds or moves a deployable, component, protocol, store, public type, route, subject, or table.

A change that stays inside one existing element, and does not add a public type or a relationship, keeps the current ids. Still do not invent a public name in code.

Search `.c4` by the words of the task (domain, service, protocol, store). Start a user-visible capability from `specs/architecture/views/features/`, then open the elements that view includes.

## Order

1. If the repo has no `specs/workspace.c4`, bootstrap from [assets/starter](assets/starter). On an empty repo, copy the whole starter, then rename the sample `app` element to the real product in that same session. On a repo that already has code, copy only the shell listed in the starter `README`, and model the deployables that already exist. Do not leave the sample service beside real code.
2. Add or change the element in the thematic model file. The LikeC4 id is the code name (`billingApi`, not a later alias). The `technology` value is the stack the code uses; change them in the same edit.
3. A new or changed public type, route, subject, or table goes in a `.tsp` file, and the element `link`s that file, before the handler is written.
4. A new or changed lifecycle goes in a `.mmd` file, and the element `link`s that file, before the sequence is coded.
5. Implement. The owning module carries the markers in [references/links.md](references/links.md).
6. Run the checks in [references/validation.md](references/validation.md). A touched contract is not done when only the code tests pass.

## Shape of the model

- Cross-container arrows end on a boundary component, not on the container as a whole. Use one suffix for the role: `Api`, `HttpEndpoint`, `Listener`, `Publisher`, `Subscriber`, `Store`, `Writer`, `Reader`, `RepositoryAdapter`, `RuntimeAdapter`.
- A cross-container arrow has one kind, written `source -[http]-> target 'what crosses' { technology 'concrete protocol' }`. The starter defines `http`, `storageRead`, and `storageWrite`. A queue or stream uses one shared `async` kind. Add a narrower kind only when two crossings share that narrower meaning. Use `config` or `telemetry` when that is the main effect, even if the bytes travel over HTTP. Split an arrow that both reads and writes, or that uses two protocols.
- Same-container calls are untyped.
- Tags are the first lines inside an element: `runtime`, `admin`, `debug`, `observability`, `storage`, `shared`, `legacy`, `deprecated`. No `deprecated` tag means the element is current.
- Title and description use the words a later search would use. The description is one to three sentences on responsibility. Field lists, algorithms, and migration history belong in the linked contract, flow, or ADR.
- A new user-visible capability adds `specs/architecture/views/features/<feature>.c4` and includes the boundary components that carry it.
- In multi-file models, refer to elements by full name (`app.billingApi`), including across files.

## Red flags

Stop and put the fact in its home before more code.

| Excuse | What to do |
| --- | --- |
| The diagram can wait until the service works | The id and the technology are part of this change. Write the element first. |
| It is only one endpoint | A new public type or route is a contract. Write the `.tsp`, then the handler. |
| `workspace.c4` is the architecture file | It is the shell. Put the container in `specs/architecture/model/`. |
| The README already explains this | Link the README from the element. Prose is not the model or the contract. |
| One Mermaid diagram is the map | Mermaid owns time. LikeC4 owns who talks to whom. |
| The hand-written OpenAPI file is the source | The `.tsp` is the source. Generate OpenAPI from it. |
| `tsp compile` passed, so the behavior is right | The compiler checks names and types. Ordering, atomicity, and recovery stay in code and tests. |
| This internal call needs its own relationship kind | Kinds are for crossings between containers. |
| Name the package now and align the model later | The LikeC4 id is the name. |

## Done

- The element id matches the code name, and `technology` matches the stack.
- Every new public type or route is in a linked `.tsp`.
- Every new lifecycle is in a linked `.mmd`.
- Every cross-container arrow uses one kind and a boundary component.
- The owning module has the markers from [references/links.md](references/links.md).
- `specs:links`, `likec4 validate`, and `tsp compile --no-emit` for each touched `.tsp` are green.
