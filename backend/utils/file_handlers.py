import os
import shutil

def cleanup_user_dir(session_id):
    temp_dir = f"temp/{session_id}"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
