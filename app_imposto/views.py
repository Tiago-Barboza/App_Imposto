from django.shortcuts import render
from django.utils.safestring import mark_safe
from project_imposto.settings import prodList, impostometroMunicipiosEstados,MunicipioFrame, impostometroFrame, token


class Produto:
    def __init__(self):
        self.nome = ""
        self.tributacao = 0

class EstadoMunicipios:
    def __init__(self):
        self.Estado = ""
        self.Municipios = ""


def tributacao(request):
    global token
    ProdList = prodList;
    if request.POST:
        produto = Produto()
        produto.nome = request.POST.get('nomeProd')
        if len(produto.nome) > 0 and token != request.POST.get('csrfmiddlewaretoken'):
            for prod in prodList:
                if prod.nome.lower() == produto.nome.lower():
                    produto.tributacao = prod.tributacao
                    break

            prodDict = {'result': mark_safe(f'{produto.nome} possui uma tributação de <span style="color: red; font-weight: bold;">{produto.tributacao}</span>'), 'prodList': ProdList, 'prodEscolhido': ''}
            token = request.POST.get('csrfmiddlewaretoken')
            return render(request, 'tributacao/encontrarImposto.html', prodDict)
        else:
            return render(request, 'tributacao/encontrarImposto.html', {'prodList': ProdList, 'result':'', 'prodEscolhido': ''})
    else:
        return render(request, 'tributacao/encontrarImposto.html', {'prodList': ProdList, 'result':'',  'prodEscolhido': ''})


def maioresImpostos(request):
    sortedList = sorted(prodList, key=lambda x: x.tributacao, reverse=True)
    dale = sortedList[:15]
    return render(request, 'tributacao/maioresImpostos.html', {'sortedList': dale})

def impostometro(request):
    global token
    print(request.POST)
    if request.POST:
        if request.POST.get('csrfmiddlewaretoken') != token:
            if 'btnPesquisar' in request.POST:
                estado = request.POST.get('selectEstado')
                if len(estado) > 0:
                    estado = estado.lower()
                    municipio = request.POST.get('selectMunicipio')
                    if municipio != None and len(municipio) > 0 and municipio != '0':
                        municipioFrame = MunicipioFrame.replace('contador/',f'contador/{estado}').replace('municipio=',f'municipio={municipio}')
                        token = request.POST.get('csrfmiddlewaretoken')
                        return render(request, 'impostometro/impostometro.html', {'frameArrecadado': mark_safe(municipioFrame)})
                    else:
                        if estado == 'br':
                            frame = impostometroFrame
                        elif estado == '':
                            frame = ''
                        else:
                            frame = impostometroFrame.replace('contador/', f'contador/{estado}')
                        token = request.POST.get('csrfmiddlewaretoken')
                        return render(request, 'impostometro/impostometro.html', {'frameArrecadado': mark_safe(frame)})
                return render(request, 'impostometro/impostometro.html', {'frameArrecadado': ''})
            elif 'selectEstado' in request.POST:
                estado = request.POST.get('selectEstado')
                estadoMunicipios = EstadoMunicipios()
                estadoMunicipios.Estado = estado
                for obj in impostometroMunicipiosEstados:
                    if obj["Estado"] == estadoMunicipios.Estado:
                        estadoMunicipios.Municipios = obj["Municipios"]
                        token = request.POST.get('csrfmiddlewaretoken')
                        return render(request, 'impostometro/impostometro.html', {'selectMunicipios':mark_safe(estadoMunicipios.Municipios), "select_value": estado})
                token = request.POST.get('csrfmiddlewaretoken')
                return render(request, 'impostometro/impostometro.html', {'select_value': estado})
        else:
            return render(request, 'impostometro/impostometro.html', {'selectMunicipios':'', 'frameArrecadado':'', 'select_value':''})
    return render(request, 'impostometro/impostometro.html', {'selectMunicipios':'', 'frameArrecadado':'', 'select_value':''})
