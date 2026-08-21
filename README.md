
# Tamazight Corpus Framework

A Python framework for creating, collecting, managing, validating, and storing speech corpora.

The framework was initially developed for collecting **Tamazight/Kabyle speech data**, but it can also be used to create speech corpora for other languages.

Each recording consists of:

- WAV audio
- Speaker
- Transcript
- Sample rate
- Number of channels
- Duration
- Recording ID

The framework provides both a **Python/CLI interface** and a **Flask web application**.

For deployment, persistent storage can be provided by **Supabase Storage**, allowing the application to run on platforms such as Render without losing corpus data after a restart or redeployment.

---

## Features

- Create corpus projects
- Manage speakers
- Record speech using a microphone
- Upload existing WAV files
- Enter and edit transcripts
- Validate audio information
- Automatically generate recording IDs
- Store recording metadata
- Store transcripts
- Play recordings from the web application
- Persistent cloud storage with Supabase
- Local filesystem storage for development
- Flask web interface
- Command-line interface
- Designed for low-resource language corpus collection

---

# 1. Architecture

The framework separates corpus-management logic from the storage system.

```text
                    Tamazight Corpus Framework
                              |
              +---------------+---------------+
              |                               |
         Python / CLI                    Flask Web App
              |                               |
              +---------------+---------------+
                              |
                           Project
                              |
                    +---------+---------+
                    |                   |
                  Corpus            Speakers
                    |                   |
               Repository          Repository
                    |
             +------+------+
             |             |
       FileRepository   SupabaseRepository
             |             |
         Local disk     Supabase Storage
This design allows the same corpus framework to work with different storage backends.
2. Requirements
Python
Python 3.13 or newer is recommended.
Check your Python version:
python --version
uv
The project uses uv⁠� for Python environment and dependency management.
Install uv according to the official documentation.
3. Installation
Clone the repository:
git clone https://github.com/belkacemm/tamazight-corpus.git
cd tamazight-corpus
Create the environment and install dependencies:
uv sync
The project environment is managed automatically by uv.
4. Command Line Interface
The framework provides a command-line interface:
uv run tamazight-corpus --help
Available commands include:
init
record
speaker
stats
validate
For example:
uv run tamazight-corpus init
The CLI can be used to create and manage corpora without running the web application.
5. Web Application
The project also includes a Flask web application.
Start the application from the project root:
uv run flask --app web.app run
Then open:
http://127.0.0.1:5000/
The web application provides browser-based access to corpus creation, speaker management, recording, transcription, and recording playback.
6. Creating a Corpus
Open the Create Corpus page.
Enter:
Corpus name
Language
For example:
Corpus name: kabyle-test
Language: Kabyle
Submit the form.
The corpus dashboard will then be displayed.
7. Adding Speakers
Open:
Speakers → Add Speaker
Enter:
Speaker ID: SPK001
Name: Speaker One
Each speaker receives a unique identifier within the corpus.
For example:
SPK001
SPK002
SPK003
Each recording is associated with one speaker.
8. Collecting Speech
Open:
Recordings
Select a speaker.
The application supports two collection methods.
Record from microphone
Click:
Start Recording
Speak normally, then click:
Stop Recording
The browser recording is processed by the application before being stored in the corpus.
Upload an existing WAV file
Select an existing WAV file and upload it together with its speaker and transcript.
9. Adding a Transcript
Enter the transcription corresponding to the recording.
For example:
Azul fellawen
The transcript is stored separately from the audio.
A recording can therefore have:
000001.wav
000001.txt
10. Recording Information
For each recording, the framework stores information such as:
Recording ID
Speaker
Audio file
Transcript
Sample rate
Number of channels
Duration
Example:
ID:          000001
Speaker:     SPK001
Sample rate: 16000
Channels:    1
Duration:    2.45 seconds
Transcript:  Azul fellawen
11. Playing Recordings
The recordings page contains an audio player.
Users can select a recording and play it directly from the web application.
When Supabase Storage is enabled, the permanent recording remains in Supabase while the application retrieves it for browser playback.
12. Persistent Storage with Supabase
For production or cloud deployment, Supabase Storage can be used.
The storage bucket should be configured appropriately for the deployment and access model.
A corpus is organized approximately as:
<corpus-name>/
|
+-- audio/
|   +-- 000001.wav
|   +-- 000002.wav
|   +-- ...
|
+-- transcripts/
|   +-- 000001.txt
|   +-- 000002.txt
|   +-- ...
|
+-- metadata/
    +-- speakers.csv
    +-- recordings.csv
The external storage system allows corpus data to remain available independently of the web application's temporary filesystem.
13. Supabase Configuration
Create a Supabase project and configure a Storage bucket.
The application uses environment variables for the Supabase connection:
SUPABASE_URL
SUPABASE_KEY
Create a .env file locally:
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
Never commit .env to GitHub.
The project .gitignore excludes environment files.
14. Render Deployment
The Flask application can be deployed to Render⁠�.
For deployment, configure the required environment variables:
SUPABASE_URL
SUPABASE_KEY
The application uses Supabase for persistent corpus storage.
This is important because the filesystem of a web-service instance should not be treated as the permanent location of collected corpus data.
After deployment, users can:
Create a corpus
Create speakers
Record or upload speech
Enter transcripts
View recordings
Play recordings
Corpus resources remain in the persistent storage backend after application restart or redeployment.
15. Local and Supabase Storage
The framework supports different storage backends.
Local storage
Local storage is useful during development and testing:
project = Project.create(
    path=corpus_path,
    config=config,
    storage="local",
)
Data is stored on the local filesystem.
Supabase storage
Supabase storage is useful for deployment:
project = Project.create(
    path=corpus_path,
    config=config,
    storage="supabase",
)
Audio, transcripts, and metadata are stored using the configured Supabase backend.
16. Developer Usage
The framework can also be used directly from Python.
Example:
from pathlib import Path

from tamazight_corpus.models.config import CorpusConfig
from tamazight_corpus.models.project import Project

config = CorpusConfig(
    name="kabyle",
    language="Kabyle",
)

project = Project.create(
    path=Path("datasets/kabyle"),
    config=config,
    storage="local",
)
For Supabase storage:
project = Project.create(
    path=Path("datasets/kabyle"),
    config=config,
    storage="supabase",
)
17. Creating a Speaker
A speaker can be created programmatically:
from tamazight_corpus.models.speaker import Speaker

speaker = Speaker(
    id="SPK001",
    name="Speaker One",
)

project.speakers.create(speaker)
Retrieve all speakers:
speakers = project.speakers.all()
Retrieve one speaker:
speaker = project.speakers.get("SPK001")
18. Creating a Recording
A recording contains an audio resource, transcript, and speaker association.
Conceptually:
Recording(
    id=...,
    audio=AudioFile(...),
    transcript=Transcript(...),
    speaker=...,
)
The audio model contains information such as:
AudioFile(
    path=...,
    sample_rate=16000,
    channels=1,
    duration=...,
)
The transcript model contains the transcription:
Transcript(
    text="Azul fellawen",
)
19. Corpus Structure
A corpus conceptually contains speakers and recordings:
Corpus
|
+-- Speakers
|
+-- Recordings
    |
    +-- Audio
    +-- Transcript
    +-- Metadata
Each recording has a unique identifier.
Example:
000001
000002
000003
20. Project Structure
The main project structure is:
tamazight-corpus/
|
+-- tamazight_corpus/
|   +-- audio/
|   +-- io/
|   +-- models/
|   +-- repositories/
|   +-- storage/
|   +-- cli.py
|
+-- web/
|   +-- app.py
|   +-- forms.py
|   +-- templates/
|   +-- static/
|
+-- tests/
|
+-- datasets/
|
+-- pyproject.toml
+-- README.md
+-- .gitignore
The tamazight_corpus package contains reusable corpus-management functionality.
The web directory contains the Flask application and presentation layer.
21. Testing
Run the test suite:
uv run pytest
Run the code-quality checks:
uv run ruff check .
The initial release includes automated tests covering core corpus, project, repository, and speaker functionality.
22. Why This Framework?
Low-resource languages often lack sufficiently large and well-structured speech datasets.
The purpose of this framework is to make the construction of such datasets easier.
A typical collection workflow is:
Speaker
   |
   v
Sentence
   |
   v
WAV recording
   |
   v
Transcript
   |
   v
Metadata
Thousands of recording/transcript pairs can eventually be used to train or fine-tune speech-recognition models.
23. Example Corpus
A larger corpus might eventually contain:
10 speakers
     |
     v
1,000 recordings
     |
     +-- 1,000 WAV files
     |
     +-- 1,000 transcripts
     |
     +-- recording metadata
The resulting dataset can then be prepared for machine-learning and ASR experiments.
24. Roadmap
Planned improvements include:
Better corpus statistics
More comprehensive corpus validation
Recording quality checks
Richer speaker and recording metadata
Export to common dataset formats
Hugging Face dataset integration
Improved speaker management
Batch upload
Dataset preparation for ASR
Additional storage backends
Authentication and user management
25. Contributing
Contributions are welcome.
Possible areas include:
New storage backends
Corpus validation
Web interface improvements
Audio processing
Dataset export
ASR dataset preparation
Support for additional languages
26. License
This project is licensed under the MIT License.
Summary
The Tamazight Corpus Framework provides a modular foundation for collecting and managing speech data.
It separates:
Corpus-management logic
Web application
Storage
The framework can be used locally for development or deployed with Flask and Supabase for persistent cloud-based corpus collection.
The initial development and evaluation focused on Tamazight/Kabyle speech data, with the framework designed to be reusable for other low-resource languages.