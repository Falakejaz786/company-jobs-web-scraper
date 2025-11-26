# 📝 **README — Automated Job Discovery & Validation Pipeline**

## 📌 Overview

This project automatically identifies company websites, finds their careers pages, extracts job postings, and validates all URLs.
It processes large datasets efficiently using multithreading and outputs a clean, structured Excel file with:

* Company website
* Careers page
* Job titles & URLs
* Link validity checks
* A methodology sheet

This automation drastically reduces manual effort required for job data collection and validation.

---

## 🚀 Features

✔ **Automatic Website Guessing**
Constructs potential company URLs from their names using common TLDs (.com, .org, .net, .io, .co, .ai).

✔ **Careers Page Detection**
Scans website links for keywords such as `career`, `job`, `join-us`, `work-with-us`.

✔ **Job Extraction**
Scrapes up to **3 job postings per company** (title + URL).

✔ **Link Validation**
Checks whether every website, careers page, and job URL is actually reachable.

✔ **Multithreading for 10× Speed**
Uses `ThreadPoolExecutor` to process many companies in parallel (~2–3 minutes instead of 30 minutes).

✔ **Excel Output (2 Sheets)**

* `Data` → All company/job results
* `Methodology` → Steps followed for data collection

---

## 📁 Project Structure

```
project/
│── script.py
│── Growth For Impact Data Assignment.xlsx
│── companies_jobs_with_methodology_validated.xlsx
│── README.md
```

---

## 🛠️ Technologies Used

| Purpose            | Tools / Libraries       |
| ------------------ | ----------------------- |
| Web Scraping       | Requests, BeautifulSoup |
| Data Processing    | Pandas                  |
| Multithreading     | concurrent.futures      |
| File Export        | openpyxl                |
| URL Validation     | HTTP HEAD requests      |
| Logic & Automation | Python 3.8+             |

---

## 📥 Input

Upload an Excel file containing at least one column:

```
Company Name
```

Example:

| Company Name      |
| ----------------- |
| Accenture         |
| Growth For Impact |
| Patagonia         |

---

## 📤 Output

The script generates:

### `companies_jobs_with_methodology_validated.xlsx`

**Sheet 1 → Data**

* Company Name
* Website + validity
* Careers Page + validity
* Job1 Title, Job1 URL, Job1 Valid
* Job2 Title …
* Job3 Title …

**Sheet 2 → Methodology**
Plain-text documentation of how the data was generated.

---

## 🧠 Methodology Summary

1. Normalize company names for URL prediction
2. Generate possible domain names using common TLDs
3. Validate reachable websites
4. Scrape homepage and detect careers-related links
5. Scrape up to 3 jobs from each careers page
6. Validate each job link with HTTP HEAD
7. Run all companies in parallel for faster execution
8. Export structured output + methodology sheet

---

## ▶️ How to Run

### 1️⃣ Install Dependencies

```bash
pip install pandas requests beautifulsoup4 openpyxl
```

### 2️⃣ Place your input file in the same folder

```
Growth For Impact Data Assignment (1).xlsx
```

### 3️⃣ Run the script

```bash
python script.py
```

### 4️⃣ Find your output file

```
companies_jobs_with_methodology_validated.xlsx
```

---

## ⚡ Performance Notes

* ThreadPoolExecutor reduces processing from **~30 min to ~2–4 min**
* Timeout of 3 seconds per request keeps the script fast
* Heavy JS-based career pages may not always be detected (no Selenium used)

---

## 🧩 Limitations

* Careers pages loaded via JavaScript cannot be scraped fully.
* Only the **first 3 job links** are extracted (customizable).
* URL guessing depends on the company name being recognizable.

---
