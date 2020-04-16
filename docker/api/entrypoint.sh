cd api
gunicorn app:app -c run.py
# python profiling.py