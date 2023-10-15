from django.shortcuts import render
from django.utils.safestring import mark_safe
from project_imposto.settings import *


class Produto:
    def __init__(self):
        self.nome = ""
        self.tributacao = 0

class EstadoMunicipios:
    def __init__(self):
        self.Estado = ""
        self.Municipios = ""


def tributacao(request):
    if request.POST:
        produto = Produto()
        produto.nome = request.POST.get('nomeProd')
        if len(produto.nome) > 0:
            for prod in prodList:
                if (prod.nome == produto.nome):
                    produto.tributacao = prod.tributacao
                    break

            prodDict = {'result': f'{produto.nome} possui uma tributação de {produto.tributacao}', 'produtosLista': prodList}
            return render(request, 'tributacao/encontrarImposto.html', prodDict)
        else:
            return render(request, 'tributacao/encontrarImposto.html', {'prodList': prodList})
    else:
        return render(request, 'tributacao/encontrarImposto.html', {'prodList': prodList})


def maioresImpostos(request):
    sortedList = sorted(prodList, key=lambda x: x.tributacao, reverse=True)
    dale = sortedList[:15]
    return render(request, 'tributacao/maioresImpostos.html', {'sortedList': dale})

def impostometro(request):
    if request.POST:
        if 'btnPesquisar' in request.POST:
            estado = request.POST.get('selectEstado')
            if len(estado) > 0:
                estado = estado.lower()
                municipio = request.POST.get('selectMunicipio')
                if municipio != None and len(municipio) > 0 and municipio != '0':
                    municipioFrame = MunicipioFrame.replace('contador/',f'contador/{estado}').replace('municipio=',f'municipio={municipio}')
                    return render(request, 'impostometro/impostometro.html', {'frameArrecadado': mark_safe(municipioFrame)})
                else:
                    if estado == 'br':
                        frame = impostometroFrame
                    elif estado == '':
                        frame = ''
                    else:
                        frame = impostometroFrame.replace('contador/', f'contador/{estado}')
                    return render(request, 'impostometro/impostometro.html', {'frameArrecadado': mark_safe(frame)})
            return render(request, 'impostometro/impostometro.html', {'frameArrecadado': ''})
        elif 'selectEstado' in request.POST:
            estado = request.POST.get('selectEstado')
            estadoMunicipios = EstadoMunicipios()
            estadoMunicipios.Estado = estado
            for obj in impostometroMunicipiosEstados:
                if obj["Estado"] == estadoMunicipios.Estado:
                    estadoMunicipios.Municipios = obj["Municipios"]
                    return render(request, 'impostometro/impostometro.html', {'selectMunicipios':mark_safe(estadoMunicipios.Municipios), "select_value": estado})
            return render(request, 'impostometro/impostometro.html', {'select_value': estado})

    return render(request, 'impostometro/impostometro.html', {'selectMunicipios':'', 'frameArrecadado':'', 'select_value':''})
