import os
import tempfile
import shutil
import zipfile
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, send_file, flash, session, redirect, url_for, jsonify

from reduction.reduce import reduce_science_images  # Your reduction function to implement

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"  # Replace with your actual secret key

@app.route("/", methods=["GET", "POST"])
def upload_and_process():
    if request.method == "POST":
        temp_dir = tempfile.mkdtemp()

        try:
            bias_files = request.files.getlist("bias")
            flat_files = request.files.getlist("flat")
            dark_files = request.files.getlist("dark")
            science_files = request.files.getlist("science")

            print(science_files)

            # Validate required uploads
            if not science_files or all(f.filename == '' for f in science_files):
                flash("Please upload at least one science FITS file.")
                return render_template("index.html")

            if not flat_files or all(f.filename == '' for f in flat_files):
                flash("Please upload at least one flat frame.")
                return render_template("index.html")
            
            if not dark_files or all(f.filename == '' for f in dark_files):
                flash("Please upload at least one dark frame.")
                return render_template("index.html")

            def save_files(files, prefix):
                paths = []
                for i, f in enumerate(files):
                    if f and f.filename:
                        filename = secure_filename(f.filename)
                        if prefix != "science":
                            filename = f"{prefix}_{i}_{filename}"
                        path = os.path.join(temp_dir, filename)
                        f.save(path)
                        paths.append(path)
                return paths

            bias_paths = save_files(bias_files, "bias")
            flat_paths = save_files(flat_files, "flat")
            dark_paths = save_files(dark_files, "dark")
            science_paths = save_files(science_files, "science")

            # Save filenames in session for display
            session["bias"] = session.get("bias", []) + [os.path.basename(p) for p in bias_paths]
            session["flat"] = session.get("flat", []) + [os.path.basename(p) for p in flat_paths]
            session["dark"] = session.get("dark", []) + [os.path.basename(p) for p in dark_paths]
            session["science"] = session.get("science", []) + [os.path.basename(p) for p in science_paths]

            reduced_paths = reduce_science_images(
                bias_paths=bias_paths,
                flat_paths=flat_paths,
                dark_paths=dark_paths,
                science_paths=science_paths,
                output_dir=temp_dir
            )

            zip_path = os.path.join(temp_dir, "reduced_images.zip")
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for filepath in reduced_paths:
                    zipf.write(filepath, arcname=os.path.basename(filepath))

            return send_file(
                zip_path,
                as_attachment=True,
                download_name="reduced_images.zip",
                mimetype="application/zip"
            )

        except Exception as e:
            flash(f"Unexpected error: {str(e)}")
            return render_template("index.html")

        @after_this_request
        def cleanup(response):
            shutil.rmtree(temp_dir)
            return response


    # For GET requests or after errors, render with current session filenames
    return render_template("index.html")


@app.route("/remove_file", methods=["POST"])
def remove_file():
    data = request.get_json()
    category = data.get("category")
    filename = data.get("filename")

    if not category or not filename or category not in ["science", "bias", "flat", "dark"]:
        return jsonify({"success": False, "message": "Invalid category or filename"}), 400

    files = session.get(category, [])
    if filename in files:
        files.remove(filename)
        session[category] = files
        return jsonify({"success": True, "message": f"Removed {filename} from {category} files."})

    return jsonify({"success": False, "message": "File not found in session."}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
