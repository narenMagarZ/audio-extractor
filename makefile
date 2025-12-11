migrate-up:
	PYTHONPATH=. python3 src/migration/create-audio-extraction-jobs.py

migrate-down:
	PYTHONPATH=. python3 src/migration/drop-audio-extraction-jobs.py