import redis
import os
from app.player_state.models import PlayerState

class PlayerStateService:
    def __init__(self, redis_host=None, redis_port=None, db=0):
        # Use environment variables for Heroku, fallback to defaults for local development
        redis_host = redis_host or os.getenv("REDISGREEN_URL", "redis://redis:6379")
        redis_port = redis_port or 6379
        
        # Try to connect to Redis, fallback to in-memory storage if it fails
        try:
            if redis_host.startswith("redis://"):
                self.redis = redis.from_url(redis_host, decode_responses=True)
            else:
                self.redis = redis.Redis(host=redis_host, port=redis_port, db=db, decode_responses=True)
            # Test the connection
            self.redis.ping()
            self.use_redis = True
        except Exception as e:
            print(f"Redis connection failed: {e}. Using in-memory storage.")
            self.redis = None
            self.use_redis = False
            self._memory_storage = {}
        
        self.REDIS_KEY = "player_state"

    def save_state(self, state: PlayerState):
        if self.use_redis:
            self.redis.set(self.REDIS_KEY, state.json())
        else:
            self._memory_storage[self.REDIS_KEY] = state.json()

    def load_state(self) -> PlayerState:
        if self.use_redis:
            data = self.redis.get(self.REDIS_KEY)
        else:
            data = self._memory_storage.get(self.REDIS_KEY)
            
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
