from supabase import create_client, Client
from ..events.models import BadEvent
from ..player_state.models import PlayerState

import math
import random

url = "https://xhduiiqjmhvhzcqkvkya.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhoZHVpaXFqbWh2aHpjcWt2a3lhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1MDUzNjAsImV4cCI6MjA3NTA4MTM2MH0.ZW_o23yyWhXiJGJEWLtULz-tVROKzRVnWYRoVXNmulk"

supabase: Client = create_client(url, key)


def create_threshold_player() -> PlayerState:
    return PlayerState(
        age=0,
        health=30,
        education=0,
        career_level=0,
        income=0,
        savings=0.0,
        happiness=30,
        social_relations=30,
        zus_balance=0.0,
        spendings=0.0
    )


def get_all_bad_events():
    supa_response = supabase.table("RandomBadEvent").select("*").execute()
    bad_events_list = list()

    for row in supa_response.data:
        temp = BadEvent()
        temp.title = row['title']
        temp.description = row['description']
        temp.image = row['image']
        temp.decisive_atribute = row['decisive_attribute']
        temp.decreased_attribute = row['decreased_attribute']
        temp.decrease_value = row['decrease_value']
        bad_events_list.append(temp)

    return bad_events_list


def select_suitable_events(player_state: PlayerState, bad_events_list: list):
    suitable_bad_events = list()
    threshold_player = create_threshold_player()
    
    for event in bad_events_list:
        player_value= getattr(player_state, event.decisive_atribute)
        threshold = getattr(threshold_player, event.decisive_atribute)

        if player_value <= threshold:
            suitable_bad_events.append(event)

    return suitable_bad_events


def should_trigger(x: float, max_x: float) -> bool:
    """
    Zwraca True z prawdopodobieństwem zgodnym z rozkładem normalnym,
    gdzie x=0 -> 100%, a x=max_x -> 0%.
    """
    # Ustal środek i odchylenie standardowe proporcjonalnie do max_x
    mean = max_x / 2
    std_dev = max_x / 4  # reguluj stromość (1/4 dobrze działa w zakresie 0–30)
    
    # Dystrybuanta rozkładu normalnego (CDF)
    cdf = 0.5 * (1 + math.erf((x - mean) / (std_dev * math.sqrt(2))))
    
    # Odwrócenie (x=0 → 1, x=max_x → 0)
    probability_true = 1 - cdf

    # Ograniczenie do przedziału [0, 1]
    probability_true = max(0.0, min(1.0, probability_true))

    # Losowanie wyniku
    return random.random() < probability_true


def draw_random_bad_event(player_state: PlayerState, bad_events_list: list):
    threshold_player = create_threshold_player()

    for event in bad_events_list:
        player_value = getattr(player_state, event.decisive_atribute)
        threshold_value = getattr(threshold_player, event.decisive_atribute)
        if(should_trigger(player_value, threshold_value)):
            return event
        
    return None
