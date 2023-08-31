#!/usr/bin/env python3

import argparse
import json
import logging
import threading

from scanners.trivy_scanner import TrivyScanner
from builders.vulnerability_data_builder import VulnerabilityDataBuilder
from generators.excel_report_generator import ExcelReportGenerator
from utils.utilities import generate_default_filename, keep_logging

def main():
    parser = argparse.ArgumentParser(description="Scan AWS configurations.")
    parser.add_argument("--output", help="Output report file name", type=str, default=None)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    output_filename = args.output if args.output else generate_default_filename()
    logging.info(f"Generating report to {output_filename}")

    data_raw = TrivyScanner.scan('aws')
    if data_raw:
        data_decoded = json.loads(data_raw)
        vuln_data = VulnerabilityDataBuilder.build(data_decoded)
        report_generator = ExcelReportGenerator(vuln_data, output_filename)
        report_generator.generate()
    else:
        logging.error("Failed to retrieve scan data.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Scanning started. Please wait...")
    t = threading.Thread(target=keep_logging)
    t.daemon = True
    t.start()
    main()
