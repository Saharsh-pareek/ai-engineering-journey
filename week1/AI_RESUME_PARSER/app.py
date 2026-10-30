import os
import tempfile
from pathlib import Path

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from mini_proj import analyze_resumes, ProjectError

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB total request
ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    error = None
    job_description = ""

    if request.method == "POST":
        job_description = request.form.get("job_description", "").strip()
        uploaded_files = request.files.getlist("resumes")

        if not job_description:
            error = "Please paste a job description."
        elif len(job_description) < 30:
            error = "Please enter a more complete job description."
        else:
            usable_files = [
                f for f in uploaded_files
                if f and f.filename and Path(f.filename).suffix.lower() in ALLOWED_EXTENSIONS
            ]
            if not usable_files:
                error = "Upload at least one PDF or DOCX resume."
            elif len(usable_files) > 20:
                error = "Please upload no more than 20 resumes per run."
            else:
                try:
                    with tempfile.TemporaryDirectory(prefix="resume_matcher_") as tmp:
                        tmp_path = Path(tmp)
                        saved_count = 0
                        for file in usable_files:
                            safe_name = secure_filename(file.filename)
                            if not safe_name:
                                continue
                            # Prefix to avoid collisions when files share a name.
                            destination = tmp_path / f"{saved_count}_{safe_name}"
                            file.save(destination)
                            saved_count += 1

                        if saved_count == 0:
                            error = "No valid files could be saved. Try renaming the files."
                        else:
                            results = analyze_resumes(job_description, tmp_path)
                            if not results:
                                error = "No readable resumes were found. Check that the files contain selectable text."
                except ProjectError as exc:
                    error = str(exc)
                except Exception:
                    app.logger.exception("Resume analysis failed")
                    error = "Analysis failed. Check the terminal for details, then try again."

    return render_template(
        "index.html",
        results=results,
        error=error,
        job_description=job_description,
    )


@app.errorhandler(413)
def request_too_large(_error):
    return render_template(
        "index.html",
        results=None,
        error="The total upload is too large. Keep all files under 16 MB.",
        job_description="",
    ), 413


if __name__ == "__main__":
    # Local development only. Do not use Flask's debug server in production.
    app.run(host="127.0.0.1", port=5000, debug=True)
