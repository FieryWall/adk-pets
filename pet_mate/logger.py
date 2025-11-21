from enum import Enum

class Role(Enum):
    USER = "User"
    AGENT = "Agent"

def display(role: Role, message: str) -> str:
    print(f"{role.value}: {message}\n")
    return message