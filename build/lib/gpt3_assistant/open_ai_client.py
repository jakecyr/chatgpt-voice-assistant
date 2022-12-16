import openai
from exchange import Exchange


class OpenAIClient:

    def __init__(self, api_key):
        # set API key on OpenAI object
        openai.api_key = api_key

    def get_completion(self, prompt, previous_responses):
        max_tokens = 100
        model = "text-davinci-003"
        request = self.get_request_under_max_tokens(max_tokens, prompt, previous_responses)

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

    @staticmethod
    def get_request_under_max_tokens(max_tokens, prompt, previous_responses):
        new_request = f"User: {prompt}\nAssistant: "
        request_header = ""

        for exchange in previous_responses:
            exchange_string = f"User: {exchange.get_user_message()}\nAssistant: {exchange.get_computer_response()}"
            draft_request = f"{request_header}\n{exchange_string}\n{new_request}"

            if len(draft_request) > max_tokens:
                return f"{request_header}\n{new_request}"
            else:
                request_header += f"\n{exchange_string}"

        return f"{request_header}\n{new_request}"
