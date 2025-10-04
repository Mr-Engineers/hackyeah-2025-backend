import redis
from app.player_state.models import PlayerState

class PlayerStateService:
    def __init__(self, redis_host="redis", redis_port=6379, db=0):
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=db, decode_responses=True)
        self.REDIS_KEY = "player_state"

    def save_state(self, state: PlayerState):
        self.redis.set(self.REDIS_KEY, state.json())

    def load_state(self) -> PlayerState:
        data = self.redis.get(self.REDIS_KEY)
        if data:
            return PlayerState.parse_raw(data)
        default_state = PlayerState()
        self.save_state(default_state)
        return default_state

    def reset_state(self) -> PlayerState:
        state = PlayerState()
        self.save_state(state)
        return state

    def update_state(self, updated_state: PlayerState) -> PlayerState:
        self.save_state(updated_state)
        return updated_state
