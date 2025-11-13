
from django import forms
from .models import Solicitud, Encuesta, Resolucion, Multimedia 

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['cuadrilla', 'observaciones', 'tipo_incidencia']

        labels = {
            'cuadrilla': 'Cuadrilla (Asignación inicial)',
            'observaciones': 'Notas Internas / Administrativas',
            'tipo_incidencia': 'Tipo de Incidencia',
        }

class EncuestaForm(forms.ModelForm):
    archivo_adjunto = forms.FileField(
        label='Adjuntar Evidencia (Foto/Video)', 
        required=False
    )

    class Meta:
        model = Encuesta
        fields = [
            'titulo', 
            'descripcion', 
            'ubicacion', 
            'prioridad', 
            'nombre_vecino', 
            'telefono_vecino', 
            'correo_vecino',
        ]
class ResolucionForm(forms.ModelForm):
    class Meta:
        model = Resolucion
        
        fields = ['descripcion','cuadrilla']
        
        labels = {
            'descripcion': 'Explicación de la Solución',
            'cuadrilla': 'Cuadrilla Resolutora',
        }

class SolicitudDerivarForm(forms.ModelForm):
    """
    Formulario minimalista para derivar una solicitud,
    solo pidiendo la Cuadrilla y observaciones opcionales.
    """
    class Meta:
        model = Solicitud
        # Solo necesitamos estos campos para la derivación
        fields = ['cuadrilla', 'observaciones'] 
        labels = {
            'cuadrilla': 'Asignar a Cuadrilla 👷',
            'observaciones': 'Notas Administrativas (Opcional)',
        }