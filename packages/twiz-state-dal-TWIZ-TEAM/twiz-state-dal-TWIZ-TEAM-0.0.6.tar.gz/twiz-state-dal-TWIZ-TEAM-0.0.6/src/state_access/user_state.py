from typing import List
from twiz_cobot.custom_libraries.twiz_state_dal.src.state_access.twiz_state_manager import TwizStateManager


class UserState:
    state_manager: TwizStateManager

    def __init__(self, state_manager: TwizStateManager):
        self.state_manager = state_manager

    @property
    def started_task(self) -> bool:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('started_task', None)

    def set_started_task(self, started_task: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['started_task'] = started_task
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def current_task(self) -> str:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('current_task', None)

    def set_current_task(self, current_task: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['current_task'] = current_task
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def current_query_result_index(self) -> int:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('current_query_result_index', None)

    def set_current_query_result_index(self, current_query_result_index: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['current_query_result_index'] = current_query_result_index
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def apl_screens(self) -> List:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('apl_screens', None)

    def set_apl_screens(self, apl_screens: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['apl_screens'] = apl_screens
        return self.state_manager.write_user_attributes(_user_attributes)

    ####
    @property
    def show_ingredients(self) -> bool:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('show_ingredients', False)

    def set_show_ingredients(self, show_ingredients: bool = False):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['show_ingredients'] = show_ingredients
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def wikihow_search_query(self) -> str:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('wikihow_search_query', None)

    def set_wikihow_search_query(self, wikihow_search_query: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['wikihow_search_query'] = wikihow_search_query
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def recipe_search_query(self) -> str:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('recipe_search_query', None)

    def set_recipe_search_query(self, recipe_search_query: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['recipe_search_query'] = recipe_search_query
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def data_source(self) -> str:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('recipe_search_query', None)

    def set_data_source(self, data_source: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['data_source'] = data_source
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def avoid_restrictions(self) -> List:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('avoid_restrictions', None)

    def set_avoid_restrictions(self, avoid_restrictions: List = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['avoid_restrictions'] = avoid_restrictions
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def enforce_restrictions(self) -> List:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('enforce_restrictions', None)

    def set_enforce_restrictions(self, enforce_restrictions: List = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['enforce_restrictions'] = enforce_restrictions
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def current_task_result(self) -> map:  # current task document (json map)
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('current_task_result', None)

    def set_current_task_result(self, current_task_result: map = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['current_task_result'] = current_task_result
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def task_history(self) -> List:  # List of lists with [task_id, data_source]
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('task_history', None)

    def set_task_history(self, task_history: List = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['task_history'] = task_history
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def has_sent_card(self) -> bool:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('has_sent_card', None)

    def set_has_sent_card(self, has_sent_card: bool = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['has_sent_card'] = has_sent_card
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def query_result(self) -> List:  # List of task Maps
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('query_result', None)

    def set_query_result(self, query_result: List = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['query_result'] = query_result
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def to_build(self) -> bool:  # List of task Maps
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('to_build', False)

    def set_to_build(self, to_build: bool = False):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['to_build'] = to_build
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def current_method(self) -> int:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('current_method', None)

    def set_current_method(self, current_method: int = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['current_method'] = current_method
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def current_step(self) -> int:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('current_step', None)

    def set_current_step(self, current_step: int = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['current_step'] = current_step
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def previous_data_source(self) -> str:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('previous_data_source', None)

    def set_previous_data_source(self, previous_data_source: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['previous_data_source'] = previous_data_source
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def previous_task(self) -> str:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('previous_task', None)

    def set_previous_task(self, previous_task: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['previous_task'] = previous_task
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def requested_task(self) -> str:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('requested_task', None)

    def set_requested_task(self, requested_task: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['requested_task'] = requested_task
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def list_item_selected(self) -> int:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('list_item_selected', None)

    def set_list_item_selected(self, list_item_selected: int = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['list_item_selected'] = list_item_selected
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def facts_per_step(self) -> List:  # list of ints
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('facts_per_step', None)

    def set_facts_per_step(self, facts_per_step: List = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['facts_per_step'] = facts_per_step
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def conversation_id(self) -> str:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('facts_per_step', None)

    def set_conversation_id(self, conversation_id: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['conversationId'] = conversation_id
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def decisions(self) -> List:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('decisions', None)

    def set_decisions(self, decisions: List = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['decisions'] = decisions
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def game_over(self) -> bool:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('game_over', None)

    def set_game_over(self, game_over: bool = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['game_over'] = game_over
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def indirect_access(self) -> bool:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('game_over', None)

    def set_indirect_access(self, indirect_access: bool = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['indirect_access'] = indirect_access
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def tree_choice(self) -> int:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('tree_choice', None)

    def set_tree_choice(self, tree_choice: int = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['tree_choice'] = tree_choice
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def dimensions_rnd_order(self) -> List:  # list of ints
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('dimensions_rnd_order', None)

    def set_dimensions_rnd_order(self, dimensions_rnd_order: List = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['dimensions_rnd_order'] = dimensions_rnd_order
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def attempting_to_leave(self) -> bool:  # list of ints
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('dimensions_rnd_order', None)

    def set_attempting_to_leave(self, attempting_to_leave: bool = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['attempting_to_leave'] = attempting_to_leave
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def number_to_read(self) -> int:  # list of ints
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('number_to_read', None)

    def set_number_to_read(self, number_to_read: int = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['number_to_read'] = number_to_read
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def fact_to_say(self) -> map:  # map of score and text
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('fact_to_say', None)

    def set_fact_to_say(self, fact_to_say: map = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['fact_to_say'] = fact_to_say
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def has_said_fact(self) -> bool:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('has_said_fact', None)

    def set_has_said_fact(self, has_said_fact: bool = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['has_said_fact'] = has_said_fact
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def game_last_response(self) -> str:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('game_last_response', None)

    def set_game_last_response(self, game_last_response: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['game_last_response'] = game_last_response
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def previous_wikihow_search_query(self) -> str:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('game_last_response', None)

    def set_previous_wikihow_search_query(self, previous_wikihow_search_query: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['previous_wikihow_search_query'] = previous_wikihow_search_query
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def previous_recipe_search_query(self) -> str:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('game_last_response', None)

    def set_previous_recipe_search_query(self, previous_recipe_search_query: str = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['previous_recipe_search_query'] = previous_recipe_search_query
        return self.state_manager.write_user_attributes(_user_attributes)

    @property
    def current_ingredient(self) -> int:
        _user_attributes = self.state_manager.user_attributes
        return _user_attributes.get('game_last_response', None)

    def set_current_ingredient(self, current_ingredient: int = None):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        _user_attributes = self.state_manager.user_attributes
        _user_attributes['current_ingredient'] = current_ingredient
        return self.state_manager.write_user_attributes(_user_attributes)

