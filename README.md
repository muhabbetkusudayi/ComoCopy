# ComoCopy

ComoCopy is a professional-grade static website mirroring and cloning tool. It is designed to download a website's full structure, including HTML, CSS, JavaScript, images, and other assets, while maintaining the original directory hierarchy.



## Core Features

* **Deep Cloning**: Recursively crawls all internal links such as dashboards, login pages, and subdirectories within the same domain.
* **Full Asset Extraction**: Automatically detects and downloads all static resources including scripts (.js), stylesheets (.css), images, and video sources.
* **Dynamic Rendering**: Utilizes Playwright to execute JavaScript and capture content from modern frameworks like React, Vue, and Angular.
* **Automated Setup**: Automatically verifies and installs required Python libraries and browser engines upon first execution.
* **Government Domain Alert**: Includes a built-in warning system for .gov domains to ensure the user is aware of the legal implications.
* **Configurable Export Path**: Offers a settings menu to define custom save locations on the local system.

## Prerequisites

The application requires Python installed on your system. The script handles the installation of the following dependencies automatically:

* Playwright (Chromium Engine)
* BeautifulSoup4
* Requests

## Installation

1. Download the script to your local machine.
2. Open a terminal or command prompt in the project folder.
3. Run the application using the following command:

**THIS PROJECT MADE FOR EDUCATIONAL PURPOSES. DO NOT USE FOR BAD THINGS.**

```bash
python main.py
