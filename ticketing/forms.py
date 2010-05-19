from django import forms

QTY_CHOICES = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
)

class TicketQtyForm(forms.Form):

    def __init__(self, *args, **kwargs):
        tickets = kwargs.pop('tickets')
        super(TicketQtyForm, self).__init__(*args, **kwargs)

        for i, ticket in enumerate(tickets):
            self.fields['qty_%s' % ticket.id] = forms.ChoiceField(label=ticket, choices=QTY_CHOICES)

    def tickets(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('qty_'):
                yield (name.replace('qty_', ''), value)

