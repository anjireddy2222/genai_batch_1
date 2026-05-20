
pip install llama-index openai pypdf
pip install llama-index-llms-openai
pip install dotenv

✅ txt
✅ pdf
✅ docx
✅ csv
✅ markdown
✅ html


OPENAI_API_KEY=xxxxx
ANTHROPIC_API_KEY=yyyyy

from llama_index.llms.anthropic import Anthropic

llm = Anthropic(model="claude-3-sonnet-20240229")



