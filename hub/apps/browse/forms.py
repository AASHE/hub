from django import forms
from django.utils.encoding import force_text


class LeanSelect(forms.Select):
    """
    Works like a regular SelectMultiple widget but only renders a list of
    initial values, rather than the full list of choices.
    """
    def render_options(self, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in self.choices:
            if not force_text(option_value) in selected_choices:
                continue
            output.append(self.render_option(
                selected_choices, option_value, option_label))
        return '\n'.join(output)


class LeanSelectMultiple(LeanSelect, forms.SelectMultiple):
    pass
