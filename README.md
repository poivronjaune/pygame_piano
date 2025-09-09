# MIDI Console Application

This project is a simple Python console application that implements a MIDI interface to display the note pressed on the keyboard. It utilizes the `mido` library for MIDI handling and `python-rtmidi` for real-time MIDI input/output.

## Project Structure

```
midi-console-app
├── src
│   ├── main.py          # Entry point of the application
│   └── midi_interface.py # Contains the MIDIInterface class
├── requirements.txt      # Lists project dependencies
└── README.md             # Documentation for the project
```

## Installation

To set up the project, you need to install the required dependencies. You can do this by running the following command:

```
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command:

```
python src/main.py
```

Once the application is running, press any key on your keyboard to see the corresponding MIDI note displayed in the console.

## MIDI Interface

The `MIDIInterface` class in `midi_interface.py` handles all MIDI input and output. It includes methods to start listening for keyboard events and to translate key presses into MIDI note values.

## Contributing

If you would like to contribute to this project, please feel free to submit a pull request or open an issue for discussion.