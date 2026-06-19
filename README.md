<<<<<<< HEAD
#  Multi-Capability AI Assistant
=======
# 🤖 Multi-Capability AI Assistant
>>>>>>> 2bed40a808f3ef7387cdeff36f728101e0f20c34

**Agentic AI Bootcamp · atomcamp | Session 2 Assignment**  
*Built by Khansa Shakeel Ahmed — AI Engineer & Lab Instructor*

---

## What It Does

A single Python program that intelligently routes your natural language input to one of three AI-powered capabilities, backed by four working tools — all in an agentic loop where the model decides when and which tools to call.

---

## Capabilities

### ✉️ 1. Enhanced Email Writer
- Drafts complete emails with Subject line, greeting, body, and closing
- Supports **formal**, **friendly**, and **casual** tones
- Uses **web search** to research the topic before writing when needed
- Trigger: *"Write email about..."* or *"Draft a formal email to..."*

### 📝 2. Smart Summarizer (with Analytics)
- Accepts any pasted multi-line text
- Generates summaries in **short / medium / long** lengths
- Shows **word count reduction stats** and **key themes**
- Trigger: *"Summarize: <text>"* or *"TL;DR: <text>"*

### 💬 3. Chat Assistant (with Memory)
- Maintains full **conversation history** across turns
- Answers follow-up questions using prior context
- Automatically calls tools (calculator, search, etc.) as needed
- Trigger: anything that isn't email or summarize

---

## Tools (Auto-Used by the Model)

| Tool | What It Does |
|------|-------------|
| 🧮 **Calculator** | Evaluates math expressions — percentages, powers, sqrt, etc. |
| 🔍 **Web Search** | Searches for factual/current information (mock database) |
| 📊 **Data Analyzer** | Stats on number lists: sum, mean, max, min, median, std |
| 🕐 **Time Info** | Current date/time in any supported timezone (PKT, UTC, EST, IST…) |

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/multi-capability-assistant.git
cd multi-capability-assistant

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API key
cp .env.example .env
# Edit .env and add your OpenAI API key
```

---

## Usage

```bash
python assistant.py
```

Type your request and press Enter. The assistant auto-routes based on intent.

---

## Example Interactions

### Email
```
You → Write a formal email to my professor requesting a deadline extension for the assignment

Assistant →
Subject: Request for Assignment Deadline Extension

Dear Professor,

I hope this message finds you well...
```

### Summarizer
```
You → Summarize: Artificial intelligence (AI) is intelligence demonstrated by machines...
      [paste any long text]

Assistant →
SUMMARY
AI encompasses machine-demonstrated intelligence that enables...

ANALYTICS
Original: 312 words | Summary: 48 words | Reduction: 84.6%

KEY THEMES
• Machine learning and neural networks
• Real-world applications
• Ethical considerations
```

### Chat + Calculator tool
```
You → If I invest 50,000 PKR at 12% annual return for 3 years, what do I get?

Assistant → [uses calculate tool automatically]
Your investment of 50,000 PKR at 12% annual return for 3 years:
Compound amount = 50,000 × (1.12)³ = 70,246.40 PKR
Profit = 20,246.40 PKR
```

### Data Analyzer
```
You → Analyze these scores: 78, 85, 92, 67, 88, 74, 95

Assistant → [uses analyze_data tool automatically]
Statistical Analysis of your 7 scores:
• Mean: 82.71  • Median: 85  • Std Dev: 9.86
• Min: 67  • Max: 95  • Sum: 579
```

### Time Tool
```
You → What time is it right now in Pakistan?

Assistant → [uses get_time_info tool]
Current time in PKT: 03:45 PM — Tuesday, June 10, 2025
```

---

## Project Structure

```
multi-capability-assistant/
├── assistant.py       ← Main program (all capabilities + tools)
├── README.md          ← This file
├── requirements.txt   ← Dependencies
├── .env.example       ← API key template
└── examples.txt       ← Sample interactions log
```

---

## Design Decisions

- **Agentic loop**: The model calls tools autonomously in up to 5 turns — no hard-coded routing to tools
- **Smart router**: Intent detection via keyword signals before hitting the LLM, saving tokens
- **Safe calculator**: Uses `eval()` with a sanitised namespace — no arbitrary code execution
- **Separation of concerns**: Each capability has its own system prompt for focused behaviour
