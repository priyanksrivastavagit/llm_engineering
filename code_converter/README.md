# <center>📦 TransCodeX</center> $${\color{lightyellow}Code \space once \space -> \space Run \space fast \space anywhere}$$

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-informational)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude--3-success)
![Gradio](https://img.shields.io/badge/UI-Gradio-orange)

> **AI-Powered Code Transpiler**: Convert Python code into high-performance Java, C++, Go, or Rust code using OpenAI GPT or Anthropic Claude.

---

## ✨ Features

* 🔄 **Python-to-X Transpiler** (Java, C++, Go, Rust)
* 🤖 Support for **OpenAI GPT** and **Anthropic Claude**
* 🧠 Smart prompts for optimal performance output
* 🧪 Built-in execution of original and transpiled code
* 🌐 Web-based UI using **Gradio**
* 🗃️ Saves and cleans target code to appropriate language files

---

## 📸 Screenshots

### 🔧 Gradio Web UI

![UI Screenshot](https://user-images.githubusercontent.com/your-username/codeconverter-ui.png)

### ⚙️ Example Output Comparison

![Comparison Screenshot](https://user-images.githubusercontent.com/your-username/codeconverter-compare.png)

---

## 📁 Directory Structure

```bash
.
├── code_converter.py     # Main app
├── .env                  # Your API Keys
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/codeconverter.git
cd codeconverter
```

### 2. Create a `.env` File

```env
OPENAI_API_KEY=your_openai_api_key
CLAUDE_API_KEY=your_claude_api_key
OPENAI_MODEL=gpt-4
CLAUDE_MODEL=claude-3-opus-20240229
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
python code_converter.py
```

---

## 🧠 Example Input/Output

### 🐍 Input (Python):

```python
def calculate(iterations, param1, param2):
    result = 1.0
    for i in range(1, iterations+1):
        j = i * param1 - param2
        result -= (1/j)
        j = i * param1 + param2
        result += (1/j)
    return result
```

### ☕ Output (Java):

```java
public class optimized_output {
    public static void main(String[] args) {
        double result = 1.0;
        int iterations = 100000000;
        for (int i = 1; i <= iterations; i++) {
            double j = i * 4 - 1;
            result -= (1.0 / j);
            j = i * 4 + 1;
            result += (1.0 / j);
        }
        System.out.printf("Result: %.12f%n", result * 4);
    }
}
```

---

## 🛠️ Language Support

* ✅ Java
* ✅ C++
* ✅ Go
* ✅ Rust

Each output file is named `optimized_output.*` and is automatically saved.

---

## ❗ Notes

* Claude and GPT streams are handled asynchronously for responsiveness
* Error handling and logging via `loguru`
* Python and transpiled code are run in sandboxed subprocesses
* Java requires `javac`, Rust requires `cargo`, Go requires `go` toolchain, and C++ uses `clang++`

---

## 📅 Roadmap

* [ ] Add more models like Deepseek, Mistral
* [ ] Add Docker support
* [ ] Add unit tests
* [ ] Add support for additional languages (e.g., C#, TypeScript, Kotlin)
* [ ] Performance benchmarking dashboard

---

## 🙋‍♂️ Contact

Made by [@priyanksrivastavagit](https://github.com/priyanksrivastavagit). Contributions welcome!

---

> "Empowering developers with AI to write faster, safer, and better code."
