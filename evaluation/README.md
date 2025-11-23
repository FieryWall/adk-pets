# Simple Web UI Evaluation

## Structure
```
evaluation/
└── agents/
    ├── guidance_writer_agent/
    │   ├── __init__.py                           # Agent definition
    │   └── guidance_writer_tests.evalset.json   # Test cases
    └── guidance_reviewer_agent/
        ├── __init__.py                           # Agent definition  
        └── guidance_reviewer_tests.evalset.json # Test cases
```

## Usage

### Start Web UI
```bash
adk web evaluation/agents --port 8002
```

### Test Your Agents
1. Open http://localhost:8002
2. Select an agent
3. Run test cases from the Eval tab
4. Chat interactively to create new test cases

### Add New Test Cases
Edit the `.evalset.json` files directly:
- `evaluation/agents/guidance_writer_agent/guidance_writer_tests.evalset.json`
- `evaluation/agents/guidance_reviewer_agent/guidance_reviewer_tests.evalset.json`

## Simple and Clean! ✨