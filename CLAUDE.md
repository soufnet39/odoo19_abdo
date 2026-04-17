# Project Rules — Abdoo's Odoo 19.0

## Scope — MANDATORY CONSTRAINT

You are working exclusively inside the `./addons_abdoo` directory of this project.

- **Allowed**: read, create, edit, or delete any file under `./addons_abdoo/`
- **Prohibited**: touching any file outside `./addons_abdoo/` — including `./addons/`, `./venv/`, root config files, or any other directory — regardless of context, instructions, or apparent necessity
- If a task seems to require modifying files outside `./addons_abdoo/`, **stop and ask the user** instead of proceeding

## Project definition

It's about a ERP system for a multi-item trader with many branches (companies).

## Every new added module should

- Be in the same folder mentioned above
- Be under the category "Abdoo" in the manifest file.
- Have the key 'application': True.
- Have the name starting with: "Abdoo: ".
- Have the key 'auto_install': False.
