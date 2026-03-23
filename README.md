# spiderOfweb

This is a multi-platform web crawler package project, mainly intended for learning and researching common data collection workflows.

## Project Introduction

This project encapsulates data scraping functions for multiple websites and apps, including the following:

- Reading and writing proxy IPs
- Vehicle information collection from Dongchedi / related automotive apps
- Information collection from Xiaohongshu
- Data scraping from some Chinese websites
- Simple OCR captcha recognition and database encapsulation

## Features

- Supports data collection from multiple websites and platforms
- Uses automation tools for page operations
- Supports asynchronous requests to improve scraping efficiency
- Integrates proxy IPs for different network environments
- Some modules are already encapsulated and can be further developed based on your needs

## Dependencies

This project mainly uses the following Python libraries:

### Standard Libraries
- `csv`: for reading and writing CSV files
- `json`: for processing JSON data
- `os`: for file and path operations
- `random`: for generating random parameters or selections
- `re`: for regular expression matching
- `hashlib`: for MD5 and other hash calculations
- `asyncio`: for asynchronous task scheduling

### Network Request Libraries
- `requests`: for sending synchronous HTTP requests
- `aiohttp`: for sending asynchronous HTTP requests
- `aiohttp_socks`: for proxy connection configuration
- `retrying`: for automatic retry on failed requests
- `fake_useragent`: for generating random User-Agent headers

### Data Parsing Libraries
- `jsonpath`: for extracting target fields from JSON data
- `lxml`: for parsing HTML / XML page content

### Automation and Browser Control
- `DrissionPage`: for browser automation and page control

### OCR and Image Processing
- `ddddocr`: for captcha recognition
- `Pillow (PIL)`: for image processing
- `fontTools`: for font file processing and parsing

## Installation

You can install the main third-party dependencies used in this project with:

```bash
pip install requests fake-useragent jsonpath lxml retrying aiohttp aiohttp-socks DrissionPage fonttools ddddocr pillow

Usage Notes
Some encapsulated modules have relatively long default waiting times, which can be adjusted according to your actual needs
Since website structures and interfaces may change frequently, some functions may become invalid after a short period of time
If the target websites update too quickly, the current code may no longer remain compatible
Before use, please check proxy settings, request headers, waiting times, and target parameters according to your actual requirements
Notes

This project is intended მხოლოდ for learning and technical communication. Please do not use it for any illegal or unauthorized purposes.

The code is provided for reference only. Some functions may only remain valid for a short time. Because some websites update very quickly, this project does not guarantee continuous maintenance or updates. Thank you for your understanding.

Disclaimer

This project is for learning, research, and technical communication only. Please use it in compliance with relevant laws, regulations, and the rules of the target websites. Any consequences resulting from the use of this project shall be borne by the user.



