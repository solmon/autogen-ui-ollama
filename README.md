# AutoGen UI

![AutoGen UI Screenshot](docs/images/autogenuiscreen.png)

> [!IMPORTANT]  
> This repo has been updated to use the [AutoGen AgentChat](https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/quickstart.html) interface based on the new AutoGen 0.4x AgentChat api. Also, the API might change, so expect some breaking changes in the future.

The hello world for building a UI interface with AutoGen AgentChat API.

Example UI to demonstrate how to build interfaces using the [AutoGen AgentChat](https://github.com/microsoft/autogen) API. The UI is built using Next.js and web apis built using FastApi.

# Changes from original repo
Following changes are introduced from the original repo:

1) Migrated to the 0.47 version of autogen.
2) Added support for running local ollama models

## What Does the App Do?

![AutoGen UI Flow Diagram](docs/images/flowdiag.png)

- [`autogenui.manager`](autogenui/manager.py) - provides a simple run method that takes a prompt and returns a response from a predefined [agent team](notebooks/default_team.json). Take a look at the [agent team](notebooks/default_team.json) json config file to see how the agents are configured. It gives a general idea on what types of agents are supported etc. Check out the [tutorial notebook](notebooks/tutorial.ipynb) for an example on how to use the provide class to load a team spec.

- [`autogenui.web.app.py`](autogenui/web/app.py) - FastApi backend that serves a simple `/generate` endpoint that takes a prompt and returns a response from a predefined [agent team](notebooks/default_team.json).

  - Creates a manager to run tasks
  - Streams results of the task run to the client ui

- [`frontend`](frontend) - Next.js frontend that provides a simple chat interface to interact with the backend.

## What's Next?

This app is clearly just a starting point. Here are some ideas on how to extend it:

- Extend the manager to support multiple team configurations from the UI
- Storing and loading interaction history in a database.
- Security - add authentication and authorization to the app

> [!TIP] Note
> [AutoGen Studio](https://github.com/microsoft/autogen/tree/main/python/packages/autogen-studio) is being rewritten on the AgentChat api to address most of the above points. Take a look at the implementation there for a more complete example.

## Getting Started

Note that you will have to setup your OPENAI_API_KEY to run the app.

```bash
export OPENAI_API_KEY=<your key>
```

Install dependencies. Python 3.9+ is required. You can install from pypi using pip.

```bash
pip install autogenui
```

or to install from source

```bash
git clone git@github.com:victordibia/autogen-ui.git
cd autogenui
pip install -e .
```

Run ui server.

Set env vars `OPENAI_API_KEY`

```bash
export OPENAI_API_KEY=<your_key>
```

```bash
autogenui # or with --port 8081
```

Open http://localhost:8081 in your browser.

To modify the source files, make changes in the frontend source files and run `npm run build` to rebuild the frontend.

## Development

To run the app in development mode, you will need to run the backend and frontend separately.

## Backend - with hot-reload

```bash
autogenui --reload
```

> [!TIP] Tip
> The UI loaded by this CLI in a pre-complied version by running the frontend build command show blow. That means if you make changes the frontend code or change the hostname or port the backend is running on the frontend updated frontend code needs to be rebuilt for it to load through this command.

## Frontend

```bash
cd frontend
```

Install dependencies

```bash
yarn install
```

Run in dev mode - with hot-reload

Set `NEXT_PUBLIC_API_SERVER` on the command line.

```bash
export NEXT_PUBLIC_API_SERVER=http://<your_backend_hostname>/api
```

Or create a `.env` file in the frontend folder with the following content.

```bash
NEXT_PUBLIC_API_SERVER=http://<your_backend_hostname>/api
```

where your_backend_hostname - is the hostname that autogenui is running on e.g. `localhost:8081`

```bash
yarn dev
```

(Re)build

Remember to install dependencies and set `NEXT_PUBLIC_API_SERVER` before building.

```bash
yarn build
```

## Roadmap

There isnt really much of a roadmap for this project. It is meant as a simple example to get started with the AutoGen AgentChat API. For a more complete example, take a look at the [AutoGen Studio](https://github.com/microsoft/autogen/tree/main/python/packages/autogen-studio) project.
