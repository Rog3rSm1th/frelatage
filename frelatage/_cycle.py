from frelatage.report.report import Report


def run_function(self, arguments: list, result: list) -> bool:
    """
    Run a function inside the tracer and return a report
    """
    trace = self.tracer.trace(self.method, arguments)

    trace_instructions = set(
        [instruction for instruction in trace.reached_instructions]
    )
    trace_instruction_pairs = set([pair for pair in trace.instructions_pairs])

    trace_instructions_count = len(trace_instructions)
    trace_instruction_pairs_count = len(trace_instruction_pairs)

    new_instructions_count = len(trace_instructions - self.reached_instructions)
    new_sequences_count = len(trace_instruction_pairs - self.instructions_pairs)

    new_instruction_error = trace.error_position not in self.error_positions

    run_report = Report(
        trace,
        arguments,
        trace.error,
        trace.timeout,
        new_instruction_error,
        trace_instructions_count,
        new_instructions_count,
        trace_instruction_pairs_count,
        new_sequences_count,
    )
    result.append(run_report)
    return True


def run_cycle(self) -> list[Report]:
    """
    run the function with each mutation of the cycle as argument.
    Return the execution reports.
    """
    cycle_reports = []

    # TODO: Implement multithreading
    for mutation in self.cycle:
        self.run_function(mutation, cycle_reports)
        self.inputs_count += 1
        self.last_seconds_executions += 1
        self.stage_inputs_count += 1
    self.cycles_count += 1
    return cycle_reports
