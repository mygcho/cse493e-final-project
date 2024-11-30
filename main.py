import yaml
from frontend.ui import create_interface

# Load configuration
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

language_choices = config['languages']

if __name__ == "__main__":
    interface = create_interface(language_choices)
    interface.launch(share=False)
