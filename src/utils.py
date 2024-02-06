from database import DatabaseInterface

def get_pydantic_model(interface:DatabaseInterface):
    return interface.model