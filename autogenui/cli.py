from typing_extensions import Annotated
import typer
import uvicorn
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server.sol")
logger.setLevel(logging.INFO)

app = typer.Typer(invoke_without_command=True)

@app.callback()
def main(
    host: str = "0.0.0.0",
    port: int = 8080,
    workers: int = 1,
    reload: Annotated[bool, typer.Option("--reload")] = True,
    docs: bool = False,
):
    """
    Launch the Autogen UI CLI .Pass in parameters host, port, workers, and reload to override the default values.
    """

    os.environ["AUTOGENUI_API_DOCS"] = str(docs)
    logger.info("Running server")

    uvicorn.run(
        "autogenui.web.app:app",
        host=host,
        port=port,
        workers=workers,
        reload=reload,
    )


@app.command()
def models():
    print("A list of supported providers:")


def run():
    logger.info("Before App")
    app()


if __name__ == "__main__":
    app()
