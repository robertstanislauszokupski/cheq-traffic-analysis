"""
Master Analysis Runner
Executes the entire analysis pipeline in sequence
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name, description):
    """
    Run a Python script and handle errors
    
    Args:
        script_name: Name of the script file
        description: Human-readable description
        
    Returns:
        True if successful, False otherwise
    """
    print(f"\n{'='*80}")
    print(f"{description}")
    print('='*80)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True
        )
        
        if result.returncode != 0:
            print(f"\n{script_name} failed with return code {result.returncode}")
            return False
        
        print(f"\n{script_name} completed successfully")
        return True
        
    except Exception as e:
        print(f"\nError running {script_name}: {e}")
        return False

def main():
    """Execute the full analysis pipeline"""
    print("="*80)
    print("CHEQ ANALYSIS - MASTER PIPELINE")
    print("="*80)
    print("\nThis will run the complete analysis workflow:")
    print("  1. Verify database schema")
    print("  2. Run core analysis queries")
    print("  3. Export core results to CSV")
    print("  4. Export advanced analysis to CSV")
    print("  5. Generate visualizations")
    print("\nNote: Data import (import_data.py) is not included - run manually if needed")
    print("Note: Cost calculator (cost_calculator.py) is interactive - run manually")
    
    response = input("\nContinue? (y/n): ").lower()
    if response != 'y':
        print("Pipeline cancelled.")
        return
    
    # Define pipeline steps
    pipeline = [
        ('verify_schema.py', 'Step 1: Verifying Database Schema'),
        ('run_analysis.py', 'Step 2: Running Core Analysis Queries'),
        ('export_results.py', 'Step 3: Exporting Core Results to CSV'),
        ('export_advanced.py', 'Step 4: Exporting Advanced Analysis to CSV'),
        ('create_visualizations.py', 'Step 5: Generating Visualizations'),
    ]
    
    # Execute pipeline
    for script, description in pipeline:
        if not run_script(script, description):
            print("\n" + "="*80)
            print("PIPELINE FAILED")
            print("="*80)
            print(f"The pipeline stopped at: {script}")
            print("Please fix any errors and run again.")
            sys.exit(1)
    
    # Success!
    print("\n" + "="*80)
    print("PIPELINE COMPLETE")
    print("="*80)
    print("\nAll analysis steps completed successfully!")
    print("\nGenerated outputs:")
    print("  - CSV files in outputs/")
    print("  - Visualizations in outputs/visualizations/")
    print("\nNext steps:")
    print("  - Run cost_calculator.py for ROI analysis (interactive)")
    print("  - Review outputs/ directory for all results")

if __name__ == '__main__':
    main()
