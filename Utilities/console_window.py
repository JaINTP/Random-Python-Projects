"""
This module provides the ConsoleWindow class, a curses-based console window interface
for creating applications with dynamic, scrollable content and a status bar. It's designed
for terminal applications that require real-time data display and user interactions.
"""

import threading
import time
import unicurses as uc

class ConsoleWindow:
    """
    A base class for creating a console window interface with scrollable content
    and a status bar, leveraging curses for real-time data display and user interactions.
    Designed for terminal applications needing dynamic content updates and userinteractions.

    Extend this class by overriding the `worker_task` method to implement specific logic for content updates.
    """

    def __init__(self):
        """
        Initializes the console window, preparing it for dynamic content display and user interaction.
        """
        self.stdscr = uc.initscr()
        self.content = []
        self.scroll_position = 0
        self.background_thread = threading.Thread(target=self.worker_task, daemon=True)
        self.status_text = "Status: Initializing"
        self.quit_message = "Press Q to quit"
        self.__init_ui()

    def __init_ui(self):
        """
        Initializes UI components such as window dimensions, color schemes, and input modes.
        """
        uc.start_color()
        uc.init_pair(1, uc.COLOR_WHITE, uc.COLOR_BLUE)
        uc.clear()
        self.height, self.width = uc.getmaxyx(self.stdscr)
        uc.noecho()
        uc.cbreak()
        uc.keypad(self.stdscr, True)
        uc.mousemask(uc.ALL_MOUSE_EVENTS)
        self.__setup_display_areas()

    def __setup_display_areas(self):
        """
        Configures display areas for the title, content, and status bar within the window.
        """
        self.title_row = 0
        self.status_row = self.height - 1
        self.content_start_row = 1
        self.content_end_row = self.status_row - 1
        uc.refresh()

    @property
    def displayable_content_lines(self):
        """
        Calculates the number of lines that can fit in the content display area.
        """
        return self.content_end_row - self.content_start_row + 1

    def set_title(self, title: str):
        """
        Sets the window's title.

        Args:
            title (str): The title text to be displayed.
        """
        uc.move(self.title_row, 0)
        uc.clrtoeol()
        uc.mvaddstr(self.title_row, 0, " " * self.width, uc.color_pair(1))
        title_position = (self.width - len(title)) // 2
        uc.mvaddstr(self.title_row, title_position, title, uc.color_pair(1) | uc.A_BOLD)
        uc.refresh()

    def add_content(self, message: str):
        """
        Appends a line of text to the scrollable content area.

        Args:
            message (str): The text to be added to the content area.
        """
        self.content.append(message)
        self.__adjust_scroll_for_new_content()
        self.update_content_window()

    def __adjust_scroll_for_new_content(self):
        """
        Adjusts the scroll position to ensure new content is displayed appropriately.
        """
        if len(self.content) > self.displayable_content_lines:
            self.scroll_position = len(self.content) - self.displayable_content_lines

    def set_status(self, status: str):
        """
        Updates the status bar text.

        Args:
            status (str): The new status message.
        """
        uc.move(self.status_row, 0)
        uc.clrtoeol()
        uc.mvaddstr(self.status_row, 0, " " * self.width, uc.color_pair(1))
        uc.mvaddstr(self.status_row, 0, status, uc.color_pair(1) | uc.A_BOLD)
        quit_msg_pos = self.width - len(self.quit_message)
        uc.mvaddstr(self.status_row, quit_msg_pos, self.quit_message, uc.color_pair(1) | uc.A_BOLD)
        uc.refresh()

    def update_content_window(self):
        """
        Redraws the content area to reflect any new additions or scroll adjustments.
        """
        uc.move(self.content_start_row, 0)
        uc.clrtobot()
        content_to_display = self.content[self.scroll_position:self.scroll_position + self.displayable_content_lines]
        for i, line in enumerate(content_to_display):
            uc.mvaddstr(self.content_start_row + i, 0, line[:self.width])
        self.set_status(self.status_text)
        uc.refresh()

    def scroll_content_up(self):
        """
        Scrolls the content area upwards by one line, if possible.
        """
        if self.scroll_position > 0:
            self.scroll_position -= 1
            self.update_content_window()

    def scroll_content_down(self):
        """
        Scrolls the content area downwards by one line, if there is more content to view.
        """
        if self.scroll_position < len(self.content) - self.displayable_content_lines:
            self.scroll_position += 1
            self.update_content_window()

    def worker_task(self):
        """
        A placeholder for a background task that updates the content dynamically.
        Must be overridden in subclasses to provide functionality.
        """
        raise NotImplementedError("Override worker_task in a subclass.")

    def run(self):
        """
        Main loop for the console window, handling user input and quitting on command.
        """
        self.background_thread.start()
        try:
            while True:
                ch = uc.getch()
                if ch == uc.KEY_MOUSE:
                    _, _, _, _, bstate = uc.getmouse()
                    if bstate & uc.BUTTON4_PRESSED:
                        self.scroll_content_up()
                    elif bstate & uc.BUTTON5_PRESSED:
                        self.scroll_content_down()
                elif ch in (ord('q'), ord('Q')):
                    break
        finally:
            uc.endwin()

if __name__ == '__main__':
    class ExampleConsoleWindow(ConsoleWindow):
        def worker_task(self):
            """
            Example override of worker_task to demonstrate dynamic content update.
            Adds content periodically, showing a running timer.
            """
            start_time = time.time()
            for count in range(1, 66):
                elapsed_time = int(time.time() - start_time)
                minutes, seconds = divmod(elapsed_time, 60)
                self.set_status(f"Running for {minutes}m {seconds}s.")
                time.sleep(1)  # Simulate work
                self.add_content(f"Example content {count}")
            self.set_status("Status: Done")

    win = ExampleConsoleWindow()
    win.set_title("Example Console Output")
    win.set_status("Status: Running")
    win.run()
