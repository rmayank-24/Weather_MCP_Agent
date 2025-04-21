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
![image](https://github.com/user-attachments/assets/06befa53-3da1-44e9-b556-336da2b90be1)

**[Enroll Now](https://www.krishnaik.in/liveclass/2.0%20Live%20Agentic%20AI%20And%20Generative%20AI%20Application%20With%20Cloud%20Bootcamp)** 

Course Overview:

Mentors: Sourangshu Paul, Mayank Aggarwal , Krish And Sunny

Start Date:May 10th 2025

Timing: 8am to 11am IST(Saturday And Sunday)

Duration : 4-5 months

This course is designed for AI developers, machine learning engineers, data scientists, and software engineers looking to build expertise in agentic AI, multi-agent systems, and AI-powered automation. Whether you are new to AI agents or have experience in NLP and GenAI, this course will equip you with the knowledge and hands-on skills required to develop, deploy, and manage AI agents at scale. By the end of the course, you will have a strong foundation in agentic AI frameworks, multi-agent collaboration, real-world automation, and end-to-end AI deployment, along with practical experience through real-world projects.
