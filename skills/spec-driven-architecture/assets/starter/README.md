# Starter layout

This tree is a valid spec-driven sample. It is not a product.

## Empty repository

Copy this whole directory to the repository root. In that same session, rename the sample `app` system, service, and contract to the real product. Do not leave the sample beside the real service.

## Repository that already has code

Copy only this shell, then model the deployables that already exist:

- `likec4.config.json`
- `package.json` (merge the three scripts and the dev dependencies)
- `.gitignore`
- `AGENTS.md` (replace the sample ids)
- `scripts/check_spec_links.py`
- `specs/architecture/00-specification.c4`
- `specs/workspace.c4` (replace the sample actors)
- `specs/adr/0001-record-architecture-decisions.md`

Do not copy `services/app/`, `specs/app/`, or the sample bodies in `specs/architecture/model/` and `specs/architecture/views/`. Add one element per existing deployable, using its current name and stack, and link the element to the code that implements it.
