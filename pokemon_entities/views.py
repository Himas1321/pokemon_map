import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_from_db = Pokemon.objects.all()
    now = localtime()

    pokemon_entity = PokemonEntity.objects.filter(
        appeared_at__lte=now, 
        disappeared_at__gte=now,
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon_entity:
        lat = entity.lat
        lon = entity.lon
        pokemon = entity.pokemon

        if pokemon.photo:
            img_url = request.build_absolute_uri(pokemon.photo.url)
        else:
            img_url = DEFAULT_IMAGE_URL

        add_pokemon(folium_map, lat, lon, img_url)


    pokemons_on_page = []
    for pokemon in pokemons_from_db:

        if pokemon.photo:
            img_url = request.build_absolute_uri(pokemon.photo.url)
        else:
            img_url = DEFAULT_IMAGE_URL

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    
    active_entities = PokemonEntity.objects.filter(pokemon=pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in active_entities:

        if entity.pokemon.photo:
            img_url = request.build_absolute_uri(pokemon.photo.url)
        else:
            img_url = DEFAULT_IMAGE_URL
        add_pokemon(folium_map, entity.lat, entity.lon, img_url)

    
    if pokemon.previous_evolution is not None:
        predok = pokemon.previous_evolution 
        previous_evolution = {
            "title_ru": predok.title,
            "pokemon_id": predok.id,
            "img_url": request.build_absolute_uri(predok.photo.url) if predok.photo else DEFAULT_IMAGE_URL,
        }
    else:
        previous_evolution = None

    pokemon.next_evolution.all()
    descendant = pokemon.next_evolution.first()
    next_evolution = None
    if descendant:
            next_evolution = {
            "title_ru": descendant.title,
            "pokemon_id": descendant.id,
            "img_url": request.build_absolute_uri(descendant.photo.url) if descendant.photo else DEFAULT_IMAGE_URL,
        }
    else:
        descendant = None

    pokemon_info = {
        'img_url': request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else DEFAULT_IMAGE_URL,
        'title_ru': pokemon.title,
        'title_jp': pokemon.title_jp,
        'title_en': pokemon.title_en,
        'description': pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution,
    }


    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_info
    
    })
