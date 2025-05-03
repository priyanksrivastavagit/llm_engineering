import os
import io
import sys
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
from IPython.display import Markdown, display, update_display
import subprocess
import gradio as gr
from loguru import logger

# Load environment variables
load_dotenv("../.env")

# Load Models
#openai_api_key = os.getenv('OPENAI_API_KEY')
CLAUDE_MODEL = os.getenv('CLAUDE_MODEL')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')

pi = """
import time

def calculate(iterations, param1, param2):
    result = 1.0
    for i in range(1, iterations+1):
        j = i * param1 - param2
        result -= (1/j)
        j = i * param1 + param2
        result += (1/j)
    return result

start_time = time.time()
result = calculate(100_000_000, 4, 1) * 4
end_time = time.time()

print(f"Result: {result:.12f}")
print(f"Execution Time: {(end_time - start_time):.6f} seconds")
"""

css = """
.inp {background-color: #306998;}
.converted_lang_out {background-color: #050;}
"""


# Initiate connections to AI Models
logger.info("Initiating Large Language Model(LLM) connections for OpenAI and Anthropic.")
openai = OpenAI()
claude = anthropic.Anthropic()

class CodeConverter:

  def __init__(self, python):
    self.python = python

  def run(self):

    with gr.Blocks(css=css) as ui:
      
      def system_message(target_lang):
        system_message = f"You are an assistant that re-engineers a Python code into a highly performant {target_lang} code."
        system_message += f"Respond only with {target_lang} code with occasional comments and no detailed explanation."
        system_message += "Remember to include all relevant libraries and import functions which are used in the code."
        system_message += "For Go language, after converting teh code, remove any libraries and functions which are not referenced in the code."
        system_message += "For Rust language, source all the crates required for executing the code logic. Do not add any tips, note and hints in the code. Do not add suggestions related to Cargo.toml."
        system_message += f"The {target_lang} code needs to produce identitical output in the most performant way."

        logger.info(f"system message: {system_message}")

        return system_message
      
      def user_prompt_for(python, target_lang):
        user_prompt = f"Re-engineer the pyton code into a high-performant {target_lang} code producing identitical output in the least amount of time."
        user_prompt += f"Respond only with {target_lang} code with occasional comments and no detailed explanation."
        user_prompt += "Pay attention to the datatypes assigned to the function parameters and return values for functions."
        user_prompt += "For Java code, keep the public class name as optimized_output and include all the relevant import libraries."
        user_prompt += "For Rust language, add all crates including extern crates referenced in the code to execute the logic if required. Generate the code compatible with the latest rust version."
        user_prompt += "Pay attention to number types to ensure no int overflows. Remember to #include all necessary C++ packages such as iomanip if the target language is c++.\n\n"
        user_prompt += python

        logger.info(f"user prompt: {user_prompt}")

        return user_prompt  
    
      def messages_for(python, target_lang):
        return [
                  {"role": "system", "content": system_message(target_lang)},
                  {"role": "user", "content": user_prompt_for(python, target_lang)}
              ]
      
      def write_output_cpp(cpp):

        logger.info(f"Creating a new cpp(C++) file: {os.getcwd()}/optimized_output.cpp")
        cpp_cleansed = cpp.replace("```cpp", "").replace("```", "")
        with open(f"{os.getcwd()}/optimized_output.cpp", "w") as f:
          f.write(cpp_cleansed)

        return cpp_cleansed
      
      def write_output_rust(rust):

        logger.info(f"Creating a new Rust file: {os.getcwd()}/optimized_output.rs")
        rust_cleansed = rust.replace("```rust", "").replace("```", "")
        with open(f"{os.getcwd()}/optimized_output.rs", "w") as f:
          f.write(rust_cleansed)

          return rust_cleansed
        
      def write_output_java(java):

        logger.info(f"Creating a new Rust file: {os.getcwd()}/optimized_output.java")
        java_cleansed = java.replace("```java", "").replace("```", "")
        with open(f"{os.getcwd()}/optimized_output.java", "w") as f:
          f.write(java_cleansed)

        return java_cleansed
      
      def write_output_go(go):

        logger.info(f"Creating a new Rust file: {os.getcwd()}/optimized_output.go")
        go_cleansed = go.replace("```go", "").replace("```", "")
        with open(f"{os.getcwd()}/optimized_output.go", "w") as f:
          f.write(go_cleansed)

          return go_cleansed
        
      def output_gpt(python, target_lang):

        logger.info(f"Code conversion from python to {target_lang} conversion using GPT.")
        try:
          stream = openai.chat.completions.create(model=OPENAI_MODEL, messages=messages_for(python, target_lang), stream=True)
          reply = ""
          for chunk in stream:
            fragment = chunk.choices[0].delta.content or ""
            reply += fragment
            #print(fragment, end='', flush=True)

          if target_lang == "C++":
            yield write_output_cpp(reply)
          elif target_lang == "Java":
            yield write_output_java(reply)
          elif target_lang == "Rust":
            yield write_output_rust(reply)
          elif target_lang == "Go":
            yield write_output_go(reply)

        except Exception as e:
          logger.error(e)
          raise

      def output_claude(python, target_lang):

        logger.info(f"Code conversion from python to {target_lang} conversion using CLAUDE.")
        result = claude.messages.stream(
            model=CLAUDE_MODEL,
            max_tokens=2000,
            system=system_message,
            messages=[{"role": "user", "content": user_prompt_for(python)}],
        )
        reply = ""
        with result as stream:
            for text in stream.text_stream:
                reply += text

        if target_lang == "C++":
          yield write_output_cpp(reply)
        elif target_lang == "Java":
          yield write_output_java(reply)
        elif target_lang == "Rust":
          yield write_output_rust(reply)
        elif target_lang == "Go":
          yield write_output_go(reply)

      def execute_python(python):

        try:
          output = io.StringIO()
          sys.stdout = output
          exec(python)

        except Exception as e:
          logger.error(e)
          raise

        return output.getvalue()

      def execute_go(filename=f"{os.getcwd()}/optimized_output.go"):

        try:
          cmd = ["go", "run", filename]
          result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        except Exception as e:
          logger.error(e)
          raise
        
        return result.stdout
      
      def execute_rust():
        
        try:
          cmd = ["/Users/priyanksrivastava/.cargo/bin/cargo", "run"]
          p = subprocess.run(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)

          if p.stderr != "" and p.stderr is not None:
            print(p.stderr)
            exit(1)

        except Exception as e:
          logger.error(e)
          raise

        #p = subprocess.run("./optimized_output", stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
        return p.stdout
      
      def execute_java():

        try:

          subprocess.check_call(['javac', f"{os.getcwd()}/optimized_output.java"])

          java_class, ext = os.path.splitext(f"{os.getcwd()}/optimized_output.java")

          cmd = ['java', java_class.split("/")[-1]]

          p = subprocess.run(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)

        except Exception as e:
          logger.error(e)
          raise
        
        return p.stdout

      def execute_cpp(filename=f"{os.getcwd()}/optimized_output.cpp"):

        try:
          cmd = ["clang++", "-O3", "-std=c++17", "-march=nocona", "-o", "optimized", filename]
          p = subprocess.run(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
          print(p.stdout)

          p1 = subprocess.run("./optimized", stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)

        except Exception as e:
          logger.error(e)
          raise
        
        return p1.stdout

      def optimize(python_code, target_language, model):
        """Optimizes Python code by converting it to a specified target language using AI models. 
        """

        try:
            if model == "GPT":
                for partial in output_gpt(python_code, target_language):
                    return partial
            elif model == "Claude":
                for partial in output_gpt(python_code, target_language):
                    return partial
        
        except Exception as e:
            raise(e)
        
      with gr.Row():
        inp = gr.Textbox(label="Python Code:", value=self.python, lines=10, show_copy_button=True)
        converted_lang_out = gr.Textbox(label="Converted Code:", lines=10, show_copy_button=True)
        
      with gr.Row():
          model = gr.Dropdown(["GPT", "Claude"], label="Select Model:", value="GPT")

      with gr.Row():
          converted_lang = gr.Radio(["Java", "C++", "Go", "Rust"], label="Select the target language", value="Java")
      with gr.Row():
          convert_code = gr.Button("Convert Code")
      with gr.Row():
          python_run = gr.Button("Execute Python Code")
          conv_code_run = gr.Button(f"Execute Converted Code")
      with gr.Row():
          python_out = gr.TextArea(label="Python result:", elem_classes=["inp"])
          conv_code_out = gr.TextArea(label="Converted Code result:", elem_classes=["converted_lang_out"])

      def execute_conv_code(converted_lang):
          value = converted_lang
          if value == "Java":
              return execute_java()
          elif value == "C++":
              return execute_cpp()
          elif value == "Rust":
              return execute_rust()
          elif value == "Go":
              return execute_go()
          else:
              raise "Please select a valid language from the list."
          
      def converted_code(inp, converted_lang, model):

          value = converted_lang
          
          return optimize(inp, value, model)
      
      #convert_code.click(optimize, inputs=[inp, converted_lang], outputs=[converted_lang_out],)
      convert_code.click(converted_code, [inp, converted_lang, model], [converted_lang_out],)
      
      python_run.click(execute_python, [inp], [python_out])
      conv_code_run.click(execute_conv_code, converted_lang, [conv_code_out])

    ui.launch(inbrowser=True)

    ui.close()

if __name__ == "__main__":
  CodeConverter(pi).run()
