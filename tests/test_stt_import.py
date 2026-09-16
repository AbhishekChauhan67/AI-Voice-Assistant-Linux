import importlib


def test_stt_import_does_not_crash_when_sounddevice_is_missing(monkeypatch):
    import sys

    sys.modules.pop("src.STT.microphone", None)
    sys.modules.pop("src.STT.stt", None)

    real_import = __import__

    def fake_import(name, *args, **kwargs):
        if name == "sounddevice":
            raise ModuleNotFoundError("No module named 'sounddevice'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)

    mod = importlib.import_module("src.STT.stt")
    assert hasattr(mod, "STT")
