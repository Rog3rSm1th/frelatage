from threading import Thread

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
            parents = self.evaluate_mutations(reports)
    # Exit the program
    # Keyboard interrupt
    except KeyboardInterrupt:
        self.exit_message(aborted_by_user=True)
        exit(0)
    # Error in Frelatage
    except Exception:
        self.exit_message(aborted_by_user=False)
        exit(1)