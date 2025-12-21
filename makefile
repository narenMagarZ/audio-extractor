migrate-up:
	PYTHONPATH=. python3 src/migration/create-audio-extraction-jobs.py

migrate-down:
	PYTHONPATH=. python3 src/migration/drop-audio-extraction-jobs.py

run:
	uvicorn src.main:app --host 127.0.0.1 --port 8000 ${RELOAD}