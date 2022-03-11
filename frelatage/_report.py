from frelatage.report.report import Report
import pickle
import os

def get_report_name(self, report: Report) -> str:
    """
    Generate a report title.
    The name of a report is in the following form:
    id<crash ID>,err<error type>
    """
    # It is assumed that the number of uniques crashes will not exceed 999999
    error_id = str(self.unique_crashes).zfill(6) 
    error_type = report.trace.error_type.lower()

    report_name = "id:{error_id},err:{error_type}".format(
        error_id=error_id,
        error_type=error_type
    )
    return report_name

def save_report(self, report) -> bool:
    """
    Save a report in the output directory (/out by default).
    The arguments passed to the function and the behavior of the function are stored
    in "input", the file inputs are stored in files ranging from 0 to n.
    The report directory is in the following form: 
    ├── out
    │   ├── id<crash ID>,err<error type>
    │       ├── input
    │       ├── <inputfile1>
    │       └── ...
    │   ├── ...
    """

    # The report contains the parameters passed to the function.
    custom_report = {
        "input": [dict(input) for input in report.input]
    }

    # /out by default
    base_directory = self.output_directory
    report_name = self.get_report_name(report)

    report_directory = "{base_directory}/{report_name}".format(base_directory=base_directory, report_name=report_name)

    # Create ./out/<report directory>/ directory if not exists
    if not os.path.exists(report_directory):
        os.makedirs(report_directory)
    
    # Save report file
    with open('{report_directory}/input'.format(report_directory=report_directory), 'wb+') as f:
        # We use pickle to store the report object
        pickle.dump(custom_report, f)

    # Save input files
    for argument in report.input:
        file_arguments_count = 0
        if argument.file:
            file_argument_content = open(argument.value, "rb").read()
            # Save file in /out/<report name>/<file name>
            filename = os.path.basename(argument.value)
            with open("{report_directory}/{filename}".format(report_directory=report_directory, filename=filename), "wb+") as f:
                f.write(file_argument_content)
    return True