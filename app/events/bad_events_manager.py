from supabase import create_client, Client
import random
from ..events.models import BadEvent
from ..player_state.models import PlayerState
from ..events.special_functions import to_str_list, to_num_list, should_trigger

url = "https://xhduiiqjmhvhzcqkvkya.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhoZHVpaXFqbWh2aHpjcWt2a3lhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1MDUzNjAsImV4cCI6MjA3NTA4MTM2MH0.ZW_o23yyWhXiJGJEWLtULz-tVROKzRVnWYRoVXNmulk"

supabase: Client = create_client(url, key)


def get_all_bad_events():
    supa_response = supabase.table("RandomBadEvent").select("*").execute()
    bad_events_list = list()

    for row in supa_response.data:
        temp = BadEvent(
            title = row['title'],
            description = row['description'],
            category = row['category'],
            decisive_atribute = row['decisive_attribute'],
            threshold = row['threshold'],
            decreased_attribute = to_str_list(row.get('decreased_attribute')),
            decrease_value = to_num_list(row.get('decrease_value'))
        )
        bad_events_list.append(temp)

    return bad_events_list


def select_suitable_bad_events(player_state: PlayerState):
    bad_events_list = get_all_bad_events()
    suitable_bad_events = list()
    
    for event in bad_events_list:
        player_value= getattr(player_state, event.decisive_atribute)
        threshold = event.threshold

        # if player_value <= threshold:
        #     suitable_bad_events.append(event)
        suitable_bad_events.append(event)

    return suitable_bad_events


def draw_random_bad_event(player_state: PlayerState):
    bad_events_list = select_suitable_bad_events(player_state)
    print(bad_events_list)
    random.shuffle(bad_events_list)

    for event in bad_events_list:
        player_value = getattr(player_state, event.decisive_atribute)
        threshold_value = event.threshold
        if(should_trigger(player_value, threshold_value)):
            return event

    return None