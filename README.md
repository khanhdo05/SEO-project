# Catch Me If You Can

Welcome to "Catch Me If You Can," a fun and interactive game built with Pygame!

## Prerequisites

Before playing the game, ensure that you have Python and Pygame installed on your machine. Follow the steps below:

### 1. Install Python

- **Windows:**
  - Download Python from [python.org](https://www.python.org/downloads/).
  - During installation, make sure to check the box that says "Add Python to PATH."

- **Linux:**
  - Use your package manager to install Python.
    ```bash
    sudo apt update
    sudo apt install python3
    ```

- **macOS:**
  - Python is usually pre-installed. If not, you can use [Homebrew](https://brew.sh/) to install it.
    ```bash
    brew install python
    ```

### 2. Install pip (if not already installed)

- **Windows:**
  - Python on Windows usually comes with `pip`. Open Command Prompt and run:
    ```bash
    pip --version
    ```

  - If `pip` is not installed, download `get-pip.py` from [https://bootstrap.pypa.io/get-pip.py](https://bootstrap.pypa.io/get-pip.py) and run:
    ```bash
    python get-pip.py
    ```

- **Linux:**
  - Most Linux distributions come with Python and `pip`. Verify with:
    ```bash
    python3 --version
    pip3 --version
    ```

- **macOS:**
  - Check Python and pip versions:
    ```bash
    python3 --version
    pip3 --version
    ```

## Game Installation

1. **Download the Repository:**
    - Click the green "Code" button on the GitHub repository page.
    - Select "Download ZIP."
    - Extract the downloaded ZIP file to a location of your choice.

2. **Open the Command Shell:**
    - On **Windows**, press `Win + R`, type `cmd`, and press Enter.
    - On **Linux/Mac**, open the Terminal.

3. **Navigate to the Game Directory:**

    ```bash
    cd Downloads/falling-object-game-main
    ```

4. **Install Pygame:**

    ```bash
    pip3 install pygame
    ```

5. **Run the Game:**

    ```bash
    python3 main.py
    ```

## How to Play

- Use the **left** and **right** arrow keys to move the player character.
- Catch the coin to score points.
- If you miss a coin, you lose 1 heart and the speed of the coin falls faster.
- Avoid foul objects to prevent losing points.
- Pause the game by pressing the **space** key.
- If you run out of hearts (you have 3), the game is over.

Have fun playing "Catch Me If You Can"!