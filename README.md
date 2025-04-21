# MCP Server Basic Example

This is a basic example of a Model Context Protocol (MCP) server implementation that demonstrates core functionality including tools and resources.

## Setup Steps

1. Initialize the project (Go to any local folder and launch powershell or cmd):
```bash
uv init mcp-server-basic
cd mcp-server-basic
```

2.  # Create virtual environment and activate it
```bash
  uv venv
  .venv\Scripts\activate
  ```

3. Install dependencies:
```bash
uv add "mcp[cli]"
```
or 
```bash
uv add -r requirements.txt
```


## Features

The server implements the following features:

### Tools
- `add(a: int, b: int)`: Adds two numbers
- `subtract(a: int, b: int)`: Subtracts second number from first

### Resources
- `greeting://{name}`: Returns a personalized greeting

## Running the Server

To run the server with the MCP Inspector for development:
```bash
uv run mcp dev main.py
```

To run the server normally:
```bash
uv run mcp run
```

To install the server in Claude desktop app:
```bash
uv run mcp install main.py
```

## MCP connect in VS code
- Open folder/mcp-server-basic in vs code
- open terminal and run below command :
```bash
uv run main.py
```
- Click Cntrl+Shift+I  to launch chat in vs code
- Do login with Github and setup 
- Folow the below steps (two way to add mcp  configuration for vs code user settings):

[Watch the demo](videos/mcp%20basic.mp4)



## Project Structure
- `main.py`: Main server implementation with tools and resources
- `pyproject.toml`: Project configuration and dependencies

## 2.0 Agentic AI And GENERATIVE AI With MCP Bootcamp
https://www.krishnaik.in/liveclass/2.0%20Live%20Agentic%20AI%20And%20Generative%20AI%20Application%20With%20Cloud%20Bootcamp
