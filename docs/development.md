# Development

## Requirements

- Python 3.11 or newer.
- A browser that can open `http://127.0.0.1:8000`.
- PowerShell on Windows, or an equivalent shell using the same Python commands.

## Install

From the repository root:

```powershell
python -m pip install -e ".[dev]"
```

This installs the app plus development dependencies:

- `fastapi`
- `uvicorn`
- `pydantic`
- `pytest`
- `httpx`

## Run On Localhost

Start the development server:

```powershell
python -m uvicorn sgs_calculator.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

The `--reload` flag restarts the server when Python files change. Static files are served directly, so most HTML, CSS, and JavaScript edits appear after a browser refresh.

If port `8000` is busy:

```powershell
python -m uvicorn sgs_calculator.main:app --reload --port 8001
```

Then open:

```text
http://127.0.0.1:8001
```

## Test

Run the full test suite:

```powershell
python -m pytest
```

Useful checks while editing the frontend:

```powershell
node --check sgs_calculator/static/app.js
```

## API Smoke Check

With the server running:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/example
```

The browser UI uses `/api/simulate` when `Start Battle` is pressed.

## Troubleshooting

If the browser reports a validation error, open `View JSON` and check the generated payload. Common causes:

- Attacker or defender side name is blank in manually edited JSON.
- A side has no surviving combat unit.
- A unit has `strength` greater than `max_strength`.
- Duplicate unit IDs exist within one side.

If imports fail, reinstall the editable package:

```powershell
python -m pip install -e ".[dev]"
```
