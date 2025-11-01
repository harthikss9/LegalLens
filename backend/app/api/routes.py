from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import tempfile, os
from app.core.config import NVIDIA_API_KEY, NVIDIA_BASE_URL, SAFE_TEMPLATES
from app.services.analyzer import Analyzer

router = APIRouter()

analyzer = None

def get_analyzer():
    global analyzer
    if analyzer is None:
        if not NVIDIA_API_KEY:
            raise HTTPException(status_code=500, detail='NVIDIA_API_KEY not set')
        analyzer = Analyzer(NVIDIA_API_KEY, NVIDIA_BASE_URL, SAFE_TEMPLATES)
    return analyzer

class ExtractResponse(BaseModel):
    document: str

class AnalyzeResponse(BaseModel):
    result: str

@router.post('/extract', response_model=ExtractResponse)
async def extract(file: UploadFile = File(...)):
    """Extract full document text from uploaded file."""
    if not file.filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail='Only PDF or TXT supported')
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        document = get_analyzer().extract_document(tmp_path)
        return ExtractResponse(document=document)
    finally:
        os.unlink(tmp_path)

@router.post('/analyze', response_model=AnalyzeResponse)
async def analyze_document(file: UploadFile = File(...)):
    """Analyze the entire uploaded document for risks and provide improvements."""
    if not file.filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail='Only PDF or TXT supported')
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        document = get_analyzer().extract_document(tmp_path)
        result = get_analyzer().analyze_document(document)
        return AnalyzeResponse(result=result)
    finally:
        os.unlink(tmp_path)
