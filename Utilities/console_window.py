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
    Designed for terminal applications needing dynamic content updates and interactions.

    Please note, resizing the terminal window can cause display issues.

    Attributes:
        stdscr: The standard screen object from unicurses used for the interface.
        content: A list of strings representing the content to be displayed.
        scroll_position: An integer tracking the current scroll position.
        background_thread: A threading.Thread object for running background tasks.
        status_text: A string representing the current status text.
        quit_message: A string displayed to indicate how to quit the application.
        buffer_size: An optional integer specifying the max number of lines in content.
    """

    def __init__(self, buffer_size=None):
        """
        Initializes the console window with an optional buffer size.
        Args:
            buffer_size (int or str, optional): Maximum number of lines to keep in the content.
                                                 If 'auto', adjusts buffer to content area size.
                                                 If None, the content is not limited.
        """
        self.stdscr = uc.initscr()
        self.content = []
        self.scroll_position = 0
        self.background_thread = threading.Thread(target=self.worker_task, daemon=True)
        self.status_text = "Status: Initializing"
        self.quit_message = "Press Q to quit"
        self.auto_buffer = buffer_size == 'auto'
        self.buffer_size = None if self.auto_buffer else buffer_size
        self.__init_ui()

    def __init_ui(self):
        """Initializes UI components like window dimensions and input modes."""
        uc.start_color()
        uc.init_pair(1, uc.COLOR_WHITE, uc.COLOR_BLUE)
        uc.clear()
        self.height, self.width = uc.getmaxyx(self.stdscr)
        uc.noecho()
        uc.cbreak()
        uc.keypad(self.stdscr, True)
        uc.mousemask(uc.ALL_MOUSE_EVENTS)
        self.__setup_display_areas()
        if self.auto_buffer:
            self.buffer_size = self.displayable_content_lines

    def __setup_display_areas(self):
        """Configures display areas for content and the status bar."""
        self.title_row = 0
        self.status_row = self.height - 1
        self.content_start_row = 1
        self.content_end_row = self.status_row - 1
        uc.refresh()
        if self.auto_buffer:
            self.buffer_size = self.displayable_content_lines

    @property
    def displayable_content_lines(self):
        """Calculates displayable lines in the content area."""
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
        uc.mvaddstr(self.title_row, title_position, title,
                    uc.color_pair(1) | uc.A_BOLD)
        uc.refresh()

    def add_content(self, message: str):
        """
        Appends a message to the content, maintaining or adjusting buffer size if specified.
        Args:
            message (str): Text to add to the content area.
        """
        if self.buffer_size is not None and len(self.content) >= self.buffer_size:
            self.content.pop(0)
        self.content.append(message)
        self.__adjust_scroll_for_new_content()
        self.__update_content_window()

    def __adjust_scroll_for_new_content(self):
        """Adjusts the scroll position for new content, if necessary."""
        if len(self.content) > self.displayable_content_lines:
            self.scroll_position = len(self.content) - self.displayable_content_lines

    def set_status(self, status: str):
        """
        Updates the status bar text.

        Args:
            status (str): New status message.
        """
        uc.move(self.status_row, 0)
        uc.clrtoeol()
        uc.mvaddstr(self.status_row, 0, " " * self.width, uc.color_pair(1))
        uc.mvaddstr(self.status_row, 0, status, uc.color_pair(1) | uc.A_BOLD)
        quit_msg_pos = self.width - len(self.quit_message)
        uc.mvaddstr(self.status_row, quit_msg_pos, self.quit_message,
                    uc.color_pair(1) | uc.A_BOLD)
        uc.refresh()

    def __update_content_window(self):
        """Redraws the content area with current content and scroll position."""
        uc.move(self.content_start_row, 0)
        uc.clrtobot()
        content_to_display = self.content[self.scroll_position:
                                          self.scroll_position + self.displayable_content_lines]
        for i, line in enumerate(content_to_display):
            uc.mvaddstr(self.content_start_row + i, 0, line[:self.width])
        self.set_status(self.status_text)
        uc.refresh()

    def __scroll_content_up(self):
        """Scrolls content up by one line, if possible."""
        if self.scroll_position > 0:
            self.scroll_position -= 1
            self.__update_content_window()

    def __scroll_content_down(self):
        """Scrolls content down by one line if more content is available."""
        if self.scroll_position < len(self.content) - self.displayable_content_lines:
            self.scroll_position += 1
            self.__update_content_window()

    def worker_task(self):
        """
        Background task for dynamic content updates. Must be overridden in subclasses.
        """
        raise NotImplementedError("Override worker_task in a subclass.")

    def run(self):
        """Main event loop for handling user input and window updates."""
        self.background_thread.start()
        try:
            while True:
                ch = uc.getch()
                if ch == uc.KEY_MOUSE:
                    _, _, _, _, bstate = uc.getmouse()
                    if bstate & uc.BUTTON4_PRESSED:
                        self.__scroll_content_up()
                    elif bstate & uc.BUTTON5_PRESSED:
                        self.__scroll_content_down()
                elif ch in (ord('q'), ord('Q')):
                    break
        finally:
            uc.endwin()


if __name__ == '__main__':
    class ExampleConsoleWindow(ConsoleWindow):
        def __init__(self, buffer_size=None):
            """
            Initializes the ExampleConsoleWindow class with an optional buffer size.
            """
            super().__init__(buffer_size)

        def worker_task(self):
            """
            Example worker task showing dynamic content updates with a timer.
            """
            start_time = time.time()
            for count in range(1, 66):
                elapsed_time = int(time.time() - start_time)
                minutes, seconds = divmod(elapsed_time, 60)
                self.set_status(f"Running for {minutes}m {seconds}s.")
                time.sleep(0.1)
                self.add_content(f"Example content {count}")
            self.set_status("Status: Done")

    win = ExampleConsoleWindow()
    win.set_title("Example Console Output")
    win.set_status("Status: Running")
    win.run()
