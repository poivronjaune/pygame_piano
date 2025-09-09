# MIDI Console Application

This project is a simple Python console application that implements a MIDI interface to display the notes pressed on the keyboard. It utilizes the `pygame.midi` for real-time MIDI input.

## Project Structure

```
pygame_piano
├── midi_pkg
│   ├── main.py           # Console app to display pressed midi notes
│   └── run.py            # Pygame window to display midi notes pressed
│   └── practice.py       # Pygame window to practice finding notes on midi keyboard
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
python midi_pkg/main.py
python midi_pkg/practice.py
```

Once the application is running, press any key on your keyboard to see the corresponding MIDI note displayed in the console.

*Note: ***on some keyboards the USB midi interface needs to be unolugged on evry run. Sometimes just shuting the keyboard down and reopening it works.***
