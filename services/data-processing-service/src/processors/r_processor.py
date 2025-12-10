"""
R Script Processor
Executes R scripts using rpy2
"""

import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import os
import asyncio
import subprocess
import logging

logger = logging.getLogger(__name__)

# Activate pandas conversion
pandas2ri.activate()

class RProcessor:
    """Process R scripts for data consolidation and analysis"""

    def __init__(self):
        self.script_dir = os.path.join(os.path.dirname(__file__), '../../../../scripts/reporting')
        logger.info(f"R Processor initialized with script directory: {self.script_dir}")

    async def run_consolidation_script(self, state: str = None, output_format: str = "csv"):
        """
        Run consolidate_license_findings_simple.R script
        """
        script_path = os.path.join(self.script_dir, 'consolidate_license_findings_simple.R')

        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script not found: {script_path}")

        try:
            # Run R script using subprocess (more reliable than rpy2 for complex scripts)
            cmd = ['Rscript', script_path]
            if state:
                cmd.extend(['--state', state])
            if output_format:
                cmd.extend(['--format', output_format])

            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.path.dirname(script_path)
            )

            stdout, stderr = await result.communicate()

            if result.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"R script failed: {error_msg}")
                raise RuntimeError(f"R script execution failed: {error_msg}")

            output = stdout.decode() if stdout else ""
            logger.info(f"R script completed successfully")

            return {
                "success": True,
                "output": output,
                "script": "consolidate_license_findings_simple.R"
            }

        except Exception as e:
            logger.error(f"Error running R script: {e}")
            raise

    async def run_letter_generation_script(self, states: list, output_dir: str = None):
        """
        Run generate_complaint_letters.R script
        """
        script_path = os.path.join(self.script_dir, 'generate_complaint_letters.R')

        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script not found: {script_path}")

        try:
            cmd = ['Rscript', script_path]
            if states:
                cmd.extend(['--states'] + states)
            if output_dir:
                cmd.extend(['--output-dir', output_dir])

            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.path.dirname(script_path)
            )

            stdout, stderr = await result.communicate()

            if result.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"R script failed: {error_msg}")
                raise RuntimeError(f"R script execution failed: {error_msg}")

            output = stdout.decode() if stdout else ""
            logger.info(f"Letter generation completed for states: {states}")

            return {
                "success": True,
                "output": output,
                "states": states,
                "script": "generate_complaint_letters.R"
            }

        except Exception as e:
            logger.error(f"Error running letter generation script: {e}")
            raise

    def execute_r_code(self, r_code: str):
        """
        Execute R code directly using rpy2
        """
        try:
            result = ro.r(r_code)
            return result
        except Exception as e:
            logger.error(f"Error executing R code: {e}")
            raise
