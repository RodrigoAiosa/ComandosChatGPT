import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from commands.catalog import COMMANDS
from commands.playbooks import PLAYBOOKS, get_playbook_by_id

VALID_COMMANDS = {c["command"] for c in COMMANDS}


def test_every_playbook_has_id_title_description_and_steps():
    for playbook in PLAYBOOKS:
        assert playbook["id"]
        assert playbook["title"]
        assert playbook["description"]
        assert len(playbook["steps"]) >= 2


def test_every_playbook_step_references_existing_command():
    for playbook in PLAYBOOKS:
        for step in playbook["steps"]:
            assert step["command"] in VALID_COMMANDS, (
                f"Playbook '{playbook['id']}' referencia comando inexistente: {step['command']}"
            )
            assert step["note"]


def test_playbook_ids_are_unique():
    ids = [pb["id"] for pb in PLAYBOOKS]
    assert len(ids) == len(set(ids))


def test_get_playbook_by_id_found():
    first = PLAYBOOKS[0]
    result = get_playbook_by_id(first["id"])
    assert result == first


def test_get_playbook_by_id_not_found():
    assert get_playbook_by_id("inexistente") is None
