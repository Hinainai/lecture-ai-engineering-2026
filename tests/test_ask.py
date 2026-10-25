from types import SimpleNamespace

from app import ask as ask_module


def test_ask_prints_token_counts_and_returns_response(monkeypatch, capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=7),
        text="回答",
    )

    class FakeModels:
        def generate_content(self, **kwargs):
            return response

    class FakeClient:
        def __init__(self, *, api_key):
            self.models = FakeModels()

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("質問") == "回答"
    assert "入力: 12, 出力: 7" in capsys.readouterr().out


def test_ask_prints_unknown_when_usage_is_missing(monkeypatch, capsys):
    response = SimpleNamespace(usage_metadata=None, text="回答")

    class FakeModels:
        def generate_content(self, **kwargs):
            return response

    class FakeClient:
        def __init__(self, *, api_key):
            self.models = FakeModels()

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("質問") == "回答"
    assert "入力: 不明, 出力: 不明" in capsys.readouterr().out