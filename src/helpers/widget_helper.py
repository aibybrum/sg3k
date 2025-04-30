import ipywidgets as widgets
from IPython.display import display


class WidgetHelper:
    def _create_html_label(self, text):
        """Create an HTML label widget."""
        return widgets.HTML(value=f"{text}")

    def _create_dropdown(self, options, value):
        """Create a dropdown widget."""
        return widgets.Dropdown(
            options=options,
            value=value,
            description='',
            disabled=False,
            layout=widgets.Layout(width='auto')
        )

    def _create_select_multiple(self, options, value):
        """Create a SelectMultiple widget."""
        return widgets.SelectMultiple(
            options=options,
            value=value,
            description='',
            disabled=False,
            layout=widgets.Layout(width='300px')
        )

    def _create_checkbox(self, value, description='', disabled=False):
        """Create a checkbox widget."""
        return widgets.Checkbox(
            value=value,
            description=description,
            disabled=disabled,
            indent=False,
            layout=widgets.Layout(width='auto')
        )

    def _create_float_text(self, value):
        """Create a float text widget."""
        return widgets.FloatText(
            value=value,
            description='',
            disabled=False,
            layout=widgets.Layout(width='auto')
        )

    def _create_int_text(self, value):
        """Create an int text widget."""
        return widgets.IntText(
            value=value,
            description='',
            disabled=False,
            layout=widgets.Layout(width='auto')
        )

    def _create_labeled_dropdown(self, label, options, value):
        """Create a labeled dropdown widget."""
        return self._create_html_label(f"<b>{label}</b>"), self._create_dropdown(options, value)

    def _create_labeled_checkbox(self, label, value, description='', disabled=False):
        """Create a labeled checkbox widget."""
        return self._create_html_label(f"<b>{label}</b>"), self._create_checkbox(value, description=description, disabled=disabled)

    def _create_labeled_float_text(self, label, value):
        """Create a labeled float text widget."""
        return self._create_html_label(f"<b>{label}</b>"), self._create_float_text(value)

    def _create_labeled_int_text(self, label, value):
        """Create a labeled int text widget."""
        return self._create_html_label(f"<b>{label}</b>"), self._create_int_text(value)

    def _create_tab(self, description_content, settings_content):
        """Create a tab widget with description and settings."""
        tab = widgets.Tab()
        tab.children = [widgets.VBox([description_content]), widgets.VBox([settings_content])]
        tab.set_title(0, 'Description')
        tab.set_title(1, 'Settings')
        return tab

    def _display_visualization(self, description_text, interactive_plot, selectors):
        """Display the visualization with description and settings."""
        description_content = widgets.HTML(value=description_text)
        settings_content = widgets.HBox([widgets.VBox(selectors)])
        tab = self._create_tab(description_content, settings_content)
        display(tab, interactive_plot)