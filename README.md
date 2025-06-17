# "JiuRu-ShanHai" - A Social Science Research Innovation Scheme Driven by Large Models

The "JiuRu-ShanHai" project is dedicated to establishing a large model-driven social science innovative research platform, enabling closed-loop automated scientific research. The project focuses on the current transition in scientific research from human-driven to AI-assisted, ultimately achieving full automation. Through a multi-agent collaborative workflow driven by multimodal large models, the project realizes full automation of the entire research process, from inputting research topics to generating creativity, revising frameworks, collecting data, analyzing results, and writing papers

## System Components

### Main Agents
1. PhD Agent
   - Focuses on research framework development
   - Uses multi-round thinking chains
   - Integrates feedback from Dr Agents
   - Ensures logical and innovative framework

2. Dr Agents (2)
   - Analyze current research status
   - Identify research gaps and opportunities
   - Evaluate research methods
   - Provide theoretical contribution suggestions

3. Writer Agent
   - Integrates research framework, data, and results
   - Uses hierarchical writing approach
   - Ensures precision and clarity
   - Maintains academic writing standards

4. Evaluator Agent
   - Uses multi-dimensional evaluation system
   - Ensures paper reliability and innovation
   - Provides specific improvement suggestions
   - Assesses academic value

### Auxiliary Modules
1. Knowledge Acquisition Module
   - Searches for relevant papers
   - Consults with LLM for information
   - Maintains research database

2. Thesis Evaluation Module
   - Evaluates thesis quality
   - Provides modification suggestions
   - Ensures academic standards

## System Workflow

1. Research Framework Development
   - Dr Agents analyze research status
   - PhD Agent develops framework
   - Multi-round feedback and revision

2. Research Execution
   - Literature review
   - Data collection
   - Progress reporting

3. Paper Writing
   - Writer Agent integrates content
   - Hierarchical writing approach
   - Quality assurance

4. Paper Evaluation
   - Multi-dimensional evaluation
   - Reliability assessment
   - Innovation verification
   - Improvement suggestions

5. Final Publication
   - Final review
   - Journal selection
   - Format adjustment

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with your API key:
```
DASHSCOPE_API_KEY=your_api_key_here
```

3. Run the system:
```bash
python main.py
```

## Project Structure

```
.
├── agents/
│   ├── __init__.py
│   ├── phd_agent.py
│   ├── dr_agent.py
│   ├── writer_agent.py
│   └── evaluator_agent.py
├── modules/
│   ├── __init__.py
│   ├── knowledge_acquisition.py
│   └── thesis_evaluation.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── main.py
├── requirements.txt
└── README.md
``` 
