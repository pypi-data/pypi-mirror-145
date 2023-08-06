from twiz_cobot.custom_libraries.response_generator.src.abstract_response_generator.abstract_rg_apl_builder import \
    ResponseGeneratorAPLBuilder
from twiz_cobot.custom_libraries.response_generator.src.abstract_response_generator.abstract_rg_update_state import \
    ResponseGeneratorUpdateState
import requests


class ResponseGeneratorController:
    state_updater: ResponseGeneratorUpdateState
    apl_builder: ResponseGeneratorAPLBuilder
    response_string_url: str
    timeout_in_millis: int

    def __init__(self, state_updater: ResponseGeneratorUpdateState,
                 apl_builder: ResponseGeneratorAPLBuilder, response_string_url: str, timeout_in_millis: int = 1000):
        self.state_updater = state_updater
        self.apl_builder = apl_builder
        self.response_string_url = response_string_url
        self.timeout_in_millis = timeout_in_millis

    def run(self) -> dict:
        """
        Invoke ResponseGeneratorUpdateState, ResponseStringController
        and other MLRemoteModule if required.
        """
        # Update necessary state attributes
        twiz_state = self.state_updater.run()

        # Get response string from response string controller microservice
        response_string = requests.post(self.response_string_url,
                                        headers={'content-type': 'application/json'},
                                        timeout=self.timeout_in_millis / 1000.0)
        response_string_json = response_string.json()

        response = response_string_json.get("response_string", None)
        if not response:
            raise Exception("Unable to get response_string")

        # Get apl doc and directives if needed
        if twiz_state.curr().is_apl_supported:
            directives = self.apl_builder.run(twiz_state)
            if directives:
                return {'response': response, 'directives': directives}

        return {'response': response}
