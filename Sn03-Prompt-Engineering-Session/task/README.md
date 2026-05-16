### 📋 Trainee Handout: Prompt Engineering Lab

**Objective:** Master the art of directing Large Language Models (LLMs) through precise prompt engineering. You will complete three levels of increasing complexity.

**Provided Infrastructure:**
You will use the provided `OpenAIAgent` class to interact with the LLM. Note that the bot takes your `system_prompt` and `template_prompt` as constructor parameters. Your `template_prompt` should include the `{query}` placeholder where the dynamic input will go.
* Use `nonstream_chat(query)` for tasks requiring a complete, structured output (like JSON or short classifications).
* Use `stream_chat(query)` for tasks generating longer text where reading in real-time is beneficial.

**Important Setup Step:**
1. Install the required Python libraries:
```bash
pip install openai python-dotenv
```

2. Before running any code, you must create a `.env` file in the root of this task directory with the following content:
```env
OPENAI_API_KEY=""
OPENAI_CHAT_MODEL="gpt-5.2"
```
*Note: Place the API key that will be provided to you by the instructor inside the quotes.*

***Note:** You MUST NOT use any LLM in that task, do it by yourself. In case of stumble, contact the instructor.*

---

#### 🟢 Level 1: The Strict Classifier (Single Agent)
**Goal:** Write a system prompt that turns the LLM into a rigid intent classifier for a regional business portal. 

**Task:**
Create a prompt that reads a user's input and classifies it into exactly one of three categories:
1.  `BUSINESS_SERVICE`: Queries related to setting up, managing, or utilizing company services.
2.  `GENERAL_INQUIRY`: Broad questions about hours, locations, or public information.
3.  `UNKNOWN`: Anything else, including gibberish or off-topic requests.

**Constraint:** The LLM must output *only* the category name. No explanations, no pleasantries.

**Implementation Example:**
```python
query = "I need to renew my commercial license."
# TODO: Construct your agent by providing the system prompt and template prompt
# system_prompt = "..."
# template_prompt = "...\n\nUser Input: {query}"
# bot = OpenAIAgent(system_prompt, template_prompt)

response = bot.nonstream_chat(query)
print(response) # Expected output: BUSINESS_SERVICE
```

---

#### 🟡 Level 2: The Structured Extractor (Single Agent, Strict Format)
**Goal:** Force the LLM to extract specific information from a noisy text (like a raw OCR scan or audio transcription) and format it strictly as JSON.

**Task:**
Write a prompt that extracts the following entities from a provided text block: `Company Name`, `Filing Date`, and `Status` (Active/Inactive). 
* If a piece of information is missing from the text, the value must be explicitly set to `null`.
* The output must be raw, valid JSON. Do not wrap it in markdown code blocks (e.g., no \`\`\`json).

**Implementation Example:**
```python
query = "Um, yeah, we registered Apex Dynamics on... I think it was March 14th, 2023. We are currently fully operational."
# TODO: Construct your agent using a system prompt and a template prompt
# system_prompt = "..."
# template_prompt = "...\n\nText: {query}"
# bot = OpenAIAgent(system_prompt, template_prompt)

response = bot.nonstream_chat(query)
# We should be able to parse your response directly:
# import json; data = json.loads(response)
```

---

#### 🔴 Level 3: The Advisory Pipeline (Multi-Agent)
**Goal:** Build a pipeline where the output of Agent A serves as the strict input for Agent B.

**Task:**
You are building an automated advisory system.
* **Agent A (The Analyst):** Write a prompt that reads a user's complex administrative problem and outputs *only* a bulleted list of the core legal/business requirements needed to solve it. 
* **Agent B (The Advisor):** Write a prompt that takes Agent A's bulleted list and drafts a polite, formal, and empathetic email to the user explaining their next steps. 

**Implementation Example:**
```python
query = "I want to open a branch of my tech startup in the new administrative zone, but I don't know what permits I need for foreign workers."

# 1. Initialize Agents
# agent_a = OpenAIAgent(analyst_system_prompt, analyst_template_prompt)
# agent_b = OpenAIAgent(advisor_system_prompt, advisor_template_prompt)

# 2. Call Agent A
requirements_list = agent_a.nonstream_chat(query)

# 3. Call Agent B using Agent A's output as the query
print("Drafting response...")
for chunk in agent_b.stream_chat(requirements_list):
    print(chunk, end="", flush=True)
```
