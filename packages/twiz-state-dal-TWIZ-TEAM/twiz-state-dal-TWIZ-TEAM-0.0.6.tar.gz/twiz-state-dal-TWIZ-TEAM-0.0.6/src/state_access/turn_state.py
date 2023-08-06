
from enum import Enum
from twiz_cobot.custom_libraries.twiz_state_dal.src.state_access.twiz_state_manager import TwizStateManager


class StateType(Enum):
    PREV = 'last_state'
    CURR = 'current_state'


class TurnState:
    state_manager: TwizStateManager
    state_type: StateType

    def __init__(self, state_manager: TwizStateManager, state_type: StateType = StateType.CURR):
        self.state_manager = state_manager
        self.state_type = state_type

    @property
    def state(self) -> dict:
        if self.state_type == StateType.PREV:
            return self.state_manager.last_state
        elif self.state_type == StateType.CURR:
            return self.state_manager.current_state
        else:
            raise Exception("Unrecognized State")

    @property
    def text(self) -> str:
        return self.state.get('text', None) if self.state else None

    def set_text(self, text: str = None):
        self.state_manager.write_state_attribute('text', text)

    @property
    def intent(self) -> str:
        return self.state.get('intent', None) if self.state else None

    def set_intent(self, intent: str = None):
        self.state_manager.write_state_attribute('intent', intent)

    @property
    def apl_screen(self) -> str:
        return self.state.get('apl_screen', None) if self.state else None

    def set_apl_screen(self, apl_screen: str = None):
        self.state_manager.write_state_attribute('apl_screen', apl_screen)

    @property
    def conversation_phase(self) -> str:
        return self.state.get('conversation_phase', None) if self.state else None

    def set_conversation_phase(self, conversation_phase: str = None):
        self.state_manager.write_state_attribute('conversation_phase', conversation_phase)

    @property
    def current_method(self) -> int:
        return self.state.get('current_method', None) if self.state else None

    def set_current_method(self, current_method: int = None):
        self.state_manager.write_state_attribute('current_method', current_method)

    @property
    def current_step(self) -> int:
        return self.state.get('current_step', None) if self.state else None

    def set_current_step(self, current_step: int = None):
        self.state_manager.write_state_attribute('current_step', current_step)

    @property
    def choose_responder(self) -> str:
        return self.state.get('choose_responder', None) if self.state else None

    def set_choose_responder(self, choose_responder: str = None):
        self.state_manager.write_state_attribute('choose_responder', choose_responder)

    @property
    def data_source(self) -> str:
        return self.state.get('data_source', None) if self.state else None

    def set_data_source(self, data_source: str = None):
        self.state_manager.write_state_attribute('data_source', data_source)

    @property
    def identify_process_responder(self) -> str:
        return self.state.get('identify_process_responder', None) if self.state else None

    def set_identify_process_responder(self, identify_process_responder: str = None):
        self.state_manager.write_state_attribute('identify_process_responder', identify_process_responder)

    @property
    def evi_qa_responder(self) -> str:
        return self.state.get('evi_qa_responder', None) if self.state else None

    def set_evi_qa_responder(self, evi_qa_responder: str = None):
        self.state_manager.write_state_attribute('evi_qa_responder', evi_qa_responder)

    @property
    def fallback_responder(self) -> str:
        return self.state.get('fallback_responder', None) if self.state else None

    def set_fallback_responder(self, fallback_responder: str = None):
        self.state_manager.write_state_attribute('fallback_responder', fallback_responder)

    @property
    def is_experiment(self) -> bool:
        return self.state.get('is_experiment', None) if self.state else None

    def set_is_experiment(self, is_experiment: bool = None):
        self.state_manager.write_state_attribute('is_experiment', is_experiment)

    @property
    def is_factoid_question(self) -> bool:
        return self.state.get('is_factoid_question', False) if self.state else False

    def set_is_factoid_question(self, is_factoid_question: bool = None):
        self.state_manager.write_state_attribute('is_factoid_question', is_factoid_question)

    @property
    def launch_screen_selected_tile(self) -> str:
        return self.state.get('launch_screen_selected_tile', None) if self.state else None

    def set_launch_screen_selected_tile(self, launch_screen_selected_tile: int = None):
        self.state_manager.write_state_attribute('launch_screen_selected_tile', launch_screen_selected_tile)

    @property
    def launch_responder(self) -> str:
        return self.state.get('launch_responder', None) if self.state else None

    def set_launch_responder(self, launch_responder: int = None):
        self.state_manager.write_state_attribute('launch_responder', launch_responder)

    @property
    def list_item_selected(self) -> int:
        return self.state.get('list_item_selected', None) if self.state else None

    def set_list_item_selected(self, list_item_selected: int = None):
        self.state_manager.write_state_attribute('list_item_selected', list_item_selected)

    @property
    def query_result_ids(self) -> map:
        return self.state.get('query_result_ids', None) if self.state else None

    def set_query_result_ids(self, query_result_ids: map = None):
        self.state_manager.write_state_attribute('query_result_ids', query_result_ids)

    @property
    def recipe_basic_qa(self) -> str:
        return self.state.get('recipe_basic_qa', None) if self.state else None

    def set_recipe_basic_qa(self, recipe_basic_qa: str = None):
        self.state_manager.write_state_attribute('recipe_basic_qa', recipe_basic_qa)

    @property
    def sensitive(self) -> map:
        return self.state.get('sensitive', None) if self.state else None

    def set_sensitive(self, sensitive: map = None):
        self.state_manager.write_state_attribute('sensitive', sensitive)

    @property
    def sensitive_responder(self) -> str:
        return self.state.get('sensitive_responder', None) if self.state else None

    def set_sensitive_responder(self, sensitive_responder: str = None):
        self.state_manager.write_state_attribute('sensitive_responder', sensitive_responder)

    @property
    def show_steps_responder(self) -> str:
        return self.state.get('show_steps_responder', None) if self.state else None

    def set_show_steps_responder(self, show_steps_responder: str = None):
        self.state_manager.write_state_attribute('show_steps_responder', show_steps_responder)

    @property
    def task_chosen(self) -> map:
        return self.state.get('task_chosen', None) if self.state else None

    def set_task_chosen(self, task_chosen: map = None):
        self.state_manager.write_state_attribute('task_chosen', task_chosen)

    @property
    def task_classifier_result(self) -> str:
        return self.state.get('task_classifier_result', None) if self.state else None

    def set_task_classifier_result(self, task_classifier_result: str = None):
        self.state_manager.write_state_attribute('task_classifier_result', task_classifier_result)

    @property
    def task_complete_responder(self) -> str:
        return self.state.get('task_complete_responder', None) if self.state else None

    def set_task_complete_responder(self, task_complete_responder: str = None):
        self.state_manager.write_state_attribute('task_complete_responder', task_complete_responder)

    @property
    def task_step_detail_responder(self) -> str:
        return self.state.get('task_step_detail_responder', None) if self.state else None

    def set_task_step_detail_responder(self, task_step_detail_responder: str = None):
        self.state_manager.write_state_attribute('task_step_detail_responder', task_step_detail_responder)

    @property
    def user_event(self) -> map:
        return self.state.get('user_event', None) if self.state else None

    def set_user_event(self, user_event: map = None):
        self.state_manager.write_state_attribute('user_event', user_event)

    @property
    def user_event_identify_process_responder(self) -> str:
        return self.state.get('user_event_identify_process_responder', None) if self.state else None

    def set_user_event_identify_process_responder(self, user_event_identify_process_responder: str = None):
        self.state_manager.write_state_attribute('user_event_identify_process_responder', user_event_identify_process_responder)

    @property
    def visible_components(self) -> map:
        return self.state.get('visible_components', None) if self.state else None

    def set_visible_components(self, visible_components: map = None):
        self.state_manager.write_state_attribute('visible_components', visible_components)

    @property
    def yes_no_responder(self) -> str:
        return self.state.get('yes_no_responder', None) if self.state else None

    def set_yes_no_responder(self, yes_no_responder: str = None):
        self.state_manager.write_state_attribute('yes_no_responder', yes_no_responder)

    # ----- variables which can only be read, not set ----- #
    @property
    def is_apl_supported(self) -> bool:
        supported_interfaces = self.state.get('supported_interfaces', None) if self.state else None
        if supported_interfaces:
            return supported_interfaces.get('apl', False)
        else:
            return False

    @property
    def creation_date_time(self) -> str:
        return self.state.get('creation_date_time', None) if self.state else None

    @property
    def app_id(self) -> str:
        return self.state.get('app_id', None) if self.state else None

    @property
    def ask_access_token(self) -> str:
        return self.state.get('ask_access_token', None) if self.state else None

    @property
    def asr(self) -> str:
        return self.state.get('asr', None) if self.state else None

    @property
    def candidate_responses(self) -> str:
        return self.state.get('candidate_responses', None) if self.state else None

    @property
    def conversation_id(self) -> str:
        return self.state.get('conversation_id', None) if self.state else None

    @property
    def coref(self) -> str:
        return self.state.get('coref', None) if self.state else None

    @property
    def directives(self) -> str:
        return self.state.get('directives', None) if self.state else None

    @property
    def input_offensive(self) -> str:
        return self.state.get('input_offensive', None) if self.state else None

    @property
    def intentdetection(self) -> str:
        return self.state.get('intentdetection', None) if self.state else None

    @property
    def next_responder(self) -> str:
        return self.state.get('next_responder', None) if self.state else None

    @property
    def nounphrases(self) -> str:
        return self.state.get('nounphrases', None) if self.state else None

    @property
    def phonemes(self) -> str:
        return self.state.get('phonemes', None) if self.state else None

    @property
    def punctuation(self) -> str:
        return self.state.get('punctuation', None) if self.state else None

    @property
    def request_type(self) -> str:
        return self.state.get('request_type', None) if self.state else None

    @property
    def response(self) -> str:
        return self.state.get('response', None) if self.state else None

    @property
    def resume_responder(self) -> str:
        return self.state.get('resume_responder', None) if self.state else None

    @property
    def resume_task(self) -> str:
        return self.state.get('resume_task', None) if self.state else None

    @property
    def sentiment_score(self) -> str:
        return self.state.get('sentiment_score', None) if self.state else None

    @property
    def slots(self) -> str:
        return self.state.get('slots', None) if self.state else None

    @property
    def user_id(self) -> str:
        return self.state.get('user_id', None) if self.state else None




