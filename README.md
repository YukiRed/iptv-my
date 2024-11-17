# IPTV Processing Script

This project contains a Python script to process IPTV `.m3u` playlist files from the [iptv-org/iptv](https://github.com/iptv-org/iptv) repository. The script:

- Downloads `.m3u` files listed in the repository's `README.md`.
- Cleans category names by removing unwanted symbols, spaces, and non-breaking spaces (`&nbsp;`).
- Checks the availability of stream links inside each `.m3u` file.
- Saves the results as separate `.m3u` files for available and unavailable links.

## Features

- **Category-Based Processing**: Processes `.m3u` playlist files grouped by categories like `News`, `Sports`, `Movies`, etc.
- **Name Sanitization**: Handles special characters, spaces, and non-breaking spaces in file names.
- **Output**: Generates two files for each playlist:
  - One containing available links.
  - One containing unavailable links.
- **Logging**: Includes detailed logs for debugging and monitoring.

---

## Folder Structure

```
.
├── m3u_files/           # Contains the raw `.m3u` files downloaded from the source.
├── processed/           # Contains the processed `.m3u` files.
│   ├── available_<category>.m3u
│   ├── unavailable_<category>.m3u
├── iptv_processing.log  # Log file with details about the script's execution.
└── process_iptv.py      # Main Python script.
```

---

## Prerequisites

- Python 3.x
- `requests` library

Install the required dependencies using:

```bash
pip install requests
```

---

## How to Use

1. Clone this repository:

   ```bash
   git clone https://github.com/YukiRed/iptv-my.git
   cd iptv-my
   ```

2. Run the script:

   ```bash
   python process_iptv.py
   ```

3. Find the results:
   - **Downloaded Files**: Located in the `m3u_files/` folder.
   - **Processed Results**: Available in the `processed/` folder:
     - `available_<category>.m3u`
     - `unavailable_<category>.m3u`

---

## Logging

Execution logs are saved in `iptv_processing.log` and include details about:

- Download progress.
- URL availability checks.
- Processing errors, if any.

---

## Contribution

Feel free to open issues or submit pull requests to improve this project. Contributions are welcome!

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

## Author

[Yuki Red](https://github.com/YukiRed)
