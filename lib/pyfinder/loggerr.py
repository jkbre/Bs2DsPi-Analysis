# =============================================================================
# Section edited with AI
# =============================================================================
# Version 0.1.0
"""
Loggerr class for Python scripts applications.
Integrates with Printter for file logging and analysis tracking.
"""
import datetime
import os
from pathlib import Path
from typing import Optional, Dict, Any, List


class Loggerr:
    """
    A logging class that works with Printter to log analysis information to files.
    Specifically designed to track:
    - Files being processed
    - Cuts being applied
    - Event counts before/after cuts
    - Analysis metadata
    """

    def __init__(self, log_file: Optional[str] = None, printter=None, auto_timestamp: bool = True):
        """
        Initialize the Loggerr class object.
        ---
        Parameters:
            log_file (str, optional): Path to log file. If None, creates default log file.
            printter (Printter, optional): Printter instance for console output
            auto_timestamp (bool): Whether to automatically add timestamps to log entries
        Returns:
            None
        """
        self.printter = printter
        self.auto_timestamp = auto_timestamp

        # Set up log file
        if log_file is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_file = Path(f"analysis_log_{timestamp}.log")
        else:
            self.log_file = Path(log_file)

        # Ensure log directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Initialize log file with header
        self._initialize_log()

        # Storage for analysis session data
        self.session_data = {
            "files_processed": [],
            "cuts_applied": {},
            "event_counts": {},
            "analysis_start_time": datetime.datetime.now(),
        }

    def _initialize_log(self):
        """Initialize the log file with header information."""
        header = f"""
=== Analysis Log ===
Log started: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Working directory: {os.getcwd()}
Log file: {self.log_file.absolute()}
{'='*50}

"""
        with open(self.log_file, "w") as f:
            f.write(header)

    def _get_timestamp(self) -> str:
        """Get formatted timestamp string."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _write_to_log(self, message: str, level: str = "INFO"):
        """Write message to log file with optional timestamp."""
        if self.auto_timestamp:
            log_entry = f"[{self._get_timestamp()}] [{level}] {message}\n"
        else:
            log_entry = f"[{level}] {message}\n"

        with open(self.log_file, "a") as f:
            f.write(log_entry)

    def log_file_processing(self, file_path: str, decay_type: str = "", year: int = None, mode: str = ""):
        """
        Log file being processed.

        Parameters:
            file_path (str): Path to the file being processed
            decay_type (str): Type of decay (e.g., "Bs2DsPi/MC")
            year (int): Year of data
            mode (str): Mode (e.g., "Up", "Down")
        """
        message = f"Processing file: {file_path}"
        if decay_type:
            message += f" | Decay: {decay_type}"
        if year:
            message += f" | Year: {year}"
        if mode:
            message += f" | Mode: {mode}"

        self._write_to_log(message, "FILE")
        self.session_data["files_processed"].append(
            {"path": file_path, "decay_type": decay_type, "year": year, "mode": mode, "timestamp": self._get_timestamp()}
        )

        # Also print to console if printter is available
        if self.printter:
            self.printter.iprint("Processing file:", file_path, order=1, colors="cyan")
            if decay_type or year or mode:
                details = f"Decay: {decay_type}, Year: {year}, Mode: {mode}"
                self.printter.iprint(details, order=2, colors="blue")

    def log_cuts_applied(self, cuts: Dict[str, str], decay_type: str = ""):
        """
        Log the cuts being applied to the data.

        Parameters:
            cuts (dict): Dictionary of cut names and cut expressions
            decay_type (str): Type of decay these cuts apply to
        """
        message = f"Applying cuts for {decay_type}:"
        self._write_to_log(message, "CUTS")

        for cut_name, cut_expr in cuts.items():
            cut_message = f"  {cut_name}: {cut_expr}"
            self._write_to_log(cut_message, "CUTS")

        # Store cuts in session data
        self.session_data["cuts_applied"][decay_type] = cuts

        # Also print to console if printter is available
        if self.printter:
            self.printter.iprint(f"Applying cuts for {decay_type}:", order=1, colors="yellow")
            for cut_name, cut_expr in cuts.items():
                self.printter.iprint(f"{cut_name}: {cut_expr}", order=2, colors="green")

    def log_event_counts(
        self, decay_type: str, year: int, before_cuts: int, after_cuts: int, efficiency: float = None, role: str = ""
    ):
        """
        Log event counts before and after cuts.

        Parameters:
            decay_type (str): Type of decay
            year (int): Year of data
            before_cuts (int): Number of events before cuts
            after_cuts (int): Number of events after cuts
            efficiency (float): Cut efficiency (before/after)
            role (str): Role in analysis ("numerator", "denominator", etc.)
        """
        if efficiency is None:
            efficiency = after_cuts / before_cuts if before_cuts > 0 else 0.0

        message = f"Event counts - {decay_type} ({year})"
        if role:
            message += f" [{role}]"
        message += f": Before cuts: {before_cuts}, After cuts: {after_cuts}, Efficiency: {efficiency:.4f}"

        self._write_to_log(message, "COUNTS")

        # Store in session data
        key = f"{decay_type}_{year}"
        if role:
            key += f"_{role}"

        self.session_data["event_counts"][key] = {
            "decay_type": decay_type,
            "year": year,
            "before_cuts": before_cuts,
            "after_cuts": after_cuts,
            "efficiency": efficiency,
            "role": role,
            "timestamp": self._get_timestamp(),
        }

        # Also print to console if printter is available
        if self.printter:
            color_map = {"numerator": "green", "denominator": "blue", "": "cyan"}
            color = color_map.get(role.lower(), "cyan")

            self.printter.iprint(f"Event counts - {decay_type} ({year})", order=1, colors=color)
            if role:
                self.printter.iprint(f"Role: {role}", order=2, colors=color)
            self.printter.iprint(f"Before cuts: {before_cuts}", order=2, colors=color)
            self.printter.iprint(f"After cuts: {after_cuts}", order=2, colors=color)
            self.printter.iprint(f"Efficiency: {efficiency:.4f}", order=2, colors=color)

    def log_analysis_summary(self):
        """Log a summary of the entire analysis session."""
        summary_header = f"\n{'='*50}\nANALYSIS SUMMARY\n{'='*50}"
        self._write_to_log(summary_header, "SUMMARY")

        # Files processed
        self._write_to_log(f"Total files processed: {len(self.session_data['files_processed'])}", "SUMMARY")
        for file_info in self.session_data["files_processed"]:
            file_summary = f"  {file_info['path']} ({file_info['decay_type']}, {file_info['year']}, {file_info['mode']})"
            self._write_to_log(file_summary, "SUMMARY")

        # Cuts applied
        self._write_to_log(f"Cuts applied to {len(self.session_data['cuts_applied'])} decay types:", "SUMMARY")
        for decay_type, cuts in self.session_data["cuts_applied"].items():
            self._write_to_log(f"  {decay_type}: {len(cuts)} cuts", "SUMMARY")

        # Event counts
        self._write_to_log(f"Event count records: {len(self.session_data['event_counts'])}", "SUMMARY")
        for key, counts in self.session_data["event_counts"].items():
            count_summary = f"  {key}: {counts['before_cuts']} -> {counts['after_cuts']} (eff: {counts['efficiency']:.4f})"
            self._write_to_log(count_summary, "SUMMARY")

        # Analysis duration
        duration = datetime.datetime.now() - self.session_data["analysis_start_time"]
        self._write_to_log(f"Analysis duration: {duration}", "SUMMARY")

        end_footer = f"{'='*50}\nAnalysis completed: {self._get_timestamp()}\n{'='*50}\n"
        self._write_to_log(end_footer, "SUMMARY")

        # Also print summary to console if printter is available
        if self.printter:
            self.printter.iprint("Analysis Summary:", order=0, colors="red")
            self.printter.iprint(f"Files processed: {len(self.session_data['files_processed'])}", order=1, colors="cyan")
            self.printter.iprint(f"Decay types with cuts: {len(self.session_data['cuts_applied'])}", order=1, colors="cyan")
            self.printter.iprint(f"Event count records: {len(self.session_data['event_counts'])}", order=1, colors="cyan")
            self.printter.iprint(f"Analysis duration: {duration}", order=1, colors="cyan")
            self.printter.iprint(f"Log saved to: {self.log_file.absolute()}", order=1, colors="green")

    def log_custom(self, message: str, level: str = "INFO"):
        """Log a custom message."""
        self._write_to_log(message, level)

        if self.printter:
            color_map = {"ERROR": "red", "WARNING": "yellow", "INFO": "blue", "DEBUG": "cyan"}
            color = color_map.get(level, "blue")
            self.printter.iprint(f"[{level}] {message}", order=0, colors=color)

    def get_log_path(self) -> Path:
        """Return the path to the log file."""
        return self.log_file.absolute()


# =============================================================================
# End of section edited with AI
# =============================================================================
