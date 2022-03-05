from frelatage.colors import Colors
from datetime import datetime
from string import Formatter
from curses import wrapper
import curses
import time
import os

# Refresh the interface 10 times/second
REFRESH_INTERVAL = 0.1

def format_delta(time_delta:datetime, format: str) -> str:
    """
    Format a time delta.
    """
    formatter = Formatter()
    digits = {}
    constants = {'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
    k = map(lambda x: x[1], list(formatter.parse(format)))
    remaining = int(time_delta.total_seconds())

    for i in ('D', 'H', 'M', 'S'):
        if i in k and i in constants.keys():
            digits[i], remaining = divmod(remaining, constants[i])

    return formatter.format(format, **digits)

def format_time_elapsed(datetime: datetime) -> str:
    """
    Format the time elapsed since a datetime in the format : 
    {D} days, {H} hrs, {M} min, {S} sec
    """
    if datetime is not None:
        format_time_delta = datetime.now() - datetime
        format_time = format_delta(format_time_delta, "{D} days, {H} hrs, {M} min, {S} sec")
    # If the event has not yet occurred
    else:
        format_time = "none seen yet" 
    return format_time

def init_interface(self, stdscr) -> bool:
    """
    Initialize the Frelatage CLI
    """
    # Hide cursor
    curses.curs_set(0)
    # Colors
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)

    self.screen = stdscr
    self.screen.clear()
    self.screen.refresh()
    return True

def refresh_interface(self):
    """
    Refresh the Frelatage CLI
    """
    # Process timing
    run_time = format_time_elapsed(self.fuzz_start_time).ljust(32)
    last_new_path_time = format_time_elapsed(self.last_new_path_time).ljust(32)
    last_unique_crash_time = format_time_elapsed(self.last_unique_crash_time).ljust(32)
    last_unique_timeout_time = format_time_elapsed(self.last_unique_timeout_time).ljust(32)
    
    # Overall results
    uniques_crashes_count = str(self.unique_crashes).ljust(32)
    uniques_timeouts_count = str(self.unique_timeout).ljust(32)

    # Finding in depth 
    total_paths_count = str(len(self.reached_instructions)).ljust(20)
    favored_paths_count = len(self.favored_pairs)
    favored_paths_rate = round(int(favored_paths_count)/int(total_paths_count) * 100, 2) if int(total_paths_count) else 0.00
    favored_paths = "{favored_paths} ({rate}%)".format(favored_paths=favored_paths_count, rate=favored_paths_rate).ljust(20)
    
    # Crashes
    total_crashes = "{crashes} ({uniques} uniques)".format(crashes=str(self.total_crashes), uniques=str(self.unique_crashes)).ljust(20)
    total_timeouts = "{total_timeouts}".format(total_timeouts=self.total_timeouts).ljust(20)

    # Progress
    cycles_count = str(self.cycles_count).ljust(20)
    total_executions = str(self.inputs_count).ljust(20)

    # Interface
    self.screen.addstr(0, 0, """
    Frelatage {version} ({function_name})

    [>] Process timing                                           [>] Finding in depth
    +--------------------------------------------------------+   +--------------------------------------------+
    | Run time            :: {run_time}|   | Favored paths       :: {favored_paths}|
    | Last new path       :: {last_new_path_time}|   | Total paths         :: {total_paths_count}|
    | Last unique crash   :: {last_unique_crash_time}|   | Total timeouts      :: {total_timeouts}|
    | Last unique timeout :: {last_unique_timeout_time}|   | Total crashes       :: {total_crashes}|
    +--------------------------------------------------------+   +--------------------------------------------+

    [>] Overall result                                           [>] Progress
    +--------------------------------------------------------+   +--------------------------------------------+
    | Uniques crashes     :: {uniques_crashes_count}|   | Cycles done         :: {cycles_count}|
    | Unique timeouts     :: {uniques_timeouts_count}|   | Total executions    :: {total_executions}|
    +--------------------------------------------------------+   +--------------------------------------------+
    """.format(
            version=self.version,
            function_name=self.method.__name__,
            run_time=run_time,
            last_new_path_time=last_new_path_time,
            last_unique_crash_time=last_unique_crash_time,
            last_unique_timeout_time=last_unique_timeout_time,
            uniques_crashes_count=uniques_crashes_count,
            uniques_timeouts_count=uniques_timeouts_count,
            favored_paths=favored_paths,
            total_paths_count=total_paths_count,
            total_timeouts=total_timeouts,
            total_crashes=total_crashes,
            cycles_count=cycles_count,
            total_executions=total_executions
        )
    )
    self.screen.refresh()

def exit_message(self, aborted_by_user: bool) -> bool:
    """
    Message displayed when exiting the program
    """
    run_time = format_time_elapsed(self.fuzz_start_time)
    uniques_crashes_count = str(self.unique_crashes)
    uniques_timeouts_count = str(self.unique_timeout)
    total_crashes = "{crashes} ({uniques} uniques)".format(crashes=str(self.total_crashes), uniques=str(self.unique_crashes))
    total_timeouts = "{total_timeouts}".format(total_timeouts=self.total_timeouts)
    total_paths_count = str(len(self.reached_instructions))
    cycles_count = str(self.cycles_count)
    total_executions = str(self.inputs_count)

    # End the curse window 
    if not self.silent:
        curses.endwin()

    # Keyboard interrupt
    if aborted_by_user:
        print(Colors.FAIL + "+++ Fuzzing aborted by user +++" + "\r\n")
    # Error in the program
    else:
        print(Colors.FAIL + "+++ Fuzzing was interrupted by an error in Frelatage +++" + "\r\n")
    
    # Message displayed at the end of the program 
    print(Colors.OKGREEN + "[+] " + Colors.ENDC + "Error reports are located in: " + Colors.BOLD + self.output_directory + Colors.ENDC + "\r\n"
          + "\r\n"
          + Colors.BOLD + "Fuzzing statistics: " + Colors.ENDC + "\r\n"
          + "\r\n"
          + "Total run time: " + run_time + "\r\n"
          + "Uniques crashes: " + Colors.FAIL + uniques_crashes_count + Colors.ENDC + "\r\n"
          + "Uniques timeouts: " + uniques_timeouts_count + "\r\n"
          + "Crashes: " + str(self.total_crashes) + "\r\n"
          + "Timeouts: " + total_timeouts + "\r\n"
          + "Reached paths: " + total_paths_count + "\r\n"
          + "Cycles: " + cycles_count + "\r\n"
          + "Executions: " + total_executions
          )
    return True

def start_interface(self):
    """
    Display the curse interface
    """
    wrapper(self.init_interface)
    while True:
        self.refresh_interface()
        time.sleep(REFRESH_INTERVAL)