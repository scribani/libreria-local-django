from datetime import date, timedelta

from django.test import SimpleTestCase
from django.utils import timezone

from catalogo.views import FormRenovarLibro


class RenovarLibroFormTest(SimpleTestCase):
    today = date.today()

    def test_fecha_label_and_help_text(self):
        form = FormRenovarLibro()

        self.assertTrue(form.fields['fecha_de_devolucion'].label == 'Fecha de renovacion')
        self.assertEqual(form.fields['fecha_de_devolucion'].help_text, 'Mínimo: mañana - Máximo: 4 semanas')

    def test_fecha_out_of_bounds(self, today=today):
        future = today + timedelta(days=1, weeks=4)
        form_today = FormRenovarLibro(data={'fecha_de_devolucion': today})
        form_future = FormRenovarLibro(data={'fecha_de_devolucion': future})

        self.assertFalse(form_today.is_valid())
        self.assertFalse(form_future.is_valid())

    def test_fecha_limits(self, today=today):
        tomorrow = today + timedelta(days=1)
        last_day = today + timedelta(weeks=4)
        form_tomorrow = FormRenovarLibro(data={'fecha_de_devolucion': tomorrow})
        form_last_day = FormRenovarLibro(data={'fecha_de_devolucion': last_day})

        self.assertTrue(form_tomorrow.is_valid())
        self.assertTrue(form_last_day.is_valid())
