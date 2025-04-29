#!/usr/bin/python
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "info@strongbox.space"
__copyright__  = "Copyright 2024"
__license__    = "MIT License"
__status__     = "Development"

__version__    = "0.0.1"
"""
# Engineering GUI dashboard to view 8 camera image feeds and develop
# Computer Vision pipeline

# Disable PyLint (VSCode) linting messages that seem unuseful
# See: https://pypi.org/project/pylint/
# pylint: disable=invalid-name
# pylint: disable=global-statement

# Disable Pyright (Zed IDE) linting messages that seem unuseful
# See: https://pypi.org/project/pyright/
# See: https://github.com/microsoft/pyright/blob/main/docs/getting-started.md
# Using CLI: pyright GUI.py
# Update: pip install --upgrade pyright

import os
import sys
# Headless environment check must run before any side-effectful code
if not os.environ.get("DISPLAY") or os.environ.get("FORCE_HEADLESS") == "1":
    print(
        "No display found. GUI cannot be launched in a headless environment."
    )
    sys.stdout.flush()
    sys.exit(1)


def main():
    """Main entry point for the StrongBox GUI application."""
    # Standard Python libraries
    from time import sleep  # Used to program pause execution

    # Load environment variables for usernames, passwords, & API keys
    # https://pypi.org/project/python-dotenv/
    from dotenv import dotenv_values

    # 3rd Party Libraries
    # Browser class GUI framework to build and display a user interface
    # on mobile, PC, and Mac
    from nicegui import ui

    # Image capture code using USB attached cameras
    import Camera

    # SQLite database to store crate locations
    import Database as db

    # Internally developed modules
    # Useful global constants used across multiple files
    import GlobalConstants as GC

    # Global Variables
    # Application boots up in light mode
    darkMode = ui.dark_mode()
    ui.colors(primary=GC.STRONG_BOX_BLUE)

    imageWidth = 720
    frameRate = 30
    textFontSize = 25

    def set_background(color: str) -> None:
        """Set the background color of the UI body."""
        ui.query("body").style(f"background-color: {color}")

    def page_refresh(cameras):
        """Refresh the page and update camera images."""
        set_background(GC.STRONG_BOX_GREEN)
        cameraA0image.source = cameras[0].take_picture()
        sleep(0.010)
        cameraA90image.source = cameras[0].take_picture()
        sleep(0.010)
        cameraA180image.source = cameras[0].take_picture()
        sleep(0.010)
        cameraA270image.source = cameras[0].take_picture()
        if GC.DEBUG_STATEMENTS_ON:
            print(f"Total number of images taken is {cameras[0].numOfPhotos}")
        cameraA0image.update()
        cameraA90image.update()
        cameraA180image.update()
        cameraA270image.update()

    darkMode.disable()
    db1 = db.Database("strongbox-gui-db.db")
    cameras = []
    for _ in range(GC.NUMBER_OF_CAMERAS):
        newCamera = Camera.Camera()
        cameras.append(newCamera)
    with ui.row().classes("self-center"):
        ui.button("PAGE REFRESH", on_click=lambda e: page_refresh(cameras))
    # Outgoing API connection should only run once.
    # It should run on a single port, in a single-threaded main function.

    # It should run in a single-threaded main function.
    # apiBackgroundProcessCode = start_api()
    # Incoming APIs URL's and keys
    try:
        dotenv_values()
    except KeyError:
        db1.insert_debug_logging_table(
            "ERROR: Could not find .ENV file when calling dotenv_values()"
        )
    if GC.DEBUG_STATEMENTS_ON:
        print(
            "Font size was set to: "
            f"{textFontSize}"
        )
    with ui.footer(value=True):
        ui.label("Strong Box: Air Plant One Mission").style(
            f"font-size: {textFontSize}px"
        )

    # Eight HD 720p (1280 × 720) or 4K UHD (3840 × 2160) cameras on the corners
    # of the A & B sides of a Strong Box cube in two 3 x 3 grids (for MVP).
    # Mission code will stitch into two circles.
    # A0 is the image on the A side of Strong Box hardware,
    # displayed at 0 degrees
    # North
    # on GUI
    with ui.grid(columns=3).classes("self-center"):
        ui.label("").style(
            (
                f"width: {imageWidth}px;"
            )
        )
        ui.label("").style(
            (
                f"width: {imageWidth}px;"
            )
        )
        ui.label("").style(
            (
                f"width: {imageWidth}px;"
            )
        )
        cameraA0image = ui.image(GC.TEST_IMAGE_A)
        cameraA270image = ui.image(GC.TEST_IMAGE_A)
        ui.label(
            f"SIDE A CAMERA'S: {frameRate} Hz"
        ).style(
            (
                f"width: {imageWidth}px; "
                f"font-size: {textFontSize}px; "
                "display: flex; "
                "justify-content: center; "
                "align-items: center;"
            )
        )
        cameraA90image = ui.image(GC.TEST_IMAGE_A)
        cameraA180image = ui.image(GC.TEST_IMAGE_A)
    with ui.grid(columns=3).classes("self-center"):
        ui.label("").style(
            (
                f"width: {imageWidth}px;"
            )
        )
        ui.label("").style(
            (
                f"width: {imageWidth}px;"
            )
        )
        ui.label("").style(
            (
                f"width: {imageWidth}px;"
            )
        )
        ui.image("")
        ui.image("")
        ui.image(GC.TEST_IMAGE_B)
        ui.label(
            f"SIDE B CAMERA'S: {frameRate} Hz"
        ).style(
            (
                f"width: {imageWidth}px; "
                f"font-size: {textFontSize}px; "
                "display: flex; "
                "justify-content: center; "
                "align-items: center;"
            )
        )
        ui.image(GC.TEST_IMAGE_B)
        ui.image(GC.TEST_IMAGE_B)

    ui.run()


if __name__ == "__main__":
    main()
