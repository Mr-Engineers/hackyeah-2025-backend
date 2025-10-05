from supabase import create_client, Client
import random
from ..events.models import Event
from ..player_state.models import PlayerState
from ..events.special_functions import to_str_list, to_num_list

url = "https://xhduiiqjmhvhzcqkvkya.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhoZHVpaXFqbWh2aHpjcWt2a3lhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1MDUzNjAsImV4cCI6MjA3NTA4MTM2MH0.ZW_o23yyWhXiJGJEWLtULz-tVROKzRVnWYRoVXNmulk"

supabase: Client = create_client(url, key)

def get_all_events():
    supa_response = supabase.table("Events").select("*").execute()
    events_list = list()

    for row in supa_response.data:
        temp = Event(
            title = row['title'],
            description = row['description'],
            category = row['category'],

            required_attributes = to_str_list(row['required_attributes']),
            required_attribute_values = to_num_list(row['required_attribute_values']),

            advantaged_attributes = to_str_list(row['required_attributes']),
            advantaged_attribute_values = to_num_list(row['advantaged_attribute_values']),

            disadvantaged_attributes = to_str_list(row['required_attributes']),
            disadvantaged_attribute_values = to_num_list(row['disadvantaged_attribute_values']),

            job_name = row['job_name'],
            job_id = row['job_id'],
            available = True
        )

        events_list.append(temp)

    return events_list


def verify_requirements(player_state: PlayerState, requirements_dict: dict):
    for key, required_value in requirements_dict.items():
        current_value = getattr(player_state, key) 
        if not current_value >=  required_value:
            return False
        
    return True


def verify_if_event_is_available(player_state: PlayerState, event_list: list):
    for event in event_list:
        if not verify_requirements(player_state, event.get_required_attributes_dict()):
            event = False


def select_suitable_events(player_state: PlayerState):
    # initial events
    events_list = get_all_events()
    suitable_events = []
    if player_state.age == 20:
        suitable_events = [event for event in events_list if event.get_required_attributes_dict().get('age') == 20.0]
    elif player_state.age == 22:
        suitable_events = [event for event in events_list if event.get_required_attributes_dict().get('age') == 22.0]
        verify_if_event_is_available(player_state, suitable_events)
    else:
        suitable_events = [
            event for event in events_list
            if not event.get_required_attributes_dict().get('age') == 20.0
        ]
        
    print(suitable_events.__len__())
    return suitable_events

select_suitable_events(PlayerState(age=25))
