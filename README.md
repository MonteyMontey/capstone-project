# Reinforcement Learning Sandbox

## Getting Started

Tested with Python 3.8 on Windows 10, macOS and Ubuntu 20.04.1 LTS. 

### Prerequisites

* Qt 5 must be installed on your system. Installation instructions can be found [here](https://doc.qt.io/qt-5/gettingstarted.html).
* [Optional] If you are on Linux or Windows and have a NVIDIA GPU, you can use [CUDA](https://developer.nvidia.com/cuda-downloads) to boost performance. 


### Installation

1. Clone the repo:
   ```sh
   git clone https://github.com/MonteyMontey/capstone-project.git
   ```

2. Go to the cloned directory and create a virtual environment:

    *On macOS and Linux:*
    ```sh
    python3 -m venv env
    ```
    *On Windows:*
    ```sh
    py -m venv env
    ```

3. Activate the virtual environment:

   *On macOS and Linux:*
    ```sh
    source env/bin/activate
    ```

    *On Windows:*
    ```sh
    .\env\Scripts\activate
    ```
4. Install the required packages:

    *On macOS and Linux:*
     ```sh
    python3 -m pip install -r requirements.txt
    ```
   
    *On Windows:*
    ```sh
    py -m pip install -r requirements.txt
    ```
   
5. Start the program:
    
    *On macOS and Linux:*
     ```sh
    python3 -m main
    ```
   
    *On Windows:*
    ```sh
    py -m main
    ```