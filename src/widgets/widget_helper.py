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
    def create_tab(self, *tab_contents, tab_titles=None):
        """Create a tab widget with specified contents and titles."""
        tab = widgets.Tab()
        tab.children = [widgets.VBox([content]) for content in tab_contents]
        if tab_titles:
            for i, title in enumerate(tab_titles):
                tab.set_title(i, title)
        return tab

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