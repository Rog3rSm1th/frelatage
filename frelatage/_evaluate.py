from datetime import datetime


def evaluate_mutations(self, reports: list) -> list:
    """
    Evaluates input reports and determines the number of unique bugs as well
    as the number of unique instruction bugs.
    Return the n mutations with the best score.
    """
    start_reached_instructions_count = len(self.reached_instructions)

    # Identify uniques crashes
    for report in reports:
        mutation_reached_instructions = set(report.trace.reached_instructions)
        mutation_instructions_pairs = set(report.trace.instructions_pairs)

        if report.error:
            self.total_crashes += 1
        if report.timeout:
            self.total_timeouts += 1

        # A crash  is unique if :
        # -> An error/timeout is triggered AND a new pair of instruction leading to a crash is found
        # OR
        # -> An error/timeout is triggered at a new position
        if report.error or report.timeout:

            new_error = False
            # We check if there are new instructions pairs
            if (report.new_error_instruction is not None) and (
                report.trace.error_position not in self.error_positions
            ):
                new_error = True
                # We update the list of instructions that led to a crash
                self.error_positions = set.union(
                    self.error_positions, [report.trace.error_position]
                )

            is_unique = (
                len(set.union(mutation_instructions_pairs, self.favored_pairs))
                != len(self.favored_pairs)
            ) or new_error
            # Unique bugs
            if is_unique:
                self.favored_pairs = set.union(
                    self.favored_pairs, mutation_instructions_pairs
                )
                self.last_unique_crash_time = datetime.now()
                self.save_report(report)
                self.unique_crashes += 1
                # Unique timeouts
                if report.timeout:
                    self.unique_timeout += 1
                    self.last_unique_timeout = datetime.now()

        # Update the list of global reached instructions and global instruction pairs
        self.reached_instructions = set.union(
            self.reached_instructions, mutation_reached_instructions
        )
        self.instructions_pairs = set.union(
            self.instructions_pairs, mutation_instructions_pairs
        )

    # If we found a new path
    if len(self.reached_instructions) > start_reached_instructions_count:
        self.last_new_path_time = datetime.now()
        self.cycles_without_new_path = 0
    else:
        self.cycles_without_new_path += 1

    # Rank reports
    ranked_reports = sorted(reports, reverse=True)

    # Select the best mutation
    best_mutations_count = int(self.threads_count * self.survival_probability)
    best_mutations = [
        mutation.input for mutation in ranked_reports[:best_mutations_count]
    ]
    return best_mutations
