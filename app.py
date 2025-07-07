from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import subprocess

app = FastAPI()

# Servimos archivos estáticos (el HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/tree")
async def tree(request: Request):
    data = await request.json()
    path = data.get("path", ".")
    output_format = data.get("format", "ascii")
    cmd = [
        "python3", "genProyTree_v2.py", path,
        "--format", output_format,
        "--ignore-dirs", data.get("ignore_dirs", ""),
        "--ignore-files", data.get("ignore_files", ""),
        "--max-depth", str(data.get("max_depth", 0)),
    ]
    if data.get("show_hidden"):
        cmd.append("--show-hidden")
    if data.get("show_sizes", True):
        cmd.append("--show-sizes")
    if data.get("debug"):
        cmd.append("--debug")
    if data.get("project_name"):
        cmd += ["--project-name", data["project_name"]]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return JSONResponse(content={"error": proc.stderr}, status_code=400)
    return {"output": proc.stdout}

# Página principal: sirve el HTML
@app.get("/")
async def main():
    return FileResponse("static/project_tree_generator.html")
s