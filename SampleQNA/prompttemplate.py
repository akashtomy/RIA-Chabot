import os
import re

import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

from secret_key import openapi_key

os.environ["OPENAI_API_KEY"] = openapi_key

def main():
    st.set_page_config(page_title="Prompt Template")
    st.header("Prompt Template")
    prompt = st.text_area("Enter your prompt: (Press Ctrl + Enter to confirm)")

    if prompt:
        prompt_keywords = []
        prompt_inputs = []

        regex = r"\{(.*?)\}"
        matches = re.finditer(regex, prompt, re.MULTILINE | re.DOTALL)

        #Check the prompt for all the keywords inside the curly braces {}
        for matchNum, match in enumerate(matches):
            for groupNum in range(0, len(match.groups())):
                #It is only a keywords if it is a single word
                if (len(re. findall(r'\w+', match.group(1))) == 1):
                    prompt_keywords.append(match.group(1))

        st.subheader("Fill in the prompt keyword/s")
        for keyword in prompt_keywords:
            input = st.text_input(keyword + ": ")
            if input != '':
                prompt_inputs.append(input)

        #If all the keywords have their respective inputs
        if (len(prompt_keywords) == len(prompt_inputs)):
            kwargs = {}

            for i in range(len(prompt_keywords)):
                kwargs[prompt_keywords[i]] = prompt_inputs[i]

            openai = OpenAI(model_name="text-davinci-003", openai_api_key=openapi_key)
            prompt_template = PromptTemplate(input_variables=prompt_keywords,template=prompt)

            st.write(openai(prompt_template.format(**kwargs)))

if __name__ == "__main__":
    main()
