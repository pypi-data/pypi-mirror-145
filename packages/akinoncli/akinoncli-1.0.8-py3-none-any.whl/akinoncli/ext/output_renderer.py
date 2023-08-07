from cement.core.output import OutputHandler
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rich_print
from rich.markup import escape

class BaseRenderer:
    def __init__(self, *args, **kwargs):
        self.run_validations(*args, **kwargs)
        self.render(*args, **kwargs)

    def run_validations(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        pass


class TableRenderer(BaseRenderer):
    def run_validations(self, *args, **kwargs):
        rows = kwargs.get('rows')
        assert rows is not None
        assert isinstance(rows, list)

        headers = kwargs.get('headers')
        assert headers is not None
        assert isinstance(headers, dict)

    def render(self, *args, **kwargs):
        headers = kwargs.get('headers')
        rows = kwargs.get('rows')
        table = Table()
        for column_header in headers.values():
            table.add_column(column_header)

        for datum in rows:
            row = list()
            for col in headers.keys():
                value = datum[col]
                if isinstance(value, bool):
                    value = 'Yes' if value else 'No'
                row.append(str(value))
            table.add_row(*row)

        console = Console(highlight=False)
        console.print(table)


class RealtimeLogRenderer(BaseRenderer):
    def run_validations(self, *args, **kwargs):
        rows = kwargs.get('rows')
        assert rows is not None
        assert isinstance(rows, list)

    def render(self, *args, **kwargs):
        rows = kwargs.get('rows')
        text = ''
        for row in rows:
            text += f'[bold]{row.get("application_type")}:[/bold] {row.get("message")}\n'

        console = Console(highlight=False)
        console.print(text)


class TextRenderer(BaseRenderer):
    def render(self, *args, **kwargs):
        text = kwargs.get('custom_text')
        print(text)


class PipelineLogRenderer(BaseRenderer):
    def render(self, *args, **kwargs):
        rows = kwargs.get('rows', [])
        if not rows:
            rich_print(Panel("No log found."))
        for row in rows:
            rich_print(Panel(f'{escape(row.get("log_data"))}', title=f"[bold][red]{row.get('created_date')}[/]"))


class AkinonOutputHandler(OutputHandler):
    renderers = {
        "text": TextRenderer,
        "realtime_log": RealtimeLogRenderer,
        "table": TableRenderer,
        "pipeline_log": PipelineLogRenderer
    }

    class Meta:
        label = 'akinon_output_handler'

    def render(self, data, *args, **kwargs):
        renderer_type = kwargs.pop('renderer_type', 'table')
        is_succeed = kwargs.pop('is_succeed', False)
        if is_succeed or renderer_type == 'text':
            self.renderers.get(renderer_type)(*args, **kwargs)
        else:
            self.app.log.error(data)
