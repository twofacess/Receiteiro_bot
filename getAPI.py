import json
import requests

qtd = 0
receita = {}
lista = {}
inicio10 = 27
inicio5 = 26


def getTagAPI(api, cod): #Faz toda a manipulação da string baixada da API
        tam = 0
        ult=0

        fim=api.find(':')

        tag=api[tam+1:fim-1]
        tag=tag.replace('"',"")
        tam=fim
        

        #Se cod=1 significa que 'publisher_url' é o ultimo item e deve buscar por ','
        if tag == 'publisher_url' and cod == 1:
                fim=api.find(',')
                chave=api[tam+2:fim-1]
                chave=chave.replace('"',"")
                fim=fim=-3
                ult=1
        else:
                if tag == 'ingredients':
                        fim=api.find(']')
                        chave=api[tam+3:fim-3]
                        chave=chave.replace('"',"")
                else:
                        #Se cod=2 significa que 'title' é o ultimo item e deve buscar por '}'
                        if tag == 'title' and cod == 2:
                                fim=api.find('}')
                                chave=api[tam+2:fim-1]
                                chave=chave.replace('"',"")

                        else:
                                fim=api.find(',')
                                chave=api[tam+2:fim]
                                chave=chave.replace('"',"")
        
        if fim==-1:
                fim=-3
                ult=1
                chave=api[tam+2:fim]
                chave=chave.replace('"',"")

        if fim!=-3:
                api=api[fim+2:]

                tam=0
                fim=0

        return [tag, chave, api, ult]


def getRecipe(item): #Chama a API para buscar a receita solicitada
        global receita

        response = requests.get('http://food2fork.com/api/get?key=4fe184badd0c478ebe05f532ba06fb8b&rId='+item)
        text=response.content
        textAPI=text.decode('utf-8')

        #Remove informações desnecessarias da string da API
        textAPI=(textAPI[12:])

        while True:
                temp=getTagAPI(textAPI,2)

                #Adiciona ao dicionario receita chave a tag com o nome do campo e o valor do campo
                receita[temp[0]]=temp[1]
                #Remove a Receita adicionada da string da API
                textAPI=temp[2]

                if temp[3]==1:
                        break

        return receita

def getListOfRecipes(item, cont): #Chama a API para buscar as receitas com o ingrediente pedido
        global lista
        global inicio5, inicio10, qtd
        if cont == 0:
                inicio10 = 27
                inicio5 = 26

        response = requests.get('http://food2fork.com/api/search?key=4fe184badd0c478ebe05f532ba06fb8b&q='+item)          
        text=response.content
        textAPI=text.decode('utf-8')

        qtd = int(textAPI[textAPI.find(':')+2:textAPI.find(',')])

        if qtd == 0:
                return qtd
        elif qtd < 10 :
                textAPI=(textAPI[inicio5:])
                #Seta o valor do inicio da receita proxima receita
                fim=textAPI.find('{')
                inicio5 = inicio5 + fim + 1
        else:
                textAPI=(textAPI[inicio10:])
                #Seta o valor do inicio da receita proxima receita
                fim=textAPI.find('{')
                inicio10 = inicio10 + fim + 1
                

        
        while True:
                temp=getTagAPI(textAPI,1)

                #Adiciona ao dicionario receita chave a tag com o nome do campo e o valor do campo
                lista[temp[0]]=temp[1]
                #Remove a Receita adicionada da string da API
                textAPI=temp[2]

                if temp[3]==1:
                        break

        lista['qtd']=qtd
        return lista



#procura receita http://food2fork.com/api/search?key=4fe184badd0c478ebe05f532ba06fb8b&q=shredded%20chicken
#pega receita http://food2fork.com/api/get?key=4fe184badd0c478ebe05f532ba06fb8b&rId=35171
#099563badfe8295493e35cf65e82dbbd



