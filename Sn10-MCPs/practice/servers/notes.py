import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notes")


NOTES_FILE = Path(__file__).resolve().parent / "notes.json"


def _load() -> dict:
    return json.loads(NOTES_FILE.read_text()) if NOTES_FILE.exists() else {}

def _save(notes: dict):
    NOTES_FILE.write_text(json.dumps(notes, indent=2))


@mcp.tool()
def add_note(title: str, content: str) -> str:
    """Save a note with a title and content."""
    notes = _load()
    notes[title] = content
    _save(notes)
    return f"Note '{title}' saved."

@mcp.tool()
def get_note(title: str) -> str:
    """Retrieve a note by title."""
    notes = _load()
    return notes.get(title, f"No note found with title '{title}'.")

@mcp.tool()
def list_notes() -> str:
    """List all saved note titles."""
    notes = _load()
    return ", ".join(notes.keys()) if notes else "No notes saved yet."

@mcp.tool()
def delete_note(title: str) -> str:
    """Delete a note by title."""
    notes = _load()
    if title in notes:
        del notes[title]
        _save(notes)
        return f"Note '{title}' deleted."
    return f"Note '{title}' not found."


if __name__ == "__main__":
    mcp.run()