#!/usr/bin/env python3
"""
Piano Practice Application
A pygame-based MIDI piano practice application for learning notes.
"""

import sys
import os

# Add the project root to Python path to ensure imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and initialize the logger first
from piano.core.logger import get_logger

# Create logger for this module
logger = get_logger(__name__)


class PianoPracticeApp:
    """Main application class for the Piano Practice application."""
    
    def __init__(self):
        """Initialize the Piano Practice application."""
        logger.info("Initializing Piano Practice Application")
        self.running = False
        
    def setup(self):
        """Set up the application resources."""
        logger.debug("Setting up application resources")
        # TODO: Initialize pygame
        # TODO: Initialize MIDI interface
        # TODO: Initialize UI components
        logger.info("Application setup complete")
        
    def run(self):
        """Main application loop."""
        logger.info("Starting Piano Practice Application")
        self.running = True
        
        try:
            self.setup()
            logger.info("Application is running...")
            
            # TODO: Main game loop will go here
            # For now, just demonstrate logging
            logger.debug("This would be where the main loop runs")
            
            # Simulate some application events for logging demonstration
            logger.info("Application started successfully")
            logger.debug("Debug: Checking MIDI devices...")
            logger.warning("Warning: No MIDI device connected (simulated)")
            
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean up application resources."""
        logger.info("Cleaning up application resources")
        # TODO: Close MIDI connections
        # TODO: Quit pygame properly
        # TODO: Any other cleanup
        logger.info("Application shutdown complete")


def main():
    """Entry point for the application."""
    logger.info("=" * 60)
    logger.info("Piano Practice Application Starting")
    logger.info("=" * 60)
    
    try:
        app = PianoPracticeApp()
        app.run()
    except Exception as e:
        logger.critical(f"Failed to start application: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
