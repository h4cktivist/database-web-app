from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Movies
from .forms import MoviesForm


def movies(request):
    sort_by = request.GET.get('sort_by', 'movie_id')
    sort_order = request.GET.get('sort_order', 'asc')
    page_number = request.GET.get('page', 1)

    columns = [
        {'field': 'movie_id', 'label': 'ID'},
        {'field': 'title', 'label': 'Название'},
        {'field': 'genre', 'label': 'Жанр'},
        {'field': 'duration', 'label': 'Длительность'},
        {'field': 'age_restriction', 'label': 'Ограничение'},
        {'field': 'rating', 'label': 'Рейтинг'},
    ]
    for col in columns:
        if col['field'] == sort_by:
            col['sort_order'] = 'desc' if sort_order == 'asc' else 'asc'
        else:
            col['sort_order'] = 'asc'

    movie_list = Movies.objects.all().order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")
    paginator = Paginator(movie_list, 25)
    try:
        movies = paginator.page(page_number)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    context = {
        'movies': movies,
        'columns': columns,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'page_number': page_number,
    }
    return render(request, 'movies/movies.html', context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movies, movie_id=movie_id)
    return render(request, 'movies/movie_detail.html', {'movie': movie})


def add_movie(request):
    if request.method == 'POST':
        form = MoviesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies')
    else:
        form = MoviesForm()
    return render(request, 'add.html', {'form': form})


def edit_movie(request, movie_id):
    movie = get_object_or_404(Movies, movie_id=movie_id)
    if request.method == 'POST':
        form = MoviesForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies')
    else:
        form = MoviesForm(instance=movie)
    return render(request, 'edit.html', {'form': form, 'movie': movie})


def delete_movie(request, movie_id):
    movie = get_object_or_404(Movies, movie_id=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('movies')
    return render(request, 'delete.html', {'redirect_url': reverse('movies')})
