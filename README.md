# AI Food Waste Reduction Assistant

A Streamlit prototype for the 1M1B AI for Sustainability Virtual Internship.

## SDG Alignment
- **Primary:** SDG 12 — Responsible Consumption and Production
- **Additional:** SDG 2 — Zero Hunger; SDG 13 — Climate Action

## What the prototype does
- Maintains a simple food inventory
- Prioritizes selected perishable foods for "Use Soon"
- Generates simple meal ideas from available ingredients
- Retrieves storage/sustainability tips from a small local knowledge base
- Demonstrates an Agentic AI-style workflow
- Includes an image-upload extension point for future computer vision

## AI Concepts Demonstrated
- Generative AI concept
- RAG (local knowledge retrieval demonstration)
- Agentic AI workflow
- NLP / recommendation logic
- Optional computer vision extension

## Run locally

1. Install Python 3.10+.
2. Open a terminal in this project folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the app:

```bash
streamlit run app.py
```

The browser will open the local Streamlit application.

## IBM Granite integration

This package intentionally runs without API credentials so it is easy to demo. For a production version, the recommendation layer can be connected to an IBM Granite endpoint/API and the local knowledge base can be replaced by a larger, validated RAG knowledge source.

Do not add API keys to GitHub. Store secrets in environment variables or Streamlit secrets.

## Suggested demo

1. Start the app.
2. Show the initial food inventory.
3. Click **Analyze My Food**.
4. Show the "Use Soon" items.
5. Show the generated meal idea.
6. Explain the RAG-style retrieved guidance.
7. Add another food item and analyze again.
8. Upload a sample food image to demonstrate the future computer-vision extension.

## Important limitation

This is an educational prototype, not a food-safety authority. Users should follow product labels and appropriate official food-safety guidance. Prototype metrics are not claims of real-world impact.
