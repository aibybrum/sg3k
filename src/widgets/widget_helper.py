import ipywidgets as widgets
from IPython.display import display
from utils import ErrorHandler


class WidgetHelper:
    @ErrorHandler.log_exceptions
    def create_html_label(self, text, bold=False, margin='0'):
        """Create an HTML label widget."""
        if bold:
            text = f"<b>{text}</b>"
        return widgets.HTML(value=text, layout=widgets.Layout(margin=margin))

    @ErrorHandler.log_exceptions
    def create_widget(self, widget_type, **kwargs):
        """Generic method to create a widget of the specified type."""
        return widget_type(**kwargs)

    @ErrorHandler.log_exceptions
    def create_labeled_widget(self, label, widget, margin='0'):
        """Create a labeled widget with customizable margins."""
        return widgets.VBox(
            [self.create_html_label(label, bold=True), widget],
            layout=widgets.Layout(margin=margin)
        )

    @ErrorHandler.log_exceptions
    def create_tab(self, description_content, settings_content):
        """Create a tab widget with description and settings."""
        tab = widgets.Tab()
        tab.children = [widgets.VBox([description_content]), widgets.VBox([settings_content])]
        tab.set_title(0, 'Description')
        tab.set_title(1, 'Settings')
        return tab

    # @ErrorHandler.log_exceptions
    # def display_visualization(self, title, description, details, interactive_plot, selectors):
    #     """Display the visualization with description and settings."""
    #     description_content = self._load_description_template(title, description, details)
    #     settings_content = widgets.HBox([widgets.VBox(selectors)])
    #     tab = self.create_tab(description_content, settings_content)
    #     display(tab, interactive_plot)

    # def _load_description_template(self, title, description, details):
    #     """Load and populate the description template."""
    #     details_html = "".join(
    #         f"<b>{detail['label']}:</b> {detail['content']}<br>" for detail in details
    #     )
    #     return widgets.HTML(value=f"<h3>{title}</h3><p>{description}</p>{details_html}")

    @ErrorHandler.log_exceptions
    def create_dropdown(self, options, value, description='', width='auto'):
        """Create a dropdown widget."""
        return self.create_widget(widgets.Dropdown, options=options, value=value, description=description,
                                  layout=widgets.Layout(width=width))

    @ErrorHandler.log_exceptions
    def create_select_multiple(self, options, value, description='', width='300px'):
        """Create a SelectMultiple widget."""
        return self.create_widget(widgets.SelectMultiple, options=options, value=value, description=description,
                                  layout=widgets.Layout(width=width))

    @ErrorHandler.log_exceptions
    def create_checkbox(self, value, description='', disabled=False, indent=False, width='auto'):
        """Create a checkbox widget."""
        return self.create_widget(widgets.Checkbox, value=value, description=description, disabled=disabled,
                                  indent=indent, layout=widgets.Layout(width=width))

    @ErrorHandler.log_exceptions
    def create_float_text(self, value, description='', width='auto'):
        """Create a float text widget."""
        return self.create_widget(widgets.FloatText, value=value, description=description,
                                  layout=widgets.Layout(width=width))

    @ErrorHandler.log_exceptions
    def create_int_text(self, value, description='', width='auto'):
        """Create an int text widget."""
        return self.create_widget(widgets.IntText, value=value, description=description,
                                  layout=widgets.Layout(width=width))