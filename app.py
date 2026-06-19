"""
Gradio UI — Multi-Capability AI Assistant
Agentic AI Bootcamp · atomcamp
"""

import gradio as gr
from assistant import MultiCapabilityAssistant

# ── One shared assistant instance (Groq/OpenAI client is stateless per call)
# Chat memory is passed via Gradio State, so each browser session is isolated.
assistant = MultiCapabilityAssistant()

# ──────────────────────────────────────────────
#  CAPABILITY HANDLERS
# ──────────────────────────────────────────────

def run_capability(capability: str, user_input: str, tone: str, chat_history: list):
    """Route to the selected capability and return output + updated chat history."""

    if not user_input.strip():
        return "⚠️  Please enter some text.", chat_history

    if capability == "✉️  Email Writer":
        result = assistant.write_email(user_input, tone=tone.lower())
        return result, chat_history

    elif capability == "📝  Summarizer":
        length = "short" if "short" in user_input.lower() else (
            "long" if "long" in user_input.lower() else "medium"
        )
        result = assistant.summarize(user_input, length=length)
        return result, chat_history

    elif capability == "💬  Chat Assistant":
        # Restore history into assistant for this session
        assistant.chat_history = chat_history.copy()
        result = assistant.chat(user_input)
        updated_history = assistant.chat_history.copy()
        return result, updated_history

    return "Unknown capability selected.", chat_history


def clear_chat(chat_history):
    assistant.chat_history = []
    return "", []


# ──────────────────────────────────────────────
#  UI LAYOUT
# ──────────────────────────────────────────────

CSS = """
/* ── Root tokens ── */
:root {
    --bg:        #0f1117;
    --surface:   #1a1d27;
    --border:    #2a2d3e;
    --accent:    #7c6af7;
    --accent-2:  #a78bfa;
    --text:      #e2e4f0;
    --muted:     #8b8fa8;
    --radius:    12px;
    --font:      'Inter', system-ui, sans-serif;
}

/* ── Base ── */
body, .gradio-container {
    background: var(--bg) !important;
    font-family: var(--font) !important;
    color: var(--text) !important;
}

/* ── Header ── */
.assistant-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.assistant-header h1 {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.02em;
    margin: 0 0 0.25rem;
}
.assistant-header p {
    color: var(--muted);
    font-size: 0.875rem;
    margin: 0;
}
.accent { color: var(--accent-2); }

/* ── Cards / panels ── */
.gr-panel, .gr-box, .gradio-group {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}

/* ── Inputs ── */
textarea, input[type="text"], select, .gr-dropdown {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: var(--font) !important;
    font-size: 0.9rem !important;
}
textarea:focus, input:focus {
    border-color: var(--accent) !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(124,106,247,0.2) !important;
}

/* ── Labels ── */
label span, .gr-form label {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

/* ── Buttons ── */
.gr-button-primary {
    background: var(--accent) !important;
    border: none !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: opacity 0.15s !important;
}
.gr-button-primary:hover { opacity: 0.85 !important; }

.gr-button-secondary {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-size: 0.85rem !important;
}
.gr-button-secondary:hover {
    border-color: var(--accent) !important;
    color: var(--accent-2) !important;
}

/* ── Output box ── */
.output-box textarea {
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    font-size: 0.85rem !important;
    line-height: 1.6 !important;
    min-height: 280px !important;
}

/* ── Capability pills (dropdown options) ── */
.capability-note {
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 0.4rem;
    line-height: 1.5;
}
"""

CAPABILITY_NOTES = {
    "✉️  Email Writer":  "Describe the email you need. Optionally add 'formal', 'friendly', or 'casual' in your text.",
    "📝  Summarizer":    "Paste any text to summarize. Add 'short' or 'long' to control summary length.",
    "💬  Chat Assistant": "Ask anything. The assistant remembers your conversation. Use 'Clear Memory' to reset.",
}

def update_note(capability):
    return CAPABILITY_NOTES.get(capability, "")

def update_tone_visibility(capability):
    return gr.update(visible=(capability == "✉️  Email Writer"))


with gr.Blocks(title="Multi-Capability AI Assistant") as demo:

    # ── State
    chat_history_state = gr.State([])

    # ── Header
    gr.HTML("""
    <div class="assistant-header">
        <h1>🤖 Multi-Capability <span class="accent">AI Assistant</span></h1>
        <p>Agentic AI Bootcamp &nbsp;·&nbsp; atomcamp &nbsp;·&nbsp; Session 2</p>
    </div>
    """)

    with gr.Row():
        # ── Left column: controls
        with gr.Column(scale=1, min_width=240):

            capability = gr.Dropdown(
                choices=["✉️  Email Writer", "📝  Summarizer", "💬  Chat Assistant"],
                value="💬  Chat Assistant",
                label="Capability",
                interactive=True,
            )

            tone = gr.Dropdown(
                choices=["Formal", "Friendly", "Casual"],
                value="Formal",
                label="Email Tone",
                visible=False,
                interactive=True,
            )

            capability_note = gr.Markdown(
                value=CAPABILITY_NOTES["💬  Chat Assistant"],
                elem_classes=["capability-note"],
            )

            gr.HTML("<div style='margin-top:1rem'></div>")

            submit_btn = gr.Button("Run ▶", variant="primary")
            clear_btn = gr.Button("Clear Memory", variant="secondary")

        # ── Right column: input + output
        with gr.Column(scale=2):

            user_input = gr.Textbox(
                label="Your Input",
                placeholder="Type your request here…",
                lines=4,
            )

            output = gr.Textbox(
            label="Assistant Output",
            lines=12,
            interactive=False,
            elem_classes=["output-box"],
)

    # ── Wiring
    capability.change(
        fn=update_note,
        inputs=capability,
        outputs=capability_note,
    )
    capability.change(
        fn=update_tone_visibility,
        inputs=capability,
        outputs=tone,
    )
    submit_btn.click(
        fn=run_capability,
        inputs=[capability, user_input, tone, chat_history_state],
        outputs=[output, chat_history_state],
    )
    user_input.submit(
        fn=run_capability,
        inputs=[capability, user_input, tone, chat_history_state],
        outputs=[output, chat_history_state],
    )
    clear_btn.click(
        fn=clear_chat,
        inputs=[chat_history_state],
        outputs=[output, chat_history_state],
    )

if __name__ == "__main__":
    demo.launch(css=CSS)
