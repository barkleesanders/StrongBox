import subprocess
import sys
import base64
import json
from pathlib import Path

import pytest
from cryptography.fernet import InvalidToken

import strongbox


def test_legacy_crypto44_ciphertext_remains_readable():
    fixture = json.loads((Path(__file__).parent / "fixtures" / "legacy-crypto44.json").read_text())
    assert strongbox.decrypt_data(base64.b64decode(fixture["ciphertext_base64"]),
        fixture["fixture_password"]) == base64.b64decode(fixture["plaintext_base64"])


def test_encryption_roundtrip_uses_fresh_salt():
    data = b"software fixture\x00\xff"
    first = strongbox.encrypt_data(data, "fixture password")
    second = strongbox.encrypt_data(data, "fixture password")
    assert first != second
    assert strongbox.decrypt_data(first, "fixture password") == data
    with pytest.raises(InvalidToken):
        strongbox.decrypt_data(first, "wrong fixture password")
    with pytest.raises(InvalidToken):
        strongbox.decrypt_data(first[:-1], "fixture password")


def test_cli_files_roundtrip_and_wrong_password(tmp_path):
    plain = tmp_path / "plain.bin"
    cipher = tmp_path / "cipher.bin"
    restored = tmp_path / "restored.bin"
    plain.write_bytes(bytes(range(256)))
    script = Path(strongbox.__file__).resolve()
    for action, source, target in [("encrypt", plain, cipher), ("decrypt", cipher, restored)]:
        result = subprocess.run([sys.executable, str(script), action, "--input", str(source),
            "--output", str(target), "--password", "fixture password"], capture_output=True, timeout=10)
        assert result.returncode == 0, result.stderr.decode()
    assert restored.read_bytes() == plain.read_bytes()
    failed = tmp_path / "must-not-exist.bin"
    result = subprocess.run([sys.executable, str(script), "decrypt", "--input", str(cipher),
        "--output", str(failed), "--password", "wrong fixture password"], capture_output=True, timeout=10)
    assert result.returncode != 0
    assert not failed.exists()
