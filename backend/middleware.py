
from langchain.agents.middleware import AgentMiddleware

class LoggingMiddleware(AgentMiddleware):

    # before_agent -> 1
    # after_agent -> 1

    # before model -> multiple times
    # after model -> multiple times

    def before_agent(self, state, runtime):
        print("\n### Before Agent###\n")
        # print(f"state\n {state}\n")

    def after_agent(self, state, runtime):
        print("\n### After Agent###\n")
        # print(f"state\n {state}\n")

    def before_model(self, state, runtime):
        print("\n### Before Model###\n")
        # print(f"state\n {state}\n")

    def after_model(self, state, runtime):
        print("\n### After Model###\n")
        # print(f"state\n {state}\n")
        user_limit = 1000

"""
 "input_tokens": 374,
          "output_tokens": 45,
          "total_tokens": 419,

           "input_tokens": 374,
          "output_tokens": 45,
          "total_tokens": 419,

     "input_tokens": 460,
          "output_tokens": 119,
          "total_tokens": 579,

           "input_tokens": 460,
          "output_tokens": 134,
          "total_tokens": 594,

"""   


