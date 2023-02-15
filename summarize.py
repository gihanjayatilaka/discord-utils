# Run like python summarize.py log.txt > summary.txt

import logging
import sys

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

logger = logging.getLogger(__name__)

class RateLimitedOpenAI(OpenAI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rate_limit = 0.5

def summarize(filename):
    llm = OpenAI()
    log = open(filename).read()
    chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=3500*3, chunk_overlap=100*3, length_function=len
    )
    sublogs = text_splitter.split_text(log)
    docs = [Document(page_content=t) for t in sublogs]
    print(f"Split log into {len(docs)} sublogs.")
    print(chain.run(input_documents=docs))  # , token_max=3500))
    # prompt = PromptTemplate(
    #     input_variables=["product"],
    #     template=("Summarize the following chat log in under 50 words. Cite "
    #      "usernames and timestamps.\n\n{log}",)
    # )
    # chain = LLMChain(llm=llm, prompt=prompt)
    # print(chain.run(open(filename).read()))


if __name__ == "__main__":
    # Just log level, YYMMDD:HHMMSS, and message.
    logging.basicConfig(
        format="%(levelname)s:%(asctime)s:%(message)s", level=logging.INFO
    )
    summarize(sys.argv[1])
