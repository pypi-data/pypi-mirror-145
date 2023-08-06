#!/bin/bash
doxygen uts-doxygen.config

aws s3 cp generated_documentation/html/. s3://python.developer.ultratimeseries.com --recursive