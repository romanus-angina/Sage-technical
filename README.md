# AI Therapy Evaluation System

An automated system for evaluating AI-powered therapy conversations using simulated clients and comprehensive scoring metrics.  This system provides a robust framework for assessing the quality and effectiveness of AI therapists by simulating diverse client interactions and applying evidence-based evaluation criteria.

## Features

* **Diverse Client Personas:** 10 realistic client simulations representing various mental health presentations and communication styles.
* **Evidence-Based AI Therapist:**  The system utilizes an AI therapist model incorporating principles of CBT, person-centered therapy, and trauma-informed care.  (Note: Currently configured to simulate a *poor* therapist for testing purposes.)
* **Comprehensive Evaluation:** Multi-dimensional scoring encompassing empathy, validation, question quality, supportive tone, and therapeutic alliance.
* **Parallel Processing:** Efficient asynchronous execution enables the simultaneous evaluation of multiple therapy conversations.
* **Detailed Analytics:**  Generates summary statistics and detailed breakdowns of therapeutic quality for each conversation and across the entire evaluation set.
* **Flexible Configuration:**  Easily customizable parameters for the number of conversations, OpenAI API key, and other system settings.
* **Transcript Generation:**  Detailed transcripts of each conversation are generated for review and analysis.
* **Results Saving:** Evaluation results, including transcripts, scores, and timestamps are saved in JSON format.


## Usage

The system is primarily run via the command-line interface (CLI).  The `run_demo.sh` script provides a quick demonstration. For more comprehensive evaluations, use the following command structure:


```bash
python -m src.main [OPTIONS]
```

**Options:**

* `--conversations <number>`: Specifies the number of simulated therapy conversations (default: 10).
* `--verbose`: Enables verbose output, showing detailed results for each conversation.
* `--no-save`: Prevents saving results to a JSON file.
* `--show-transcript <conversation_number>`: Displays the full transcript for a specific conversation.

**Example Commands:**

* Run a default evaluation with 10 conversations:  `python -m src.main`
* Run an evaluation with 5 conversations and verbose output: `python -m src.main --conversations 5 --verbose`
* Run an evaluation and suppress result saving: `python -m src.main --no-save`
* Display transcript for conversation 3: `python -m src.main --conversations 3 --show-transcript 3`


## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd therapy-eval-system
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and provide your OpenAI API key if necessary. The default key from `.env.example` is used if not specified.


## Technologies Used

* **Python:** The primary programming language for the entire system.
* **OpenAI API:** Used for generating client responses and therapist interactions, leveraging the power of large language models.  Specifically, the `gpt-4.1-mini-2025-04-14` model is used (configurable).
* **asyncio:** Enables asynchronous operations for parallel processing of conversations.
* **click:**  Used to create the command-line interface.
* **tabulate:** Used for formatting the output of the evaluation results.
* **dotenv:**  Handles environment variable loading from a `.env` file.
* **dataclasses:** Used for creating data structures for the evaluation scores and client personas.
* **pytest:** Used for testing purposes.

## Statistical Analysis

The system calculates several key metrics for each conversation and provides summary statistics including averages.  The scoring rubric combines quantitative and qualitative assessments.  Averages are computed for the overall score and for individual dimensions (empathy, validation, question quality, supportive tone, and therapeutic alliance).

## Configuration

The system configuration is managed through the `src/config.py` file and environment variables.  Key settings include:

* `OPENAI_API_KEY`: Your OpenAI API key (required).
* `MODEL`: The OpenAI model to use (default: `gpt-4.1-mini-2025-04-14`).
* `CONVERSATION_TURNS`: The number of turns per conversation.
* `MAX_CONCURRENT_CONVERSATIONS`:  The maximum number of conversations to run concurrently.
* `RESULTS_DIR`: The directory where evaluation results are saved.


## Dependencies

The project dependencies are listed in the `requirements.txt` file.  These can be installed using `pip install -r requirements.txt`.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.


## Testing

Unit tests are provided using `pytest`. To run the tests:

```bash
pytest tests/
```



*README.md was made with [Etchr](https://etchr.dev)*