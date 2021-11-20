from django.http import HttpResponse
from django.template import Template, Context

MARCAS = ['Kia','Mazda','BMW']
MODELO = []
CARROCERIA = []
COMBUSTIBLE = []
COLOR = ['Rojo','Azul','Verde']

#Vistas
def form(request):
    doc_file = open('C:/Users/ariza/Documents/GitHub/Cars_Deployment/carwebiste/carwebiste/templates/form.html') # Relative path plz
    plt = Template(doc_file.read())
    doc_file.close()

    ctx=Context({"marcas":MARCAS, "modelos":MODELO, "carrocerias":CARROCERIA, "combustibles":COMBUSTIBLE, "colores":COLOR})
    doc=plt.render(ctx)

    return HttpResponse(doc)