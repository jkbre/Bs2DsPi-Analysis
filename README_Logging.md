# Logging Integration with Printter

<!--
=============================================================================
Section edited with AI
=============================================================================
-->

This implementation adds comprehensive logging functionality to your analysis workflow that integrates seamlessly with your existing `Printter` class.

## Features

The `Loggerr` class provides:

1. **File Processing Logging**: Records what files are being processed
2. **Cut Logging**: Documents what cuts are being applied to which decay types
3. **Event Count Logging**: Tracks events before/after cuts with efficiency calculations
4. **Role-based Logging**: Distinguishes between numerator and denominator data
5. **Console Integration**: Works with your `Printter` class for colored console output
6. **Session Tracking**: Maintains analysis session data in memory for easy access

## Quick Start

```python
from lib.pyfinder import Printter, Loggerr

# Initialize
p = Printter(verbose=True)
logger = Loggerr(printter=p)  # Auto-generates timestamped log file

# Log file processing
logger.log_file_processing(
    file_path="/path/to/data.root",
    decay_type="Bs2DsPi/MC",
    year=2015,
    mode="Up"
)

# Log cuts
cuts = {
    "eta_cut": "lab0_ETA > 2.0 && lab0_ETA < 5.0",
    "mass_cut": "lab2_MM >= 1948 && lab2_MM <= 1988"
}
logger.log_cuts_applied(cuts, "Bs2DsPi/MC")

# Log event counts
logger.log_event_counts(
    decay_type="Bs2DsPi/MC",
    year=2015,
    before_cuts=150000,
    after_cuts=45000,
    role="numerator"  # or "denominator"
)

# Generate analysis summary
logger.log_analysis_summary()
```

## Integration with Your Analysis

The logging has been integrated into your `beginning.ipynb` notebook in the following cells:

1. **Initialization Cell**: Creates logger instance with printter integration
2. **Analysis Loop**: Automatically logs:
   - Each file being processed
   - Cuts applied to each decay type
   - Event counts before/after cuts
   - Role identification (numerator/denominator)
3. **Summary Cell**: Displays log file location and analysis summary

## Log File Format

The log file contains timestamped entries with different levels:

```
=== Analysis Log ===
Log started: 2025-06-04 10:30:15
Working directory: /home/jade/GitHub/the-respected-daimyo/src/projects/Bs2DsPi/src/Bs2DsPi-Analysis
Log file: /home/jade/GitHub/the-respected-daimyo/src/projects/Bs2DsPi/src/Bs2DsPi-Analysis/analysis_log_20250604_103015.log
==================================================

[2025-06-04 10:30:15] [INFO] Starting analysis processing
[2025-06-04 10:30:15] [FILE] Processing file: /path/to/data.root | Decay: Bs2DsPi/MC | Year: 2015 | Mode: Up
[2025-06-04 10:30:15] [CUTS] Applying cuts for Bs2DsPi/MC:
[2025-06-04 10:30:15] [CUTS]   eta_cut: lab0_ETA > 2.0 && lab0_ETA < 5.0
[2025-06-04 10:30:15] [COUNTS] Event counts - Bs2DsPi/MC (2015) [numerator]: Before cuts: 150000, After cuts: 45000, Efficiency: 0.3000
```

## Accessing Session Data

The logger maintains session data that you can access programmatically:

```python
# Access files processed
for file_info in logger.session_data['files_processed']:
    print(f"Processed: {file_info['path']} ({file_info['decay_type']})")

# Access event counts by role
for key, counts in logger.session_data['event_counts'].items():
    if counts['role'] == 'numerator':
        print(f"Numerator: {counts['after_cuts']} events")
```

## Custom Log File Location

```python
# Specify custom log file location
logger = Loggerr(log_file="my_analysis.log", printter=p)

# Or use default timestamped file
logger = Loggerr(printter=p)  # Creates analysis_log_YYYYMMDD_HHMMSS.log
```

## Running the Example

To see the logging in action, run the example script:

```bash
cd /home/jade/GitHub/the-respected-daimyo/src/projects/Bs2DsPi/src/Bs2DsPi-Analysis
python example_logging.py
```

This will demonstrate all logging features and create an example log file.

## Requirements Answered

The implementation answers all your requirements:

1. ✅ **What file are you using?** - Logged via `log_file_processing()`
2. ✅ **What cuts are being applied?** - Logged via `log_cuts_applied()`
3. ✅ **How many events before cuts?** - Logged via `log_event_counts()`
4. ✅ **How many after cuts for denominator?** - Logged with `role="denominator"`
5. ✅ **How many after cuts for numerator?** - Logged with `role="numerator"`

The logging integrates with your existing `Printter` class for colored console output while maintaining detailed file logs for later analysis.

<!--
=============================================================================
End of section edited with AI
=============================================================================
-->
