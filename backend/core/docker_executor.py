import docker
import os
import uuid

client = docker.from_env()

def run_function_in_docker(file_path, language, timeout):
    container_name = f"lambda_{uuid.uuid4().hex}"
    base_image = "lambda_base_python" if language == "python" else "lambda_base_node"

    try:
        container = client.containers.run(
            image=base_image,
            command=["python3", "/app/code.py"] if language == "python" else ["node", "/app/code.js"],
            volumes={
                os.path.abspath(file_path): {"bind": f"/app/code.{file_path.split('.')[-1]}", "mode": "ro"}
            },
            name=container_name,
            network_disabled=True,
            detach=True,
            mem_limit='128m',
            stderr=True,
        )
        result = container.wait(timeout=timeout)
        logs = container.logs().decode()
        container.remove()
        return {"result": logs, "status": result}
    except Exception as e:
        return {"error": str(e)}
