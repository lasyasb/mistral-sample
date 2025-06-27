from flask import Flask, render_template, request, send_file
import os
from datetime import datetime
from mistral_content_creator import generate_content_streaming, save_to_pptx

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    ppt_download_link = None
    generated_text = None

    if request.method == "POST":
        topic = request.form["topic"]
        content_type = request.form["type"]
        tone = request.form["tone"]

        content = generate_content_streaming(topic, content_type, tone)

        if content:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_base = f"{content_type}_{topic.replace(' ', '_')}_{timestamp}"
            text_path = os.path.join("outputs", f"{filename_base}.txt")

            os.makedirs("outputs", exist_ok=True)
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            if content_type == "ppt":
                pptx_path = save_to_pptx(content, os.path.join("outputs", filename_base))
                ppt_download_link = pptx_path
            else:
                generated_text = content

    return render_template("index.html", content=generated_text, ppt_link=ppt_download_link)

@app.route("/download/<path:filename>")
def download_file(filename):
    return send_file(filename, as_attachment=True)
import webbrowser

if __name__ == "__main__":
    port = 5000
    url = f"http://127.0.0.1:{port}/"
    print(f"🚀 Opening {url}")
    webbrowser.open(url)
    app.run(debug=True, port=port)
