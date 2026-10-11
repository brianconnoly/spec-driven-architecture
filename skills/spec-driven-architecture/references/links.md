# Link markers

Paths in code, TypeSpec, and Mermaid are repository-relative. LikeC4 `link` paths are relative to the `.c4` file that contains them. Every target must exist. A URL is not a stand-in for a file in the repo.

## Code

The module that owns the boundary starts with these lines. Use `//`, `///`, `//!`, or `#`, whichever the language uses. Omit `Contract` or `Flow` only when that file does not exist.

```text
Architecture: specs/architecture/model/app.c4 -> app.appApi.httpApi
Contract: specs/app/app-api.tsp
Flow: specs/app/request-flow.mmd
```

The path points at the model file that declares the element. The name after `->` is the full LikeC4 id. The last segment (`httpApi`) is the identifier in that file.

## LikeC4

```likec4
httpApi = component 'HTTP API' 'Accepts public HTTP commands.' {
  #runtime
  link ../../app/app-api.tsp
  link ../../app/request-flow.mmd
  link ../../../services/app/api.ts
}
```

Link the contract file, the flow file, and the owning source file. A directory link is only for a package that contains several files. A linked source file must contain an `Architecture` marker.

## TypeSpec

In the header of a service file:

```typespec
/**
 * Architecture: app.appApi.httpApi
 * Implementation: services/app/api.ts
 * Flow: specs/app/request-flow.mmd
 */
```

`Implementation` is the owning source file. Shared files that have no `@service` are imported by a service file; they do not need their own element.

## Mermaid

The first lines of the `.mmd` file:

```text
%% Architecture: specs/architecture/model/app.c4 -> app.appApi.httpApi
%% Contract: specs/app/app-api.tsp
```

The diagram names the same participants as the LikeC4 ids. It does not restate fields that the `.tsp` already defines.
