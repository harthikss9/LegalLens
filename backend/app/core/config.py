"""
Configuration file for LegalLens API application
"""
import os
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables from .env file
load_dotenv()

# NVIDIA API Configuration
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "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")
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")

# Application Configuration
APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = int(os.getenv("APP_PORT", "8001"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Safe clause templates
SAFE_TEMPLATES: List[Dict[str, str]] = [
  {"topic":"confidentiality", "text":"Each party shall keep all confidential information private and use it solely for contractual purposes."},
  {"topic":"termination",     "text":"Either party may terminate this agreement with thirty (30) days' written notice for reasonable cause."},
  {"topic":"liability",       "text":"Liability is limited to direct damages and shall not exceed the total contract value paid under this agreement."},
  {"topic":"indemnity",       "text":"Each party shall indemnify and hold the other harmless for losses arising from its own breach or negligence."},
  {"topic":"governing_law",   "text":"This agreement shall be governed by and construed in accordance with the laws of California, without regard to conflicts of law."},
  {"topic":"payment_terms",   "text":"Invoices are due within thirty (30) days of receipt; late payments may incur interest at the lesser of 1.5% per month or the maximum allowed by law."},
  {"topic":"ip_ownership",    "text":"Each party retains ownership of its pre-existing IP. Deliverables created under this agreement are owned by Company upon full payment, subject to licensor's background IP."},
  {"topic":"data_protection", "text":"Parties will implement reasonable administrative, technical, and physical safeguards to protect personal data and will process such data only for the purposes of this agreement."},
  {"topic":"subcontracting",  "text":"Contractor may not subcontract material obligations without prior written consent; Contractor remains fully responsible for subcontractors' performance."},
  {"topic":"warranty",        "text":"Contractor warrants that services will be performed in a professional and workmanlike manner in accordance with industry standards for ninety (90) days."}
]
