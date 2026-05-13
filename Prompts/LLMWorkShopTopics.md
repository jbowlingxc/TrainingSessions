# LLM Workshop Topics: Local LLM Management for IT Professionals

This document outlines the core subjects for a series of presentations designed to guide IT professionals through the setup, management, and extension of local Large Language Models (LLMs). While the audience may have used cloud-based AI, these topics assume no prior deep knowledge of local LLM architecture and operations.

## 1. LLM Essentials
*Goal: Demystify the core mechanics of LLMs by comparing local setups with cloud offerings. Use LMStudio for practical demonstrations.*

- **Introduction to LLMs**: What is a Large Language Model? How does it differ from traditional software?
- **The Inference Server**: Understanding the role of the inference server in hosting and serving models locally.
- **Model Types**: Detailed look at specialized models:
    - **Instruct**: Optimized for following directions.
    - **Reasoning**: Specialized for complex problem solving and chain-of-thought.
    - **Tools/Function Calling**: Models capable of interacting with external systems.
    - **Embedding**: Models used for converting text to vectors for search and RAG.
- **Model Landscape**: Comparison of leading open-weights models (e.g., Llama, Mistral, Phi, DeepSeek), including their purpose, backing organizations, and release timelines.
- **Fundamental Constraints**: Understanding LLM limitations, including training data cut-offs and the inability to "think" or "act" without external tools.
- **Model Architecture**:
    - **Parameters & Knowledge Depth**: What parameters are and how they relate to the model's capability and training bias.
    - **Quantization**: Explaining the process of reducing model precision to fit on consumer hardware and its impact on performance vs. accuracy.
- **Configuration & Tuning**:
    - **Temperature & Top-P**: How these settings control randomness and creativity.
    - **Context Window**: Understanding context size, its impact on memory (VRAM), and strategies for managing long conversations.

## 2. Hardware & Infrastructure
*Goal: Provide a technical blueprint for deploying local LLMs.*

- **Compute Requirements**: GPU vs. CPU inference; the critical role of VRAM (Video RAM) and system RAM.
- **Hardware Bottlenecks**: Understanding memory bandwidth and how it affects tokens-per-second (TPS).
- **Deployment Tools**: Comparing local hosting solutions:
    - **LMStudio**: For easy exploration and testing.
    - **Ollama**: For streamlined CLI-based management and API serving.
    - **vLLM / LocalAI**: For production-grade, high-throughput serving.

## 3. Extending LLM Capabilities
*Goal: Move from a simple chat interface to a functional AI system.*

- **Model Context Protocol (MCP)**: Introduction to the standard for connecting LLMs to external data sources and tools.
- **Tool Use & Skills**: 
    - Defining function schemas.
    - Handling the tool-call loop (Request -> Call -> Response -> Final Answer).
    - Implementing "skills" for autonomous task execution.
- **Retrieval Augmented Generation (RAG)**: 
    - The concept of grounding LLMs in private data.
    - Vector databases and the retrieval pipeline.
- **Orchestration Frameworks**: Using tools like LangChain, AutoGPT, or custom scripts to manage complex workflows and skill chains.

## 4. Security & Governance
*Goal: Ensure the safe deployment of AI extensions in an enterprise environment.*

- **Security Validation**: Methods for auditing and validating the security of skills and MCP servers downloaded from the internet.
- **MCP Gateways**: Implementing a gateway layer for access control, request filtering, and auditing of tool calls.
- **Governance Frameworks**: Establishing policies for third-party extension approval and data privacy boundaries.
- **Sandboxing**: Running untrusted tools/skills in isolated environments to prevent system compromise.

## 5. Interfaces & User Experience
*Goal: Bridging the gap between technical infrastructure and end-user utility.*

- **Agentic Harnesses**: Comparing different agent implementations (e.g., OpenCode, Claude) and how they manage state and tool execution.
- **User-Centric Design**: Creating simplified chat interfaces that allow non-technical users to leverage complex local LLM capabilities without needing to understand the underlying prompts or parameters.
- **Evaluation & Benchmarking**: How to objectively measure the performance, accuracy, and safety of a local setup using benchmarks.
