# incidencias/forms.py

from django import forms
from .models import Solicitud, Encuesta, Resolucion, Multimedia # <-- Importar Multimedia

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        # Excluimos 'estado' ya que se inicializa en la vista
        fields = ['cuadrilla', 'observaciones', 'tipo_incidencia']

        labels = {
            'cuadrilla': 'Cuadrilla (Asignación inicial)',
            'observaciones': 'Notas Internas / Administrativas',
            'tipo_incidencia': 'Tipo de Incidencia',
        }

class EncuestaForm(forms.ModelForm):
    # Campo para la multimedia (no es un campo del modelo Encuesta, es solo para el formulario)
    # IMPORTANTE: Este campo NO está en el modelo Encuesta.
    archivo_adjunto = forms.FileField(
        label='Adjuntar Evidencia (Foto/Video)', 
        required=False
    )

    class Meta:
        model = Encuesta
        # **EXCLUIMOS** 'solicitud' y 'usuario' porque los asignamos en views.py
        fields = [
            'titulo', 
            'descripcion', 
            'ubicacion', 
            'prioridad', 
            'nombre_vecino', 
            'telefono_vecino', 
            'correo_vecino',
        ]

        labels = {
            'titulo': 'Título de la Incidencia / Asunto',
            'descripcion': 'Descripción del Incidente (Detalle de campo)',
            'ubicacion': 'Ubicación Exacta',
            'prioridad': 'Prioridad de Atención (Alta, Media, Baja)',
            'nombre_vecino': 'Nombre del Vecino',
            'telefono_vecino': 'Teléfono del Vecino',
            'correo_vecino': 'Correo Electrónico del Vecino',
        }

class ResolucionForm(forms.ModelForm):
    class Meta:
        model = Resolucion
        
        fields = ['descripcion','cuadrilla']
        
        labels = {
            'descripcion': 'Explicación de la Solución',
            'cuadrilla': 'Cuadrilla Resolutora',
        }