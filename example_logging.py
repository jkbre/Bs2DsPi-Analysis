# =============================================================================
# Section edited with AI
# =============================================================================
#!/usr/bin/env python3
"""
Example script demonstrating the Loggerr class usage with Printter integration.
This shows how to log analysis information including files, cuts, and event counts.
"""

from lib.pyfinder import Printter, Loggerr
from pathlib import Path


def example_analysis_logging():
    """Example function showing how to use Loggerr for analysis logging."""

    # Initialize Printter and Loggerr
    p = Printter(verbose=True, devMode=False)
    logger = Loggerr(log_file="example_analysis.log", printter=p)

    # Example 1: Log custom messages
    logger.log_custom("Starting example analysis", "INFO")
    logger.log_custom("This is a warning message", "WARNING")

    # Example 2: Log file processing
    example_files = ["/path/to/Bs2DsPi_2015_Up.root", "/path/to/Bs2DsPi_2015_Down.root", "/path/to/Bs2DsPi_2016_Up.root"]

    for i, file_path in enumerate(example_files):
        year = 2015 if "2015" in file_path else 2016
        mode = "Up" if "Up" in file_path else "Down"
        logger.log_file_processing(file_path=file_path, decay_type="Bs2DsPi/MC", year=year, mode=mode)

    # Example 3: Log cuts being applied
    example_cuts = {
        "eta_cut": "lab0_ETA > 2.0 && lab0_ETA < 5.0",
        "rich_cut": "lab1_hasRich == 1",
        "mass_cut": "lab2_MM >= 1948 && lab2_MM <= 1988",
        "bdt_cut": "BDTGResponse_3 > 0.4",
    }

    logger.log_cuts_applied(example_cuts, "Bs2DsPi/MC")

    # Example 4: Log event counts
    # Simulate some event counts for demonstration
    example_counts = [
        {"year": 2015, "before": 150000, "after": 45000, "role": "numerator"},
        {"year": 2015, "before": 200000, "after": 75000, "role": "denominator"},
        {"year": 2016, "before": 180000, "after": 54000, "role": "numerator"},
        {"year": 2016, "before": 220000, "after": 88000, "role": "denominator"},
    ]

    for counts in example_counts:
        efficiency = counts["after"] / counts["before"]
        logger.log_event_counts(
            decay_type="Bs2DsPi/MC",
            year=counts["year"],
            before_cuts=counts["before"],
            after_cuts=counts["after"],
            efficiency=efficiency,
            role=counts["role"],
        )

    # Example 5: Log analysis summary
    logger.log_analysis_summary()

    # Example 6: Access session data programmatically
    print(f"\nSession Data Summary:")
    print(f"Files processed: {len(logger.session_data['files_processed'])}")
    print(f"Cuts applied to: {list(logger.session_data['cuts_applied'].keys())}")
    print(f"Event count records: {len(logger.session_data['event_counts'])}")

    # Example 7: Show log file location
    print(f"\nLog file saved to: {logger.get_log_path()}")

    return logger


if __name__ == "__main__":
    logger = example_analysis_logging()

    # Optional: Print the contents of the log file
    print(f"\n{'='*60}")
    print("LOG FILE CONTENTS:")
    print(f"{'='*60}")
    try:
        with open(logger.get_log_path(), "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Log file not found.")

# =============================================================================
# End of section edited with AI
# =============================================================================
