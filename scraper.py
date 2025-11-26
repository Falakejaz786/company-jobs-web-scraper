import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

df = pd.read_excel("Growth For Impact Data Assignment (1).xlsx")

COMMON_TLDS = ["com", "org", "net", "io", "co", "ai"]

def normalize(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

def guess_company_website(company_name):
    base = normalize(company_name)
    for tld in COMMON_TLDS:
        for prefix in ['', 'www.']:
            url = f"https://{prefix}{base}.{tld}"
            try:
                response = requests.head(url, timeout=3)
                if response.status_code in (200, 301, 302):
                    return url
            except:
                continue
    return None

def find_careers_page(website):
    if not website:
        return None
    try:
        response = requests.get(website, timeout=3)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            if any(x in href for x in ['career', 'job', 'join-us', 'work-with-us']):
                return href if href.startswith('http') else website.rstrip('/') + '/' + href.lstrip('/')
    except:
        return None

def scrape_jobs(careers_page):
    jobs = []
    if not careers_page:
        return jobs
    try:
        response = requests.get(careers_page, timeout=3)
        soup = BeautifulSoup(response.text, 'html.parser')
        job_links = soup.find_all('a', href=True)[:3]
        for link in job_links:
            job_url = link['href'] if link['href'].startswith('http') else careers_page.rstrip('/') + '/' + link['href'].lstrip('/')
            job_title = link.get_text(strip=True)
            jobs.append({'Job URL': job_url, 'Job Title': job_title})
    except:
        pass
    return jobs

def check_link(url):
    try:
        r = requests.head(url, timeout=3, allow_redirects=True)
        return r.status_code < 400
    except:
        return False

def process_company(row):
    result = {'Company Name': row['Company Name'], 'Website': None, 'Website Valid': False,
              'Careers Page': None, 'Careers Valid': False, 'Jobs': []}
    website = guess_company_website(row['Company Name'])
    if not website:
        return result
    result['Website'] = website
    result['Website Valid'] = check_link(website)
    careers = find_careers_page(website)
    result['Careers Page'] = careers
    result['Careers Valid'] = check_link(careers) if careers else False
    jobs = scrape_jobs(careers)
    for job in jobs:
        job['Valid'] = check_link(job['Job URL'])
    result['Jobs'] = jobs
    return result

results = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_company, row) for index, row in df.iterrows()]
    for future in as_completed(futures):
        results.append(future.result())

job_data = []
for res in results:
    for i, job in enumerate(res['Jobs']):
        job_data.append({
            'Company Name': res['Company Name'],
            'Website': res['Website'],
            'Website Valid': res['Website Valid'],
            'Careers Page': res['Careers Page'],
            'Careers Valid': res['Careers Valid'],
            f'Job{i+1} Title': job['Job Title'],
            f'Job{i+1} URL': job['Job URL'],
            f'Job{i+1} Valid': job['Valid']
        })

jobs_df = pd.DataFrame(job_data)

methodology_text = [
    ["Methodology"],
    ["1. Enriched company data using Python with requests and BeautifulSoup."],
    ["2. Guessed official websites using common TLDs (.com, .org, .net, .io, .co, .ai)."],
    ["3. Identified careers pages by searching for links containing 'career', 'job', 'join-us', 'work-with-us'."],
    ["4. Scraped up to 3 job postings per company (title + URL)."],
    ["5. Checked all URLs for validity automatically (valid=True, broken=False)."],
    ["6. Saved the final Excel with two sheets: Data (company/jobs) and Methodology (steps above)."]
]

with pd.ExcelWriter("companies_jobs_with_methodology_validated.xlsx", engine="openpyxl") as writer:
    jobs_df.to_excel(writer, sheet_name="Data", index=False)
    pd.DataFrame(methodology_text).to_excel(writer, sheet_name="Methodology", index=False, header=False)
