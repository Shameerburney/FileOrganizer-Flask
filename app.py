from flask import Flask, render_template, request
import os, shutil

app = Flask(__name__)

# Your file organizing function
def organize_files(folder_path):
    extensions = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif'],
        'Documents': ['.pdf', '.docx', '.txt', '.csv', '.xlsx', '.pptx'],
        'Videos': ['.mp4', '.mov', '.avi'],
        'Music': ['.mp3', '.wav'],
        'Code': ['.py', '.ipynb', '.env']
    }

    file_count = 0
    for folder in extensions.keys():
        os.makedirs(os.path.join(folder_path, folder), exist_ok=True)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            moved = False
            for folder, exts in extensions.items():
                if ext in exts:
                    shutil.move(file_path, os.path.join(folder_path, folder, filename))
                    moved = True
                    file_count += 1
                    break
            if not moved:
                os.makedirs(os.path.join(folder_path, 'Others'), exist_ok=True)
                shutil.move(file_path, os.path.join(folder_path, 'Others', filename))
                file_count += 1

    return file_count

# Flask route
@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        folder = request.form.get("folder_path")
        if folder and os.path.exists(folder):
            count = organize_files(folder)
            message = f"Organized {count} files successfully!"
        else:
            message = "Please enter a valid folder path."
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
