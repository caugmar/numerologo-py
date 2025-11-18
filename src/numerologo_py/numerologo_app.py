from textual import on
from textual.app import App
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widgets import (
    Button, Footer, Header, Input, MaskedInput, Label, MarkdownViewer, Static
)
from markdownify import markdownify as md
from numerologo import Numerologo


class NumerologoApp(App):
    CSS_PATH = "numerologo_app.tcss"
    BINDINGS = [("f1", "ajuda", "Ajuda"),
                ("ctrl+q", "quit", "Sair"),
                ("ctrl+t", "toggle_dark", "Mudar tema")]

    def compose(self):
        yield Header(show_clock=True)
        with HorizontalGroup(id="painel"):
            with VerticalGroup(classes="nome"):
                yield Label(" Nome:")
                yield Input(placeholder="Nome do consulente", id="nome",
                            tooltip="Certifique-se de que o nome [b]esteja correto[/]")
            with VerticalGroup(classes="data"):
                yield Label(" Nascimento:")
                yield MaskedInput(template="99/99/9999", id="data",
                                  tooltip="Informe a data de nascimento [b]correta[/]")
            with VerticalGroup(classes="analisar"):
                yield Static()
                yield Button("Analisar", id="analisar",
                             tooltip="Clique aqui para iniciar a análise")
            viewer = MarkdownViewer(id="resultado")
        viewer.border_title = "[b]Resultado[/] da Análise"
        yield viewer
        yield Footer()

    def action_ajuda(self):
        AJUDA = """
        Informe o nome completo do consulente,
        seguido pela data de nascimento. Clique
        em "Analisar". O resultado será exibido
        no painel abaixo.
        """
        self.notify(AJUDA, timeout=10)

    @on(Button.Pressed, "#analisar")
    def analisar(self):
        viewer = self.query_one("#resultado")
        nome = self.query_one("#nome").value
        data = self.query_one("#data").value
        numerologo = Numerologo()
        analise = md(numerologo.analise(nome, data))
        viewer.document.update(analise)


if __name__ == "__main__":
    app = NumerologoApp()
    app.run()
