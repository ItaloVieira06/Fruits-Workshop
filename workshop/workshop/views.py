from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponse
from .models import Fruits, Sell
# Create your views here.

#página de login
def login1 (request):
    if request.method == 'POST':
      form = AuthenticationForm(request, data = request.POST)
      if form.is_valid():
        user = form.get_user()
        login(request, user)
        if user.is_superuser:
          return redirect('admin:index')
        else:
          return redirect('salesman')
      else:
        error = form.errors
        print(error)
    else:
      form = AuthenticationForm()
      error = None
    return render(request, "login.html", {'form':form, 'error': error})

#página do vendedor
def salesman(request):
 fruits = Fruits.objects.all()
 return render(request, "salesman.html", {"fruits":fruits})
# return HttpResponse("Hello World")

#página de venda
def sales(request):
 fruits = Fruits.objects.all() 
 return render(request, "sales.html", {"fruits":fruits})

#página de relatório
def report(request):
  report = Sell.objects.filter(salesman = request.user)
  return render(request, "report.html", {"sell":report})

#função de get e tratamento de dados
def send(request):
  #setar variável de erro
  warning = None

  #pegar pelo POST
  if (request.method == "POST"):
   
   #get de valores
   name_fruit = request.POST.getlist("frutas[]")
   quant_fruit = request.POST.getlist("quantity[]")
   date = request.POST.get("date")
   discount = request.POST.get("discount")
   
   price = 0

   #checagem de valor vazio
   name_fruit = [name for name in name_fruit if name.strip()]
   quant_fruit = [qty for qty in quant_fruit if qty.strip()]

   #For para percorrer os objetos e após isso registrar os que passarem
   for index, name in enumerate(name_fruit):

    #obter informações da fruta pelo nome da fruta
    fruit = get_object_or_404(Fruits, name=name)

    if (fruit.quant < int(quant_fruit[index])):

      #retorno e warning se der algum erro
      warning = f'Não há estoque suficiente. O estoque atual é: {fruit.quant}'


      return render(request, "salesman.html", {"error": warning})
    
    else:

      #atualização de produtos no bd
      fruit.quant = fruit.quant-int(quant_fruit[index])
      fruit.save()
      
      if (discount != 0):
       price = fruit.value*int(quant_fruit[index])
       value_discount = (int(discount)*price)/100
       price = price - value_discount

      report = Sell(
        salesman = str(request.user),
        products = name,
        hour = date,
        value = price
      )
       
      price+=fruit.value 
      report.save()

   
   print(price)
   value_discount = (int(discount)*price)/100
   price = price - value_discount
   

  #retorno para a página anterior
  return render(request, "salesman.html", {"error": warning})

def search(request):
  if (request.method == "POST"):
   type_search = request.POST.get("fruit_type")
   object_search = request.POST.get("txt_fruit")

   warning = None

   if type_search == "name":
    searcher = Fruits.objects.filter(name = object_search)
    
   if type_search == "clas":
    #buscar pela classificação
    try:
     searcher = Fruits.objects.filter(clas = object_search)
    except ValueError:
      warning = 'Valor de classe de fruta inválido, digite: Extra, Primeira, Segunda, Terceira'
      return render(request, "salesman.html", {"error":warning})

   if type_search == "fresh":
    #indentificar o valor
    if object_search == "sim" or "Sim":
     searcher = Fruits.objects.filter(fresh = True)

    elif object_search == "não" or "Não":
     searcher = Fruits.objects.filter(fresh = False)

    else:
      warning = 'Valor inserido inválido'
      return render(request, "salesman.html", {"error":warning})
   
   if type_search == "quant":
    #transformar em inteiro
    searcher = Fruits.objects.filter(quant = int(object_search))

   if type_search == "value":
    #tranformar em float
    searcher = Fruits.objects.filter(value = float(object_search))

   #retornar página atualizada
   return render(request, "salesman.html", {"fruits":searcher})