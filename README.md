<picture>
 <source media="(prefers-color-scheme: dark)" srcset="images/Interface.png">
 <source media="(prefers-color-scheme: light)" srcset="images/Interface.png">
 <img alt="YOUR-ALT-TEXT" src="images/Interface.png">
</picture>

### Biometric Voice App for Dual Input Recording

This Project was developed By Ansen Herrick for the Computer Engineering Department at Clarkson University 
Download the raw exe file here: https://drive.google.com/drive/folders/1QpEKyU-ISvTi3NBDXlIJSYdha-J8p20A?usp=drive_link

### Background
At Clarkson University, researchers have developed an innovative approach to biometric identification through voice analysis. By meticulously measuring and analyzing the subtle nuances in the way individuals pronounce and articulate words, this technology can distinguish between different speakers or verify if two voice samples originate from the same person. The application we've developed serves as a critical tool in this research, enabling the collection of voice samples under various conditions. It supports both text-independent and text-dependent voice recording sessions, accommodating the diverse needs of linguistic research and biometric identification.

### Features
* **Simultaneous Dual-Device Recording:** This feature enables the concurrent audio capture from two distinct devices, enhancing the robustness and diversity of voice data collection.
* **Environmental Tagging Capability:** Users can tag recordings to indicate they were made in noisy environments, facilitating more accurate data categorization and analysis.
* **Microphone Selection Option:** The application allows users to select specific microphones for recording, offering flexibility and control over the audio capture process.
* **Microphone Functionality Feedback:** Provides immediate feedback on microphone status, ensuring users are aware of their operational status and can troubleshoot any issues promptly.

### Setup
To get started with this program, follow the steps below to download the necessary files and install the required packages:

1. Download the application files from the repository.
2. Ensure Python is installed on your system.
3. Install the following dependencies using pip, Python's package installer:

```
pip install tkinter ttkthemes sounddevice numpy wavio SpeechRecognition Pillow customtkinter
```

These packages provide the core functionality for the application, including the graphical user interface (GUI) with Tkinter and CustomTkinter, audio processing with SoundDevice and Wavio, speech recognition capabilities, and support for JSON and image processing.

After installing the dependencies, you can run the application by executing the main Python script. The application is designed to be user-friendly, with a straightforward setup process that allows researchers and users alike to start collecting and analyzing voice data promptly.
