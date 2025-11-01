import numpy as np
import pdfplumber
from rank_bm25 import BM25Okapi
from openai import OpenAI
import faiss

class Analyzer:
    def __init__(self, api_key: str, base_url: str, templates: list[dict[str,str]]):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.corpus = [t['text'] for t in templates]
        self.topics = [t['topic'] for t in templates]
        emb_dim = len(self._embed('warm start'))
        doc_embs = np.vstack([self._embed(t, 'passage') for t in self.corpus])
        self.doc_embs_n = doc_embs / np.linalg.norm(doc_embs, axis=1, keepdims=True)
        self.faiss = faiss.IndexFlatIP(emb_dim)
        self.faiss.add(self.doc_embs_n)
        tokenized = [c.lower().split() for c in self.corpus]
        self.bm25 = BM25Okapi(tokenized)

    def _embed(self, text: str, input_type: str = 'passage') -> np.ndarray:
        emb = self.client.embeddings.create(
            input=[text],
            model='nvidia/llama-3.2-nemoretriever-300m-embed-v2',
            encoding_format='float',
            extra_body={'input_type': input_type, 'truncate': 'NONE'}
        )
        return np.array(emb.data[0].embedding, dtype='float32')

    def call_llm(self, prompt: str, model: str, max_tokens: int) -> str:
        resp = self.client.chat.completions.create(
            model=model,
            messages=[{"role":"system","content":"You are a helpful assistant."}, {"role":"user","content":prompt}],
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content

    def extract_document(self, file_path: str) -> str:
        """Extract full document text from PDF or TXT file."""
        text = ''
        if file_path.endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    pt = page.extract_text()
                    if pt:
                        text += pt + "\n"
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        return text.strip()

    def hybrid_search(self, query_text: str, top_k=8, alpha=0.6):
        q = self._embed(query_text, 'query')
        qn = q / np.linalg.norm(q)
        sim, idx = self.faiss.search(qn.reshape(1,-1), min(top_k, len(self.corpus)))
        emb_scores = sim[0].tolist(); emb_idx = idx[0].tolist()
        bm_scores = self.bm25.get_scores(query_text.lower().split()).tolist()
        def norm(arr):
            a = np.array(arr, dtype=float)
            return (a - a.min()) / (a.max() - a.min() + 1e-9)
        emb_norm = norm([emb_scores[emb_idx.index(i)] if i in emb_idx else 0 for i in range(len(self.corpus))])
        bm_norm  = norm(bm_scores)
        hybrid = alpha*emb_norm + (1-alpha)*bm_norm
        top_indices = np.argsort(hybrid)[::-1][:top_k].tolist()
        selected, selected_vecs = [], []
        lamb = 0.75
        while top_indices and len(selected) < min(5, top_k):
            best_i, best_score = None, -1
            for i in top_indices:
                rel = hybrid[i]
                div = 0 if not selected_vecs else max(np.dot(self.doc_embs_n[i], v) for v in selected_vecs)
                mmr = lamb*rel - (1-lamb)*div
                if mmr > best_score:
                    best_score, best_i = mmr, i
            selected.append(best_i)
            selected_vecs.append(self.doc_embs_n[best_i])
            top_indices.remove(best_i)
        return [{"topic": self.topics[i], "text": self.corpus[i], "score": float(hybrid[i])} for i in selected]

    def retrieve_best_reference(self, clause: str):
        cands = self.hybrid_search(clause, top_k=8, alpha=0.6)
        candidates_blob = "\n".join([f"[{i}] Topic: {c['topic']}\nText: {c['text']}\n" for i, c in enumerate(cands)])
        prompt = (
            "Rank the following reference clauses by how well they match the user's clause intent and provide a brief reason. "
            "Return JSON with fields: ranked (array of indices best→worst), reasons (array of strings).\n\n"
            f"User Clause:\n{clause}\n\n"
            "Candidates:\n" + candidates_blob
        )
        judge = self.call_llm(prompt, model='nvidia/llama-3.3-nemotron-super-49b-v1.5', max_tokens=2000)
        import json, re as _re
        try:
            js = json.loads(_re.search(r'\{.*\}', judge, _re.S).group(0))
            order = js.get('ranked', [])
            best = cands[order[0]] if order else cands[0]
        except Exception:
            best = cands[0]
        return best, cands, judge

    def analyze_document(self, document: str) -> str:
        """Analyze the entire contract document for risks and provide safer alternatives."""
        best, _, _ = self.retrieve_best_reference(document)
        ref = best['text']; topic = best['topic']
        
        analysis_prompt = (
            "You are a legal risk analysis expert. "
            "Analyze the following contract document and identify all risks, vague terms, unfair wording, and potential issues. "
            "Compare it against standard safe contract practices and identify areas that need improvement.\n\n"
            f"Contract Document:\n{document}\n\n"
            f"Reference Safe Contract Template ({topic}):\n{ref}\n\n"
            "Return your analysis as a JSON object with the following structure:\n"
            "{\n"
            '  "overall_risk": "High/Medium/Low",\n'
            '  "risk_score": 85,\n'
            '  "issues": [\n'
            '    {\n'
            '      "type": "risky/unclear/safe",\n'
            '      "severity": "high/medium/low",\n'
            '      "description": "Description of the issue",\n'
            '      "clause": "Relevant contract clause",\n'
            '      "recommendation": "How to fix this issue"\n'
            '    }\n'
            '  ],\n'
            '  "key_concerns": [\n'
            '    "List of major areas of concern"\n'
            '  ],\n'
            '  "missing_clauses": [\n'
            '    "List of important clauses that are missing"\n'
            '  ],\n'
            '  "summary": {\n'
            '    "total_issues": 12,\n'
            '    "risky_count": 5,\n'
            '    "unclear_count": 4,\n'
            '    "safe_count": 3,\n'
            '    "document_length": 2500,\n'
            '    "main_topics": ["payment", "liability", "termination"]\n'
            '  }\n'
            "}\n\n"
            "Ensure the JSON is valid and complete."
        )
        
        analysis = self.call_llm(
            analysis_prompt,
            model='nvidia/llama-3.3-nemotron-super-49b-v1.5', max_tokens=4000
        )
        
        rewrite_prompt = (
            "Based on the risk analysis below, rewrite the contract to address the identified issues and make it more balanced for both parties. "
            "Maintain the original structure and intent while improving clarity, fairness, and legal soundness.\n\n"
            f"Original Contract:\n{document}\n\n"
            f"Risk Analysis:\n{analysis}\n\n"
            "Return your response as a JSON object with the following structure:\n"
            "{\n"
            '  "improved_contract": "The complete rewritten contract text",\n'
            '  "key_improvements": [\n'
            '    "List of major improvements made"\n'
            '  ],\n'
            '  "changes_summary": {\n'
            '    "clauses_modified": 8,\n'
            '    "clauses_added": 3,\n'
            '    "clauses_removed": 1,\n'
            '    "risk_reduction": "High/Medium/Low"\n'
            '  }\n'
            "}\n\n"
            "Ensure the JSON is valid and complete."
        )
        
        rewrite = self.call_llm(
            rewrite_prompt,
            model='nvidia/nvidia-nemotron-nano-9b-v2', max_tokens=4000
        )
        
        # Parse JSON responses
        import json
        import re
        
        try:
            # Extract JSON from analysis response
            analysis_json = json.loads(re.search(r'\{.*\}', analysis, re.DOTALL).group(0))
        except:
            analysis_json = {"error": "Failed to parse analysis JSON", "raw": analysis}
        
        try:
            # Extract JSON from rewrite response
            rewrite_json = json.loads(re.search(r'\{.*\}', rewrite, re.DOTALL).group(0))
        except:
            rewrite_json = {"error": "Failed to parse rewrite JSON", "raw": rewrite}
        
        # Format the response
        result = "📄 Contract Analysis\n" + "="*50 + "\n\n"
        
        # Document preview
        result += f"📋 Document Preview:\n{document[:300]}...\n\n"
        
        # Risk analysis
        if "error" not in analysis_json:
            result += f"⚠️ Risk Assessment: {analysis_json.get('overall_risk', 'Unknown')}\n"
            result += f"📊 Risk Score: {analysis_json.get('risk_score', 'N/A')}/100\n\n"
            
            # Issues summary
            issues = analysis_json.get('issues', [])
            result += f"🔍 Issues Found: {len(issues)} total\n"
            risky_count = len([i for i in issues if i.get('type') == 'risky'])
            unclear_count = len([i for i in issues if i.get('type') == 'unclear'])
            safe_count = len([i for i in issues if i.get('type') == 'safe'])
            result += f"   🔴 Risky: {risky_count}\n"
            result += f"   🟡 Unclear: {unclear_count}\n"
            result += f"   🟢 Safe: {safe_count}\n\n"
            
            # Key concerns
            concerns = analysis_json.get('key_concerns', [])
            if concerns:
                result += "🚨 Key Concerns:\n"
                for concern in concerns:
                    result += f"   • {concern}\n"
                result += "\n"
            
            # Missing clauses
            missing = analysis_json.get('missing_clauses', [])
            if missing:
                result += "❌ Missing Important Clauses:\n"
                for clause in missing:
                    result += f"   • {clause}\n"
                result += "\n"
            
            # Detailed issues
            if issues:
                result += "📋 Detailed Issues:\n"
                for i, issue in enumerate(issues, 1):
                    emoji = "🔴" if issue.get('type') == 'risky' else "🟡" if issue.get('type') == 'unclear' else "🟢"
                    result += f"{i}. {emoji} {issue.get('description', 'No description')}\n"
                    if issue.get('clause'):
                        result += f"   Clause: {issue.get('clause')}\n"
                    if issue.get('recommendation'):
                        result += f"   Fix: {issue.get('recommendation')}\n"
                    result += "\n"
        else:
            result += f"⚠️ Risk Analysis (Raw):\n{analysis_json.get('raw', 'No analysis available')}\n\n"
        
        # Improved contract
        if "error" not in rewrite_json:
            result += "✅ Improved Contract\n" + "="*50 + "\n\n"
            result += f"{rewrite_json.get('improved_contract', 'No improved contract available')}\n\n"
            
            # Key improvements
            improvements = rewrite_json.get('key_improvements', [])
            if improvements:
                result += "🔧 Key Improvements Made:\n"
                for improvement in improvements:
                    result += f"   • {improvement}\n"
                result += "\n"
            
            # Changes summary
            changes = rewrite_json.get('changes_summary', {})
            if changes:
                result += "📊 Changes Summary:\n"
                result += f"   • Clauses Modified: {changes.get('clauses_modified', 0)}\n"
                result += f"   • Clauses Added: {changes.get('clauses_added', 0)}\n"
                result += f"   • Clauses Removed: {changes.get('clauses_removed', 0)}\n"
                result += f"   • Risk Reduction: {changes.get('risk_reduction', 'Unknown')}\n\n"
        else:
            result += f"✅ Improved Contract (Raw):\n{rewrite_json.get('raw', 'No improved contract available')}\n\n"
        
        return result
