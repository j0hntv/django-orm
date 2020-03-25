import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.http import request

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.all()

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity.pokemon.title,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.filter(id=pokemon_id).first()
    if not pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    previous_evolution = pokemon.previous_evolution and {
        'title_ru': pokemon.previous_evolution.title,
        'pokemon_id': pokemon.previous_evolution.id,
        'img_url': pokemon.previous_evolution.image.url
    }
    
    try:
        pokemon_next_evolutions = pokemon.next_evolutions.get()
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        pokemon_next_evolutions = None

    next_evolution = pokemon_next_evolutions and {
        'title_ru': pokemon_next_evolutions.title,
        'pokemon_id': pokemon_next_evolutions.id,
        'img_url': pokemon_next_evolutions.image.url
    }

    pokemon_features = {
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
            'description': pokemon.description,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'previous_evolution': previous_evolution,
            'next_evolution': next_evolution
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    
    pokemon_entities = pokemon.pokemon_entities.all()

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity.pokemon.title,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_features})
