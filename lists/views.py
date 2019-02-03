from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from lists.forms import ItemForm
from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

# test function to check endpoint

# def test_view(request):
#     return HttpResponse("OK")

def new_list(request):
  form = ItemForm(data=request.POST)
  if form.is_valid():
    list_ = List.objects.create()
    form.save(for_list=list_)
    return redirect(list_)
  else:
    return render(request, 'home.html', {"form": form})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
      form = ItemForm(data=request.POST)
      if form.is_valid():
        form.save(for_list=list_)
        return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})
