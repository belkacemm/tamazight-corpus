from argparse import ArgumentParser
from pathlib import Path

from .models.config import CorpusConfig
from .models.project import Project
from .models.speaker import Speaker


def main():

    parser = ArgumentParser(
        description="Tamazight Corpus Framework"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # =====================
    # INIT
    # =====================

    init_parser = subparsers.add_parser(
        "init",
        help="Create a new corpus project"
    )

    init_parser.add_argument(
        "path"
    )

    init_parser.add_argument(
        "--name",
        required=True
    )

    init_parser.add_argument(
        "--language",
        required=True
    )

    # =====================
    # RECORD
    # =====================

    record_parser = subparsers.add_parser(
        "record",
        help="Record a new utterance"
    )

    record_parser.add_argument(
        "path"
    )

    # =====================
    # SPEAKER
    # =====================

    speaker_parser = subparsers.add_parser(
        "speaker",
        help="Manage speakers"
    )

    speaker_subparsers = speaker_parser.add_subparsers(
        dest="speaker_command",
        required=True
    )

    # speaker create

    speaker_create_parser = speaker_subparsers.add_parser(
        "create",
        help="Create a speaker"
    )

    speaker_create_parser.add_argument(
        "path"
    )

    speaker_create_parser.add_argument(
        "speaker_id"
    )

    speaker_create_parser.add_argument(
        "--name",
        default=None
    )

    # speaker list

    speaker_list_parser = speaker_subparsers.add_parser(
    "list",
    help="List all speakers"
    )

    speaker_list_parser.add_argument(
    "path"
    )

    # =====================
    # STATS
    # =====================

    stats_parser = subparsers.add_parser(
        "stats",
        help="Show corpus statistics"
    )

    stats_parser.add_argument(
        "path"
    )

    # =====================
    # VALIDATE
    # =====================

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate corpus files"
    )

    validate_parser.add_argument(
        "path"
    )

    # =====================
    # PARSE
    # =====================

    args = parser.parse_args()

    # =====================
    # INIT
    # =====================

    if args.command == "init":

        config = CorpusConfig(
            name=args.name,
            language=args.language
        )

        Project.create(
            path=Path(args.path),
            config=config
        )

        print("Project created.")

    # =====================
    # RECORD
    # =====================

    elif args.command == "record":

        project = Project.open(
            Path(args.path)
        )

        speaker_id = input(
            "Speaker ID: "
        ).strip()

        speaker = project.speakers.get(
            speaker_id
        )

        if speaker is None:
            print(
                f"Speaker {speaker_id} not found."
            )
            return

        recording = project.corpus.record(
            speaker
        )

        print(
            f"Saved recording {recording.id}"
        )

    # =====================
    # SPEAKER
    # =====================

    elif args.command == "speaker":

        project = Project.open(
            Path(args.path)
        )

        # speaker create

        if args.speaker_command == "create":

            existing = project.speakers.get(
                args.speaker_id
            )

            if existing is not None:
                print(
                    f"Speaker {args.speaker_id} already exists."
                )
                return

            speaker = Speaker(
                id=args.speaker_id,
                name=args.name
            )

            project.speakers.create(
                speaker
            )

            print(
                f"Speaker {args.speaker_id} created."
            )

        # speaker list

        elif args.speaker_command == "list":

            speakers = project.speakers.all()

            if not speakers:
                print("No speakers found.")
                return

            for speaker in speakers:

                name = speaker.name or ""

                print(
                    f"{speaker.id}\t{name}"
                )
    elif args.command == "stats":

        project = Project.open(
            Path(args.path)
        )

        stats = project.corpus.stats()

        print(f"Corpus: {project.config.name}")
        print()
        print(f"Recordings: {stats.recordings}")
        print(f"Speakers:   {stats.speakers}")
        print(
            f"Duration:   {stats.total_duration:.1f} seconds"
        )
        print(
            f"Average:    {stats.average_duration:.1f} seconds"
        )

    elif args.command == "validate":

        project = Project.open(
            Path(args.path)
        )

        recordings = project.corpus.recordings

        errors = []

        recordings = project.corpus.recordings

        errors = []
        recording_ids = set()

        for recording in recordings:

            if recording.id in recording_ids:
                errors.append(
                    f"{recording.id}: duplicate recording ID"
                )

            recording_ids.add(recording.id)

            if not recording.audio.path.exists():
                errors.append(
                    f"{recording.id}: audio file missing"
                )

            transcript_path = (
                project.path
                / "transcripts"
                / f"{recording.id}.txt"
            )

            if not transcript_path.exists():
                errors.append(
                    f"{recording.id}: transcript file missing"
                )

            speaker = project.speakers.get(
                recording.speaker.id
            )

            if speaker is None:
                errors.append(
                    f"{recording.id}: "
                    f"speaker {recording.speaker.id} not found"
                )        
        
        print()
        print("Corpus validation")
        print("=================")
        print(
            f"Recordings checked: {len(recordings)}"
        )

        speaker_ids = {
            recording.speaker.id
            for recording in recordings
        }

        print(
            f"Speakers referenced: {len(speaker_ids)}"
        )

        if errors:

            print()
            print(
                f"Errors found: {len(errors)}"
            )

            for error in errors:
                print(
                    f"  - {error}"
                )

        else:

            print()
            print("Validation successful.")
            print("Errors found: 0")
               

if __name__ == "__main__":
    main()