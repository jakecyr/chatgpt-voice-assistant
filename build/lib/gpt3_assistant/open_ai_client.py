import openai
from exchange import Exchange


# Client to interact with the Open AI API
class OpenAIClient:

    def __init__(self, api_key: str):
        # set API key on OpenAI object
        openai.api_key = api_key

    def get_completion(self, **kwargs):
        """
        Get a completion (response) from the specified OpenAI GPT-3 model.
        Reference: https://beta.openai.com/docs/api-reference/completions

        :keyword str prompt:                the prompt to send to the model for completion.
        :keyword str previous_exchanges:    the previous exchanges for context.
        :keyword str model:                 optionally specify the model to use.
        :keyword int max_tokens:                the max number of tokens to use including the prompt and response.
        """
        if "prompt" not in kwargs:
            raise Exception("Missing required 'prompt' argument")

        if "previous_responses" not in kwargs:
            raise Exception("Missing required 'previous_responses' argument")

        prompt = kwargs['prompt']
        previous_exchanges = kwargs['previous_exchanges']
        model = kwargs['model'] if "model" in kwargs else 'text-davinci-003'
        max_tokens = kwargs['max_tokens'] if "max_tokens" in kwargs else 100

        request = self.get_request_under_max_tokens(max_tokens, prompt, previous_exchanges)

        completion = openai.Completion.create(
            model=model,
            prompt=request,
            max_tokens=max_tokens,
            temperature=0.7
        )

        choices = completion["choices"]
        tokens_used = completion['usage']['total_tokens']
        was_cut_short = False

        if len(choices) == 0:
            raise Exception(f"No choices returned from Open AI for prompt: {prompt}")

        first_choice = completion["choices"][0]

        if first_choice['finish_reason'] == 'length':
            print("OpenAI stopped producing output due to a limit on the max tokens")
            print(f"Max tokens is set to: {max_tokens}. Total tokens consumed with prompt were: {tokens_used}")
            was_cut_short = True

        first_choice_text = first_choice["text"].replace("\n", " ").strip()

        return Exchange(prompt, first_choice_text, was_cut_short)

    def _get_request_under_max_tokens(self, max_tokens, prompt, previous_exchanges):
        """
        Get a full request with previous context to send to the completion endpoint.
        :param int max_tokens: the max number of tokens to be used for the prompt.
        :param str prompt: the new prompt to be sent for completion.
        :param list[Exchange] previous_exchanges: the list of previous exchanges for context.
        :return: str the full request with context and the new prompt to be sent to the completion endpoint.
        """
        new_request = f"User: {prompt}\nAssistant: "
        request_header = ""

        for exchange in previous_exchanges:
            exchange_string = f"User: {exchange.get_user_message()}\nAssistant: {exchange.get_computer_response()}"
            draft_request = f"{request_header}\n{exchange_string}\n{new_request}"

            if len(draft_request) > max_tokens:
                return f"{request_header}\n{new_request}"
            else:
                request_header += f"\n{exchange_string}"

        return f"{request_header}\n{new_request}"
