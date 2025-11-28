from pydantic import BaseModel, Field

class ProfileGeneratorInput(BaseModel):
    pet_full_name: str = Field(description="The official full name of the pet (species and breed if applicable) from the session, e.g., 'Golden Retriever', 'Persian cat', 'European Hedgehog'.")

class ProfileGeneratorOutput(BaseModel):
    pet_profile: str = Field(description="Comprehensive pet profile including most important characteristics, care guidelines, and interesting facts. Structured for use in future guidance scenarios.")