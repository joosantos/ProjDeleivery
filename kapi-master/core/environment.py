import os

from dotenv import load_dotenv
from envyaml import EnvYAML

load_dotenv()
env_var = os.getenv("ENV", "Production")
print("\nEnviroment mode: " + env_var + "\n")
if env_var == "DEV":
    environment = os.getenv("ENVIRONMENT", "dev")
else:
    environment = os.getenv("ENVIRONMENT", "staging")

config = EnvYAML(f".envs/{environment}.yaml")
