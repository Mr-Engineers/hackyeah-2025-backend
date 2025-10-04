from supabase import create_client, Client
from ..events.models import BadEvent
from ..player_state.models import PlayerState
from ..events.special_functions import to_str_list, to_num_list, should_trigger

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
        temp.decreased_attribute = to_str_list(row.get('decreased_attribute'))
        temp.decrease_value = to_num_list(row.get('decrease_value'))
        bad_events_list.append(temp)
        print(temp)

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


def draw_random_bad_event(player_state: PlayerState, bad_events_list: list):
    threshold_player = create_threshold_player()

    for event in bad_events_list:
        player_value = getattr(player_state, event.decisive_atribute)
        threshold_value = getattr(threshold_player, event.decisive_atribute)
        if(should_trigger(player_value, threshold_value)):
            return event
        
    return None

get_all_bad_events()