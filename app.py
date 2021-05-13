from factories import Factory
from dotenv import load_dotenv

load_dotenv()
app = Factory().create_app()
if __name__ == '__main__':
    app.run()
