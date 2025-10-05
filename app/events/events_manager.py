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
            chance_increaser = row['chance_increaser']
        )

        events_list.append(temp)
        print(temp)

    return events_list


def select_suitable_events(player_state: PlayerState, events_list: list):
    # initial events
    suitable_events = list()
    if player_state.age == 20:
        first_events = [event for event in events_list if (event.required_attributes == "Studenckie życie na krawędzi budżetu" or event.title == "Weź ster w swoje ręce")]
        suitable_events.append(first_events)

    return suitable_events

select_suitable_events(PlayerState(), get_all_events())