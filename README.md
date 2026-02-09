# 🧠 Lecture Brain

A modular educational content processing system built with a **Core + Plugins** architecture.

This project is designed to be **scalable, maintainable, and framework-agnostic**, allowing us to add new features without modifying the core logic.

---

## 📌 Project Vision

Lecture Brain processes educational content (lectures, texts, files, etc.) through:

- **Sources** → fetch content
- **Actions** → process content (summaries, explanations, quizzes, etc.)

All logic lives in a **Core** layer, while features are added as **Plugins**.

---

## 🏗️ Architecture Overview

Frontend / User
↓
API (FastAPI) ← Phase 3
↓
Core
┌───────────────┐
│ Registry │
│ Interfaces │
│ Models │
└───────────────┘
↓
Plugins
┌───────────────┐
│ Sources │
│ Actions │
└───────────────┘


---

## 📂 Project Structure

lecture-brain/
│
├─ app/
│ ├─ core/
│ │ ├─ models.py # Core entities (LectureBrain, Knowledge)
│ │ ├─ interfaces.py # Base interfaces for plugins
│ │ ├─ registry.py # Plugin registration & retrieval
│ │
│ ├─ core/plugins_example.py
│ # Example plugins for testing
│
├─ README.md


---

## 🧩 Core Concept

### Core
The Core:
- Contains business logic only
- Has NO dependency on FastAPI, frontend, or database
- Manages plugins and execution flow

> The Core should rarely change.

---

### Plugins
Plugins are the extensibility mechanism.

#### 🔹 Sources
Responsible for fetching data.

Examples:
- Text files
- PDFs
- YouTube transcripts
- Databases

```python
source.fetch(input_data)
🔹 Actions
Responsible for processing data.

Examples:

Summarization

Explanation

Quiz generation

Search

action.run(lecture, options)
📜 Interfaces (interfaces.py)
Interfaces define contracts that all plugins must follow.

This ensures:

Consistent behavior

Safe extension

Team collaboration without conflicts

If a plugin does not follow the interface, it will fail at runtime.

🧠 Plugin Registry
The PluginRegistry:

Registers all available plugins

Retrieves plugins by name, not by class

Example:

registry.register_source(TextSource)
registry.register_action(SummaryAction)

source = registry.get_source("text")
action = registry.get_action("summary")
This keeps the system flexible and decoupled.

▶️ How to Run (Current Phase)
1️⃣ Activate the environment
conda activate GP
2️⃣ Run Python shell
python
3️⃣ Test the Core manually
from app.core.registry import PluginRegistry
from app.core.plugins_example import TextSource, SummaryAction
from app.core.models import LectureBrain, Knowledge

registry = PluginRegistry()
registry.register_source(TextSource)
registry.register_action(SummaryAction)

source = registry.get_source("text")
print(source.fetch("example.txt"))

lecture = LectureBrain("l1", "Algebra")
lecture.add_knowledge(Knowledge("Important algebra point"))

action = registry.get_action("summary")
print(action.run(lecture, {}))
🛠️ Development Phases
✅ Phase 1 – Core Foundation
Core models

Interfaces

Plugin registry

Manual testing

🚧 Phase 2 – Plugin Expansion
More sources

More actions

Real use cases

🔜 Phase 3 – API Layer
FastAPI endpoints

Frontend integration

External usage

🤝 Team Workflow Rules
Any new feature = Plugin

Avoid modifying Core without discussion

Follow interfaces strictly

Keep plugins independent

📌 Notes
The Core will not be rewritten when adding FastAPI

API will act as a thin layer on top of the Core

This structure is designed for long-term scalability
