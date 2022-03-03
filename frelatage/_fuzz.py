from threading import Thread

def fuzz(self) -> None:
    """
    Run the fuzzer
    """
    # Interface
    p = Thread(target=self.start_interface)
    p.start()

    # Fuzzing
    parents = [self.arguments]
    while True: 
        self.generate_cycle_mutations(parents)
        reports = self.run_cycle()
        parents = self.evaluate_mutations(reports)