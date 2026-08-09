Tamazight Corpus Framework
A Python framework for building, managing, and validating low-resource Tamazight speech corpora, initially focused on Kabyle and automatic speech recognition (ASR).

The project provides a structured way to collect speech recordings together with speaker information, transcripts, audio metadata, corpus configuration, statistics, and validation results.

The long-term goal is to make low-resource speech-corpus creation accessible to researchers, developers, and eventually non-programmers through a web application.

Project status
Active research and development

The core corpus framework is currently functional and can be used through a command-line interface (CLI).

Currently available
Corpus initialization
Speaker management
Audio recording
Transcript collection
Recording metadata
File-based repositories
Corpus statistics
Corpus validation
Command-line interface
Automated tests
Example scripts
Python package structure
Reproducible development environment using uv
In development
Flask web application
Browser-based corpus management
Easier speech-data collection
Expanded corpus validation
ASR dataset preparation
Future
Larger Kabyle speech corpus
Public dataset release
Kabyle ASR experiments
CPU-friendly ASR approaches
Hugging Face dataset
ASR model
Research publications
Motivation
Kabyle (Tamazight) is a relatively low-resource language in modern speech and language technology.

Building an automatic speech recognition system requires speech data that is not only large enough, but also properly organized.

A useful speech corpus needs:

audio recordings
accurate transcripts
speaker information
recording identifiers
audio metadata
corpus configuration
quality control
validation
reproducible organization
This project provides a framework for managing these components systematically.

The broader research objective is to contribute reusable tools and resources for Kabyle/Tamazight language technology.

Who is this framework for?
Researchers
Researchers can use the framework to:

create speech corpora
organize speakers
record speech
collect transcripts
maintain metadata
calculate corpus statistics
validate corpus files
prepare data for ASR research
reproduce corpus construction procedures
The framework is particularly intended for researchers working with low-resource languages.

Developers
Developers can use the framework as a foundation for:

speech-data collection applications
corpus-management systems
ASR data pipelines
command-line tools
web applications
research software
The corpus framework is separated from its user interface so that different interfaces can be built on top of the same core functionality.

Currently the main interface is the CLI.

A Flask web interface is planned.

Speech-data collectors
The current version requires use of the command line.

The planned web application will make the framework easier to use for people who do not have Python or command-line experience.

The planned workflow is:

Select speaker
      ↓
Record speech
      ↓
Enter transcript
      ↓
Save recording
      ↓
Review data
Architecture
The framework separates the main concepts of a corpus.

Corpus
 │
 ├── Speakers
 │
 └── Recordings
       │
       ├── Audio
       ├── Transcript
       └── Metadata
A recording belongs to a speaker and has a corresponding audio file and transcript.

For example:

SPK001
   │
   └── Recording 000001
          ├── 000001.wav
          └── 000001.txt
This relationship is important for ASR research because the audio and its transcription must remain correctly associated.

Current corpus format
After initializing a corpus and recording an utterance, the framework produces a structure similar to:

kabyle_dataset/
│
├── corpus.yaml
│
├── audio/
│   └── 000001.wav
│
├── transcripts/
│   └── 000001.txt
│
└── metadata/
    ├── speakers.csv
    └── recordings.csv
Corpus configuration
The corpus.yaml file describes the corpus.

Example:

name: Test Corpus
language: kabyle
sample_rate: 16000
channels: 1
audio_directory: audio
transcript_directory: transcripts
metadata_directory: metadata
The current recording configuration uses:

Language: Kabyle
Sample rate: 16,000 Hz
Channels: 1 (mono)
The configuration also specifies where audio, transcripts, and metadata are stored.

Speaker metadata
Speaker information is stored in:

metadata/speakers.csv
Example:

id,name
SPK001,Test Speaker
Each speaker receives a unique identifier.

For example:

SPK001
SPK002
SPK003
Speaker identifiers are important for organizing recordings and for future speaker-independent training and evaluation.

Recording metadata
Recording information is stored in:

metadata/recordings.csv
Example:

id,speaker,audio,transcript,sample_rate,channels,duration
1,SPK001,000001.wav,000001.txt,16000,1,5
The recording metadata connects:

Speaker
   ↓
Recording
   ↓
Audio + Transcript
It also records:

recording ID
speaker ID
audio filename
transcript filename
sample rate
number of channels
duration
This makes the corpus suitable for later processing and ASR dataset preparation.

Transcripts
Each recording has a corresponding transcript file.

For example:

audio/000001.wav
transcripts/000001.txt
The filenames use the same recording identifier.

This makes the audio/transcript relationship easy to maintain.

Installation
The following instructions start from a clean computer.

The current project requires:

Python 3.13 or newer
Git
uv
a working microphone for recording
internet access during installation
The framework is currently developed primarily on Windows.

1. Install Python
Check whether Python is already installed:

python --version
The project requires Python 3.13 or newer.

For example:

Python 3.13.6
If Python is not installed, install Python 3.13 or newer.

After installation, open a new terminal and verify:

python --version
The repository also contains a .python-version file identifying the Python version used by the project.

2. Install Git
Git is used to clone the repository and obtain future updates.

Check whether Git is installed:

git --version
If Git is not installed, install Git for Windows and open a new terminal afterward.

3. Install uv
The project uses uv to manage its Python environment and dependencies.

Check:

uv --version
If uv is not installed, install it using the official installation instructions for your operating system.

Then verify:

uv --version
4. Clone the repository
Clone the repository:

git clone https://github.com/belkacemm/tamazight-corpus.git
Enter the project directory:

cd tamazight-corpus
Replace the example GitHub URL with the actual repository URL.

5. Create the Python environment
Run:

uv sync
This reads the project's:

pyproject.toml
uv.lock
.python-version
and creates/synchronizes the project environment.

The environment is normally stored in:

.venv/
You normally do not need to activate .venv manually when using uv.

Commands can be run through:

uv run ...
Dependencies
The project defines two groups of dependencies:

Runtime dependencies
Development dependencies
Runtime dependencies
These are required to use the corpus framework.

PyYAML
pyyaml>=6.0.3
Used to read and write YAML configuration files.

The corpus configuration is stored in:

corpus.yaml
SciPy
scipy>=1.18.0
SciPy provides scientific and signal-processing functionality used by the project.

It is useful for audio and speech-data processing.

sounddevice
sounddevice>=0.5.5
Used to communicate with the computer's audio devices.

The framework uses it to record speech through a microphone.

soundfile
soundfile>=0.14.0
Used to read and write audio files.

The framework currently stores recordings as WAV files.

Development dependencies
Development dependencies are required when modifying or testing the framework.

They include:

pytest
pytest>=9.1.1
Used for automated tests.

Run the tests with:

uv run pytest
mypy
mypy>=2.3.0
Used for static type checking.

ruff
ruff>=0.16.1
Used for Python linting and code quality checks.

hatchling
hatchling>=1.31.0
Used as the Python package build backend.

Development environment
Developers should install the development dependencies:

uv sync --dev
Then run the tests:

uv run pytest
Run type checking:

uv run mypy .
Run linting:

uv run ruff check .
Verify the installation
After installation, verify the CLI:

uv run python -m tamazight_corpus.cli --help
The current CLI provides:

usage: cli.py [-h] {init,record,speaker,stats,validate} ...

Tamazight Corpus Framework

positional arguments:
  init
  record
  speaker
  stats
  validate
Command-line interface
The current CLI provides five main commands:

init
record
speaker
stats
validate
Create a new corpus
The init command creates a new corpus project.

Syntax:

uv run python -m tamazight_corpus.cli init PATH --name NAME --language LANGUAGE
Example:

uv run python -m tamazight_corpus.cli init kabyle_dataset --name "Kabyle Speech Corpus" --language "kabyle"
Expected output:

Project created.
This creates the corpus directory and its configuration.

Create a speaker
The speaker create command creates a speaker.

Syntax:

uv run python -m tamazight_corpus.cli speaker create PATH SPEAKER_ID --name NAME
Example:

uv run python -m tamazight_corpus.cli speaker create kabyle_dataset SPK001 --name "Speaker 001"
Expected output:

Speaker SPK001 created.
The speaker is stored in:

metadata/speakers.csv
List speakers
Use:

uv run python -m tamazight_corpus.cli speaker list kabyle_dataset
Example output:

SPK001  Speaker 001
This allows the researcher to verify which speakers are currently registered.

Record an utterance
Use:

uv run python -m tamazight_corpus.cli record kabyle_dataset
The framework asks for a speaker ID:

Speaker ID: SPK001
It then records the configured duration:

Recording for 5.0 seconds...
Recording finished.
The framework then asks for the transcript:

Transcript: Azul fellawen aken matelam
The recording is saved:

Saved recording 000001
The framework automatically creates the corresponding audio and transcript files and updates the recording metadata.

What happens during recording?
The record command performs several operations:

record
 │
 ├── Select speaker
 │
 ├── Record audio
 │
 ├── Ask for transcript
 │
 ├── Save WAV file
 │
 ├── Save transcript
 │
 └── Update recording metadata
For example:

SPK001
   │
   └── 000001
         ├── audio/000001.wav
         ├── transcripts/000001.txt
         └── metadata/recordings.csv
This is the fundamental audio/transcript relationship required for ASR dataset construction.

View corpus statistics
Use:

uv run python -m tamazight_corpus.cli stats kabyle_dataset
Example:

Corpus: Kabyle Speech Corpus
Recordings: 1
Speakers:   1
Duration:   5.0 seconds
Average:    5.0 seconds
The statistics provide a quick overview of the corpus.

As the corpus grows, this information can be used to monitor:

number of recordings
number of speakers
total duration
average recording duration
Validate the corpus
Use:

uv run python -m tamazight_corpus.cli validate kabyle_dataset
Example:

Corpus validation
=================
Recordings checked: 1
Speakers referenced: 1
Validation successful.
Errors found: 0
Validation helps identify inconsistencies before the corpus is used for further research.

Complete dataset-building example
The following is a complete example of creating a small Kabyle speech corpus.

Step 1 — Initialize the corpus
uv run python -m tamazight_corpus.cli init kabyle_dataset --name "Kabyle Speech Corpus" --language "kabyle"
Expected:

Project created.
Step 2 — Create a speaker
uv run python -m tamazight_corpus.cli speaker create kabyle_dataset SPK001 --name "Speaker 001"
Expected:

Speaker SPK001 created.
Step 3 — Verify the speaker
uv run python -m tamazight_corpus.cli speaker list kabyle_dataset
Expected:

SPK001  Speaker 001
Step 4 — Record an utterance
uv run python -m tamazight_corpus.cli record kabyle_dataset
The framework will ask:

Speaker ID: SPK001
Then:

Recording for 5.0 seconds...
Recording finished.
Enter the exact transcript of the recording:

Transcript: Azul fellawen aken matelam
The framework saves the recording.

Step 5 — Check the corpus
uv run python -m tamazight_corpus.cli stats kabyle_dataset
Corpus: Test Corpus

Recordings: 1
Speakers:   1
Duration:   5.0 seconds
Average:    5.0 seconds

Step 6 — Validate the corpus
uv run python -m tamazight_corpus.cli validate kabyle_dataset
A successful corpus should report:

Validation successful.
Errors found: 0
Resulting dataset
After one recording, the corpus looks like:

kabyle_dataset/
│
├── corpus.yaml
│
├── audio/
│   └── 000001.wav
│
├── transcripts/
│   └── 000001.txt
│
└── metadata/
    ├── speakers.csv
    └── recordings.csv
With multiple recordings:

kabyle_dataset/
│
├── corpus.yaml
│
├── audio/
│   ├── 000001.wav
│   ├── 000002.wav
│   ├── 000003.wav
│   └── ...
│
├── transcripts/
│   ├── 000001.txt
│   ├── 000002.txt
│   ├── 000003.txt
│   └── ...
│
└── metadata/
    ├── speakers.csv
    └── recordings.csv
Recommended research workflow
For building a larger speech corpus, the recommended workflow is:

Prepare recording environment
          ↓
Initialize corpus
          ↓
Create speakers
          ↓
Record utterances
          ↓
Enter accurate transcripts
          ↓
Review recordings
          ↓
Run statistics
          ↓
Run validation
          ↓
Correct problems
          ↓
Repeat
          ↓
Prepare ASR dataset
The most important part of this process is transcription accuracy.

For supervised ASR training, each audio file should have a corresponding correct transcription.

Speaker-aware dataset design
Speaker information is important when preparing ASR datasets.

Suppose the corpus contains:

SPK001 → 500 recordings
SPK002 → 400 recordings
SPK003 → 300 recordings
When creating training and test sets, it may be preferable to make speaker-independent splits.

For example:

Training
  SPK001
  SPK002

Testing
  SPK003
This prevents the ASR system from being evaluated primarily on speakers it has already seen during training.

The framework stores speaker IDs specifically so that this type of processing is possible later.

Git and the dataset
The software project and the collected dataset should be treated separately.

The Git repository contains the framework:

Source code
Tests
Examples
Configuration
Documentation
The corpus contains:

Audio
Transcripts
Speaker metadata
Recording metadata
Corpus configuration
Large audio datasets generally should not be committed directly to the source-code Git repository.

In addition, speech recordings may contain personal information and should only be distributed after appropriate consent and licensing procedures have been established.

Project structure
The current source tree is organized approximately as follows:

tamazight_corpus/
│
├── audio/
│   ├── recorder.py
│   └── recorder_config.py
│
├── io/
│   └── config_io.py
│
├── models/
│   ├── audio_file.py
│   ├── config.py
│   ├── corpus.py
│   ├── corpus_statistics.py
│   ├── project.py
│   ├── recording.py
│   ├── speaker.py
│   └── transcript.py
│
├── repositories/
│   ├── file_repository.py
│   ├── repository.py
│   └── speaker_repository.py
│
└── cli.py

tests/
├── test_corpus.py
├── test_project.py
├── test_repository.py
└── test_speaker.py

examples/
├── test_get_example.py
└── test_loading.py
Testing
The framework contains automated tests using pytest.

Run:

uv run pytest
Tests currently cover important parts of:

corpus management
project management
repositories
speakers
The tests are intended to make changes to the framework safer and more reproducible.

Code quality
The project uses:

pytest for testing
mypy for static type checking
ruff for linting
hatchling for package building
Developers can run:

uv run pytest
uv run mypy .
uv run ruff check .
Web application
The CLI is useful for researchers and developers, but it is not ideal for everyone.

The next major development stage is a Flask web application.

The goal is to allow corpus collection through a web browser.

The planned architecture is:

                 Web Browser
                      │
                      ▼
                Flask Web App
                      │
                      ▼
             Tamazight Corpus
                 Framework
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      Repositories              Audio
          │                       │
          └───────────┬───────────┘
                      ▼
                 Corpus Data
The Flask application will use the existing framework instead of duplicating its logic.

Planned web interface
The future application is expected to provide pages for:

Dashboard
│
├── Speakers
│
├── Record
│
├── Transcripts
│
├── Recordings
│
├── Statistics
│
└── Validation
A non-programmer should eventually be able to:

Open the application.
Select or create a speaker.
Record speech.
Enter the transcript.
Save the recording.
Review the recording.
Continue collecting speech.
This will make the framework more practical for community-based and researcher-led data collection.

ASR research
The corpus framework is one component of a larger low-resource ASR research project.

The intended pipeline is:

Kabyle Speech
      ↓
Speech Corpus
      ↓
Validation
      ↓
Dataset Preparation
      ↓
Training / Validation / Test Sets
      ↓
ASR Training
      ↓
Evaluation
      ↓
Kabyle ASR
The project is particularly interested in approaches that can work in low-resource and CPU-limited environments.

Future ASR work
Planned research includes:

establishing a Kabyle ASR baseline
investigating lightweight ASR models
CPU-friendly training approaches
evaluation using appropriate error metrics
comparing ASR approaches
improving transcription quality
creating reproducible training datasets
publishing trained models
publishing research results
Hugging Face and public datasets
A future goal is to publish appropriate versions of the corpus and ASR models through platforms such as Hugging Face.

Potential future resources include:

Kabyle speech dataset
Kabyle ASR model
Tokenizer
Training scripts
Evaluation datasets
Research documentation
Any public release of speech recordings will depend on:

speaker consent
privacy requirements
dataset licensing
ethical research requirements
Research reproducibility
Reproducibility is an important goal of this project.

The repository includes:

pyproject.toml
uv.lock
.python-version
tests/
These files help developers reproduce the software environment and verify that the framework continues to work.

The corpus itself also contains structured metadata so that recordings can be traced to speakers and transcripts.

Roadmap
Completed
[x] Python project structure
[x] uv environment management
[x] Project configuration
[x] Corpus model
[x] Project model
[x] Speaker model
[x] Recording model
[x] Transcript model
[x] Audio model
[x] Speaker repository
[x] File repository
[x] Audio recording
[x] Speaker management
[x] Transcript collection
[x] Recording metadata
[x] Corpus statistics
[x] Corpus validation
[x] CLI
[x] Automated tests
[x] Example scripts
[x] Git repository
Current development
[ ] Flask web application
[ ] Browser-based speaker management
[ ] Browser-based recording
[ ] Browser-based transcript entry
[ ] Browser-based recording review
[ ] Browser-based statistics
[ ] Browser-based validation
Future research
[ ] Expand Kabyle speech corpus
[ ] Improve corpus quality control
[ ] Standardize dataset format
[ ] Speaker-independent dataset splits
[ ] Public corpus release
[ ] ASR baseline
[ ] CPU-friendly ASR experiments
[ ] ASR evaluation
[ ] Kabyle ASR model
[ ] Hugging Face dataset
[ ] Hugging Face model
[ ] Research publications
Research direction
This project is part of a broader effort to develop practical language technology for Tamazight/Kabyle, with an emphasis on low-resource conditions.

The project is being developed incrementally:

Stage 1
Corpus framework
       ↓
Stage 2
Speech collection
       ↓
Stage 3
Kabyle ASR
       ↓
Stage 4
Web-based data collection
       ↓
Stage 5
Public research resources
The intention is not simply to create a collection of audio files, but to establish a reproducible framework for building high-quality speech resources for an under-resourced language.

Contributing
The project is currently in active research and development.

Researchers and developers interested in:

Kabyle
Tamazight
low-resource languages
speech recognition
corpus construction
NLP
language technology
are welcome to follow the project and contribute ideas, code, data, or research collaboration.

Contribution guidelines will be expanded as the project matures.

Data ethics
Speech data collection should be performed responsibly.

Before collecting or publishing recordings from other people, researchers should consider:

informed consent
privacy
anonymization where appropriate
appropriate metadata handling
data ownership
licensing
redistribution rights
ethical research requirements
The framework provides technical tools for corpus construction; it does not itself provide legal or ethical authorization to collect or distribute someone's speech.

License
The software framework and the future speech corpus may have different licenses.

The software license will be specified in the repository.

Any future public speech dataset will have its own documentation and licensing conditions appropriate to the collected data and speaker agreements.

Author and research project
Tamazight/Kabyle Low-Resource Speech and Language Technology

This project is being developed as an independent research effort focused on building practical and reproducible resources for Kabyle/Tamazight.

The long-term objective is to contribute open research tools, datasets, models, and knowledge for low-resource language technology.