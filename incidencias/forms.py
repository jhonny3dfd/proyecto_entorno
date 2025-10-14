# incidencias/forms.py

from django import forms
from .models import Solicitud

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        # Excluimos 'fecha_creacion' ya que tiene 'default=timezone.now' en el modelo
        # Mantenemos 'cuadrilla' como un campo opcional (null=True, blank=True)
        fields = ['cuadrilla', 'estado', 'observaciones', 'tipo_incidencia']

        # Opcional: Personalizar etiquetas
        labels = {
            'cuadrilla': 'Cuadrilla Asignada',
            'estado': 'Estado de la Solicitud',
            'observaciones': 'Observaciones/Notas',
            'tipo_incidencia': 'Tipo de Incidencia',
        }