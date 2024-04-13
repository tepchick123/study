cd ..
call venv/scripts/activate
uvicorn main:app --reload --port=8000
cmd