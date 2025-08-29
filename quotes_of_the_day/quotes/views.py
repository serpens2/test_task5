from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from . import models, forms
from numpy.random import choice, randint

def get_quote(request):
    # считаем кол-во цитат с весом 1, кол-во цитат с весом 2 и с весом 3
    counts = {i: 0 for i in range(1,4)}
    for type_ in counts:
        counts[type_] = models.Quote.objects.filter(weight=type_).count()
    # умножаем на два кол-во цитат с "большим" весом 3
    # и делим на два кол-во цитат с "маленьким" весом 1
    counts[1] /= 2
    counts[3] *= 2
    total_count = sum(counts.values())
    if total_count > 0:
        for type_ in counts:
            # делим на общее кол-во цитат, получая
            # три вероятности: вероятность выбрать группу
            # цитат с весом 1, группу с весом 2 и с весом 3
            counts[type_] /= total_count
        probs = [ val for val in counts.values() ]
        # выбираем одну из трёх групп по рассчитанным вероятностям с помощью numpy-функции
        chosen_type = choice([1,2,3], p = probs)
        # находим в базе данных все цитаты с выбранным типом веса
        query = models.Quote.objects.filter(weight=chosen_type)
        # выбираем наугад цитату
        q = query[randint(0,query.count())]
        q.views += 1
        q.save(update_fields=['views'])
    else:
        q = None
    context = {'q': q}
    return render(request,'quotes/quote.html',context)

@require_POST
def react_to_quote(request, quote_id):
    # reaction - реакция, которую пользователь поставил *сейчас*
    # status - реакция, которую пользователь поставил *раньше*
    # например, если reaction = 'like' = status, то пользователь отменил свой лайк
    reaction = request.headers.get("reaction")
    status = request.headers.get("status")
    q = models.Quote.objects.get(id=quote_id)
    if status == "neutral":
        if reaction == "like":
            q.likes += 1
        elif reaction == "dislike":
            q.dislikes += 1
    else:
        if status == reaction:
            if reaction == "like":
                q.likes -= 1
            elif reaction == "dislike":
                q.dislikes -= 1
        else:
            if reaction == "like":
                q.likes += 1
                q.dislikes -= 1
            elif reaction == "dislike":
                q.dislikes += 1
                q.likes -= 1
    q.save(update_fields=["likes","dislikes"])
    return HttpResponse(status=200)

def get_top_quotes(request):
    if models.Quote.objects.count() > 0:
        top_quotes = models.Quote.objects.order_by("-likes")[:10]
        for q in top_quotes:
            q.views += 1
            q.save(update_fields=['views'])
    else:
        top_quotes = None
    context = {'top_quotes': top_quotes}
    return render(request, 'quotes/top_quotes.html', context)

def add_quote(request):
    if request.method == "POST":
        form = forms.QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_quote")
    else:
        form = forms.QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})