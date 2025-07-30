# pajaMAS

This is a series of multi-agent system (MAS) exploits demonstrations, centered around [MAS hijacking](https://arxiv.org/abs/2503.12188) (attacks that manipulate the control flow of a MAS). These highlight how MASs amplify existing agentic AI security issues and introduce inter-agent control flow as a new vector exploitation.

![mas_demo](https://github.com/user-attachments/assets/f3a393dc-a11d-479e-946f-dbab4f8eb85d)

**Warning:** This repository contains intentionally vulnerable examples for research and demonstration only.

**Reproducibility Note:** Due to the probabilistic nature of LLMs, results may vary. For consistent evaluation, run each example 5 times.

- `simple_mas`: Demonstrates MAS hijacking in a basic multi-agent system, where an orchestrator delegates tasks to sub-agents. Shows how malicious web content can manipulate agent workflows and trigger unintended code execution. Includes 7 hijacking examples.
- `tool_mas`: Shows MAS hijacking using a malicious tool.
- `agent_memory_mas`: Demonstrates persistent MAS hijacking by compromising an agent's memory in a memory-augmented MAS.
- `url_anchor_mas`: Illustrates MAS hijacking via URL anchors that poison agent memory for persistent compromise.
- `trifecta_mas`: Uses MAS hijacking to exploit the 'lethal trifecta' of LLM security.
- `cycle_mas`: Exploits unintended cycles in a MAS using MAS hijacking.
- `defense_mas`: Demonstrates a naive security guardrail that does not prevent MAS hijacking

## Setup

To set up the environment, use uv:

1. **Install uv** (if you don't have it):

   ```bash
   pip install uv
   # or
   curl -Ls https://astral.sh/uv/install.sh | sh
   ```

2. **Create a virtual environment and install dependencies:**

   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

## References 
+ [Multi-Agent Systems Execute Arbitrary Malicious Code (Triedman et al., 2025)](https://arxiv.org/abs/2503.12188)

## 
*A wise man once said "Hijacking a MAS is so easy: you can do it in your pajaMAS."*
