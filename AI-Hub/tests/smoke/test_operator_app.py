from ai_hub.presentation.operator_ui.app import build_initial_snapshot, main


class _Column:
    def metric(self, *args): pass


class _UI:
    def __init__(self): self.configured = False
    def set_page_config(self, **kwargs): self.configured = True
    def title(self, value): pass
    def caption(self, value): pass
    def columns(self, count): return [_Column() for _ in range(count)]
    def subheader(self, value): pass
    def dataframe(self, value, **kwargs): pass


def test_operator_app_starts_without_provider_credentials() -> None:
    snapshot = build_initial_snapshot()
    assert snapshot.router_ready is False
    ui = _UI()
    main(ui)
    assert ui.configured is True
