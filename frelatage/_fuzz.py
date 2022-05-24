from threading import Thread
from frelatage.config.config import Config


def fuzz(self) -> None:
    """
    Run the fuzzer
    """
    try:
        # Interface
        if not self.silent:
            p = Thread(target=self.start_interface)
            p.daemon = True
            p.start()

        # Fuzzing
        parents = [self.arguments]
        while True:
            self.generate_cycle_mutations(parents)
            reports = self.run_cycle()
            # If no new paths have been found for a while, we go to the next stage
            if (
                self.cycles_without_new_path
                >= Config.FRELATAGE_MAX_CYCLES_WITHOUT_NEW_PATHS
            ):
                # Next stage
                self.queue.position += 1
                if not self.queue.end:
                    # Initialize the new stage
                    self.arguments = self.queue.current_arguments()
                    parents = [self.arguments]
                    self.cycles_without_new_path = 0
                    self.stage_inputs_count = 0
                    self.init_file_inputs()
                # End of the fuzzing process
                # Exit the program
                else:
                    self.exit_message(normal_ending=True)
                    exit(1)
            else:
                parents = self.evaluate_mutations(reports)
    # Exit the program
    # Keyboard interrupt
    except KeyboardInterrupt:
        self.exit_message(aborted_by_user=True)
        exit(0)
    # Error in Frelatage
    except Exception as e:
        self.exit_message(aborted_by_user=False)
        if Config.FRELATAGE_DEBUG_MODE:
            print(e)
        exit(1)
