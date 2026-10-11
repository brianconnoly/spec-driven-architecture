# Validation

Run these from the repository root after any change to a `.c4`, `.tsp`, `.mmd`, or link marker.

```bash
python3 scripts/check_spec_links.py
npx likec4 validate --no-layout .
npx tsp compile path/to/touched.tsp --no-emit
```

The starter's npm scripts are `specs:links`, `likec4:check`, and `typespec:check`. Install `likec4` and `@typespec/compiler` plus `@typespec/http` as dev dependencies before the `npx` forms, or use the versions in the starter `package.json`.

`scripts/check_spec_links.py` lives in this skill at `scripts/check_spec_links.py`. The starter carries the same file. Copy it into a bootstrapped repo and keep the two copies identical when you change the checker.

The checker fails when:

- a LikeC4 `link` target is missing
- an `Architecture`, `Contract`, `Flow`, or `Implementation` marker points at a missing path or an id that is not declared in that `.c4` file
- a `.tsp` file with `@service`, or a `specs/**/*.mmd` file, is not the target of a LikeC4 `link`
- a source file that is itself a LikeC4 `link` target has no `Architecture` marker

`likec4 validate` checks that the model parses and that views refer to real elements. `tsp compile --no-emit` checks that the contract parses and its types line up. Neither command proves runtime ordering, atomicity, or recovery. Those stay in tests against the implementation.

Copy the checker into a repo that did not start from the starter:

```bash
mkdir -p scripts
cp skills/spec-driven-architecture/scripts/check_spec_links.py scripts/check_spec_links.py
```

Adjust the source path to wherever this skill is installed.
