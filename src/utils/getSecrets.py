
# def _get_secret(name: str) -> str:
#     with open(f"/run/secrets/{name}", "r") as file:
#         return file.read()

# Use this definition if runnning outside docker container   
def _get_secret(name: str) -> str:
    filename = "secrets/" + name + ".txt"
    with open(filename, "r") as file:
        return file.read()