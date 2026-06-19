"""
Multi-Capability AI Assistant
<<<<<<< HEAD
Agentic AI Bootcamp  | Session 2 Assignment
=======
Agentic AI Bootcamp - atomcamp | Session 2 Assignment
>>>>>>> 2bed40a808f3ef7387cdeff36f728101e0f20c34
Author: Khansa Shakeel Ahmed
"""

import os
import json
import math
import re
import statistics
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
<<<<<<< HEAD
from groq import Groq
=======
from openai import OpenAI
>>>>>>> 2bed40a808f3ef7387cdeff36f728101e0f20c34

load_dotenv()

# ──────────────────────────────────────────────
#  TOOL FUNCTIONS
# ──────────────────────────────────────────────

def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    Supports: +, -, *, /, **, %, sqrt, abs, log, floor, ceil, round, pi, e
    """
    try:
        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("_")
        }
        allowed_names.update({"abs": abs, "round": round})
        # Sanitise: only allow math-safe characters
        if re.search(r"[a-zA-Z_]", expression):
            # strip any identifier not in allowed_names
            for token in re.findall(r"[a-zA-Z_]+", expression):
                if token not in allowed_names:
                    return json.dumps({"error": f"Unknown function or variable: '{token}'"})
        result = eval(expression, {"__builtins__": {}}, allowed_names)  # noqa: S307
        return json.dumps({"expression": expression, "result": result})
    except ZeroDivisionError:
        return json.dumps({"error": "Division by zero"})
    except Exception as e:
        return json.dumps({"error": f"Calculation failed: {e}"})


def web_search(query: str) -> str:
    """
    Mock web search that returns realistic, structured results.
    In production, replace with SerpAPI / Tavily / DuckDuckGo.
    """
    mock_db = {
        "python": "Python 3.12 released Oct 2023. Key features: f-string improvements, improved error messages, faster CPython. Source: python.org",
        "machine learning": "ML is a subset of AI enabling systems to learn from data without explicit programming. Top frameworks: PyTorch, TensorFlow, scikit-learn.",
        "langchain": "LangChain is an open-source framework for building LLM-powered applications with chains, agents, and memory. Latest: v0.2.x (2024).",
        "openai": "OpenAI offers GPT-4o, GPT-4 Turbo, and o1 models. ChatGPT has 100M+ weekly users as of 2024.",
        "karachi": "Karachi is Pakistan's largest city with 14M+ people. Financial capital, home to PSX. Climate: hot semi-arid.",
        "rag": "Retrieval-Augmented Generation (RAG) grounds LLM responses in external knowledge. Key components: vector DB, embeddings, retriever, generator.",
        "fastapi": "FastAPI is a modern Python web framework. Ranked #1 in speed among Python frameworks. Auto-generates OpenAPI docs.",
        "default": "Web search results for '{query}': Multiple sources indicate this is a widely discussed topic. For best results, consult domain-specific resources.",
    }
    q_lower = query.lower()
    for key, value in mock_db.items():
        if key in q_lower:
            return json.dumps({"query": query, "result": value, "source": "mock_search"})
    return json.dumps({
        "query": query,
        "result": mock_db["default"].format(query=query),
        "source": "mock_search",
    })


def analyze_data(numbers_str: str, operation: str = "all") -> str:
    """
    Perform statistical analysis on a comma-separated list of numbers.
    Operations: sum | mean | max | min | median | std | all
    """
    try:
        numbers = [float(n.strip()) for n in numbers_str.split(",") if n.strip()]
        if not numbers:
            return json.dumps({"error": "No valid numbers provided"})

        ops = {
            "sum": sum(numbers),
            "mean": statistics.mean(numbers),
            "max": max(numbers),
            "min": min(numbers),
            "median": statistics.median(numbers),
            "std": round(statistics.stdev(numbers), 4) if len(numbers) > 1 else 0,
            "count": len(numbers),
        }
        if operation == "all":
            return json.dumps({"numbers": numbers, **ops})
        if operation in ops:
            return json.dumps({"operation": operation, "result": ops[operation]})
        return json.dumps({"error": f"Unknown operation '{operation}'. Use: {list(ops)}"})
    except ValueError as e:
        return json.dumps({"error": f"Invalid number in list: {e}"})


def get_time_info(timezone: str = "PKT") -> str:
    """
    Return current time/date. Supports common timezone labels (mock offsets).
    """
    utc_offset_map = {
        "PKT": 5, "UTC": 0, "EST": -5, "PST": -8,
        "GMT": 0, "IST": 5.5, "CET": 1, "JST": 9, "GST": 4,
    }
    tz = timezone.upper()
    offset = utc_offset_map.get(tz)
    if offset is None:
        return json.dumps({"error": f"Unknown timezone '{tz}'. Supported: {list(utc_offset_map)}"})
    from datetime import timezone as tz_module, timedelta
    now = datetime.now(tz_module.utc) + timedelta(hours=offset)
    return json.dumps({
        "timezone": tz,
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "day": now.strftime("%A"),
        "date": now.strftime("%B %d, %Y"),
        "time": now.strftime("%I:%M %p"),
    })


# ──────────────────────────────────────────────
#  TOOL SCHEMAS  (OpenAI function-calling format)
# ──────────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression accurately. Use for any arithmetic, percentages, or math involving numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to evaluate, e.g. '15/100 * 200' or 'sqrt(144)'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information, facts, or research on a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_data",
            "description": "Perform statistical analysis (sum, mean, max, min, median, std) on a list of numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "numbers_str": {
                        "type": "string",
                        "description": "Comma-separated numbers, e.g. '10, 20, 30, 45'",
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["sum", "mean", "max", "min", "median", "std", "all"],
                        "description": "Statistical operation to perform. Default is 'all'.",
                    },
                },
                "required": ["numbers_str"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_time_info",
            "description": "Get current date and time in a specified timezone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone code, e.g. PKT, UTC, EST, IST. Default: PKT",
                    }
                },
                "required": [],
            },
        },
    },
]

FUNCTION_MAP = {
    "calculate": calculate,
    "web_search": web_search,
    "analyze_data": analyze_data,
    "get_time_info": get_time_info,
}


# ──────────────────────────────────────────────
#  MULTI-CAPABILITY ASSISTANT
# ──────────────────────────────────────────────

class MultiCapabilityAssistant:
    """
    Routes user requests to one of three capabilities:
    1. Enhanced Email Writer  – drafts professional emails with optional web research
    2. Smart Summarizer       – summarises text with analytics
    3. Chat Assistant         – general Q&A with persistent conversation memory
    """

    SYSTEM_BASE = """You are a helpful, concise AI assistant with access to tools.
Always use the calculate tool for any math. Use web_search when you need factual/current info.
Use analyze_data for statistical questions. Use get_time_info for date/time questions.
Be precise, well-structured, and professional but friendly."""

    EMAIL_SYSTEM = """You are an expert professional email writer.
Given a description, you write a complete email with:
- A clear, compelling Subject line
- Proper greeting
- Well-structured body
- Appropriate closing
Adapt your tone: formal, friendly, or casual as requested.
Use web_search if you need to research the topic before writing.
Format output as:
Subject: <subject>

<email body>"""

    SUMMARIZER_SYSTEM = """You are a precise text summarizer.
Summarize the given text clearly. Then provide analytics:
- Original word count
- Summary word count  
- Reduction percentage
- 3 key themes/topics as bullet points
Format output clearly with sections: SUMMARY, ANALYTICS, KEY THEMES."""

    def __init__(self):
<<<<<<< HEAD
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
         raise EnvironmentError(
        "GROQ_API_KEY not found. Add it to your .env file."
    )
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"
=======
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "OPENAI_API_KEY not found. Copy .env.example to .env and add your key."
            )
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
>>>>>>> 2bed40a808f3ef7387cdeff36f728101e0f20c34
        self.chat_history: list[dict] = []

    # ── Tool execution engine ──────────────────

    def _run_tools(self, response) -> Optional[str]:
        """Execute all tool calls in a response and return combined results."""
        if not response.choices[0].message.tool_calls:
            return None
        results = []
        for tc in response.choices[0].message.tool_calls:
            fn_name = tc.function.name
            fn_args = json.loads(tc.function.arguments)
            if fn_name in FUNCTION_MAP:
                result = FUNCTION_MAP[fn_name](**fn_args)
                results.append({
                    "tool_call_id": tc.id,
                    "role": "tool",
                    "name": fn_name,
                    "content": result,
                })
        return results

    def _call_with_tools(self, messages: list, system: str) -> str:
        """
        Single agentic loop: call LLM → execute tools → call LLM again until done.
        """
        full_messages = [{"role": "system", "content": system}] + messages
        for _ in range(5):  # max 5 tool-use turns
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                tools=TOOLS,
                tool_choice="auto",
            )
            msg = response.choices[0].message
            if not msg.tool_calls:
                return msg.content or ""

            # Append assistant's tool-call message
            full_messages.append(msg)
            # Execute tools and append results
            tool_results = self._run_tools(response)
            full_messages.extend(tool_results)

        return "Max tool iterations reached."

    # ── Capability 1: Email Writer ─────────────

    def write_email(self, description: str, tone: str = "formal") -> str:
        """Draft a complete email based on description and tone."""
        prompt = f"Write an email for the following request.\nTone: {tone}\nRequest: {description}"
        return self._call_with_tools([{"role": "user", "content": prompt}], self.EMAIL_SYSTEM)

    # ── Capability 2: Smart Summarizer ─────────

    def summarize(self, text: str, length: str = "medium") -> str:
        """Summarize text with analytics. Length: short | medium | long"""
        length_guide = {
            "short": "1-2 sentences",
            "medium": "3-4 sentences",
            "long": "5-6 sentences with detail",
        }.get(length, "3-4 sentences")
        prompt = (
            f"Summarize the following text in {length_guide}. "
            f"Then provide word count analytics and key themes.\n\nTEXT:\n{text}"
        )
        return self._call_with_tools([{"role": "user", "content": prompt}], self.SUMMARIZER_SYSTEM)

    # ── Capability 3: Chat Assistant ────────────

    def chat(self, user_input: str) -> str:
        """General chat with persistent memory."""
        self.chat_history.append({"role": "user", "content": user_input})
        response_text = self._call_with_tools(list(self.chat_history), self.SYSTEM_BASE)
        self.chat_history.append({"role": "assistant", "content": response_text})
        return response_text

    def clear_memory(self):
        """Reset conversation history."""
        self.chat_history = []

    # ── Smart Router ────────────────────────────

    def process(self, user_input: str) -> str:
        """
        Auto-route the request to the right capability based on intent signals.
        """
        u = user_input.strip().lower()

        # Email signals
        if any(k in u for k in ["write email", "draft email", "compose email", "send email",
                                  "email to", "email about", "formal email", "friendly email"]):
            tone = "casual" if "casual" in u else ("friendly" if "friendly" in u else "formal")
            return self.write_email(user_input, tone=tone)

        # Summarizer signals
        if u.startswith("summarize") or u.startswith("summarise") or "tldr" in u or "summary of" in u:
            length = "short" if "short" in u else ("long" if "long" in u else "medium")
            # Strip leading keyword
            text = re.sub(r"^(summarize|summarise|tldr)[:\s]*", "", user_input, flags=re.I).strip()
            return self.summarize(text or user_input, length=length)

        # Default: chat (with memory + tools)
        return self.chat(user_input)


# ──────────────────────────────────────────────
#  CLI INTERFACE
# ──────────────────────────────────────────────

BANNER = """
╔══════════════════════════════════════════════════════════╗
║         🤖  Multi-Capability AI Assistant  🤖            ║
║         Agentic AI Bootcamp · atomcamp                   ║
╚══════════════════════════════════════════════════════════╝

 Capabilities auto-routed from your input:
  ✉️  Email    → "Write email about..."
  📝 Summarize → "Summarize: <text>"
  💬 Chat      → anything else (has memory!)

 Commands:
  help        → show this menu
  clear       → clear chat memory
  exit / quit → exit the program
"""

HELP_TEXT = """
┌─────────────────────────────────────────────────────────┐
│  CAPABILITIES                                           │
│  ✉️  Email Writer   → "Write a formal email to my prof  │
│                       about missing class"              │
│  📝 Summarizer     → "Summarize: <paste any text>"      │
│                       Add 'short' or 'long' for length  │
│  💬 Chat + Memory  → Any question (uses tools auto!)    │
│                                                         │
│  TOOLS (auto-used by the model)                         │
│  🧮 Calculator     → math expressions                   │
│  🔍 Web Search     → factual / research questions       │
│  📊 Data Analyzer  → "analyze 10, 20, 30, 40"           │
│  🕐 Time Info      → "what time is it in EST?"          │
│                                                         │
│  COMMANDS                                               │
│  help | clear | exit                                    │
└─────────────────────────────────────────────────────────┘
"""


def main():
    print(BANNER)
    try:
        assistant = MultiCapabilityAssistant()
    except EnvironmentError as e:
        print(f"❌  Setup error: {e}")
        return

    while True:
        try:
            user_input = input("\n You → ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋  Goodbye!")
            break

        if not user_input:
            print("  ⚠️  Please enter something.")
            continue

        cmd = user_input.lower()
        if cmd in ("exit", "quit", "bye"):
            print("👋  Goodbye!")
            break
        if cmd == "help":
            print(HELP_TEXT)
            continue
        if cmd == "clear":
            assistant.clear_memory()
            print("  🗑️  Chat memory cleared.")
            continue

        print("\n  🤔  Thinking...\n")
        try:
            response = assistant.process(user_input)
            print(f"  Assistant →\n{response}\n")
            print("─" * 60)
        except Exception as e:
            print(f"  ❌  Error: {e}")
            print("  Please try again or type 'help'.")


if __name__ == "__main__":
    main()
