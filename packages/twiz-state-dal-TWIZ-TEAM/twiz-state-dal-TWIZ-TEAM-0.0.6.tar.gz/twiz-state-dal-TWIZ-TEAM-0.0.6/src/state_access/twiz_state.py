from typing import Union

from twiz_cobot.custom_libraries.twiz_state_dal.src.state_access.turn_state import TurnState, StateType
from twiz_cobot.custom_libraries.twiz_state_dal.src.state_access.twiz_state_manager import TwizStateManager
from .user_state import UserState


class TwizState:

    _user: UserState
    _prev: TurnState
    _curr: TurnState
    _session_history: Union[list, list]

    def __init__(self, user_id: str, user_table_name: str = 'UserTable', state_table_name: str = 'StateTable'):
        state_manager = TwizStateManager(user_id, user_table_name, state_table_name)
        self._user = UserState(state_manager)
        self._prev = TurnState(state_manager, StateType.PREV)
        self._curr = TurnState(state_manager)  # Default is current_state
        #self._session_history = state_manager.session_history

    @property
    def user(self):
        return self._user

    @property
    def prev(self):
        return self._prev

    @property
    def curr(self):
        return self._curr

    @property
    def session_history(self):
        return self._session_history
