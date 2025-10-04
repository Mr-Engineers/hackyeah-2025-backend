from ..player_state.router import service as player_state_service

class FinanceService:
    def invest(self, amount: float):
        player_state = player_state_service.load_state()
        if player_state.cash < amount:
            raise ValueError("not enough money")
        player_state.savings -= amount
        player_state.investments += amount
        player_state_service.save_state(player_state)
        return player_state
    
    def withdraw(self, amount: float):
        player_state = player_state_service.load_state()
        if player_state.investments < amount:
            raise ValueError("not enough money")
        
        player_state.investments -= amount
        player_state.savings += amount
        player_state_service.save_state(player_state)
        return player_state
    