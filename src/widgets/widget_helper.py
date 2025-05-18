import ipywidgets as widgets
from IPython.display import display


class WidgetHelper:
    def create_html_label(self, text, bold=False):
        """Create an HTML label widget."""
        if bold:
            text = f"<b>{text}</b>"
        return widgets.HTML(value=text)
    
    def create_dropdown(self, options, value, description='', width='auto'):
        """Create a dropdown widget."""
        return widgets.Dropdown(
            options=options,
            value=value,
            description=description,
            disabled=False,
            layout=widgets.Layout(width=width)
        )
    
    def create_select_multiple(self, options, value, description='', width='300px'):
        """Create a SelectMultiple widget."""
        return widgets.SelectMultiple(
            options=options,
            value=value,
            description=description,
            disabled=False,
            layout=widgets.Layout(width=width)
        )

    def create_checkbox(self, value, description='', disabled=False, indent=False, width='auto'):
        """Create a checkbox widget."""
        return widgets.Checkbox(
            value=value,
            description=description,
            disabled=disabled,
            indent=indent,
            layout=widgets.Layout(width=width)
        )
    
    def create_float_text(self, value, description='', width='auto'):
        """Create a float text widget."""
        return widgets.FloatText(
            value=value,
            description=description,
            disabled=False,
            layout=widgets.Layout(width=width)
        )

    def create_int_text(self, value, description='', width='auto'):
        """Create an int text widget."""
        return widgets.IntText(
            value=value,
            description=description,
            disabled=False,
            layout=widgets.Layout(width=width)
        )

    def create_labeled_widget(self, label, widget):
        """Create a labeled widget."""
        return widgets.VBox([self.create_html_label(label, bold=True), widget])
    
    def create_tab(self, description_content, settings_content):
        """Create a tab widget with description and settings."""
        tab = widgets.Tab()
        tab.children = [widgets.VBox([description_content]), widgets.VBox([settings_content])]
        tab.set_title(0, 'Description')
        tab.set_title(1, 'Settings')
        return tab
    
    def display_visualization(self, description_text, interactive_plot, selectors):
        """Display the visualization with description and settings."""
        description_content = widgets.HTML(value=description_text)
        settings_content = widgets.HBox([widgets.VBox(selectors)])
        tab = self.create_tab(description_content, settings_content)
        display(tab, interactive_plot)

    def create_labeled_dropdown(self, label, options, value):
        """Create a labeled dropdown widget."""
        return self.create_labeled_widget(label, self.create_dropdown(options, value))

    def create_labeled_checkbox(self, label, value, description='', disabled=False):
        """Create a labeled checkbox widget."""
        return self.create_labeled_widget(label, self.create_checkbox(value, description=description, disabled=disabled))

    def create_labeled_float_text(self, label, value):
        """Create a labeled float text widget."""
        return self.create_labeled_widget(label, self.create_float_text(value))

    def create_labeled_int_text(self, label, value):
        """Create a labeled int text widget."""
        return self.create_labeled_widget(label, self.create_int_text(value))

    def create_description_tab(self, description_text):
        """Helper to create the description tab."""
        return widgets.VBox([widgets.HTML(value=description_text)])

    def create_settings_tab(self, selectors):
        """Helper to create the settings tab."""
        return widgets.VBox([widgets.HBox(selectors)])