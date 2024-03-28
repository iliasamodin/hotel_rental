from fastapi import FastAPI

import uvicorn
import sys
import os

from settings import settings

# FastAPI instance declaration
app = FastAPI()

if __name__ == "__main__":
    # Getting the project directory 
    #   - the parent directory for the directory 
    #   in which the main.py module is located
    project_path = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__),
        ),
        os.pardir,
    )
    # Adding the project root directory to the list of module paths
    sys.path.append(project_path)

    uvicorn.run(
        app="app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
