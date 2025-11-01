"use client";
import React, { useState } from "react";
import axios from "axios";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [document, setDocument] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<string>("");

  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8001";


  async function handleAnalyze() {
    if (!file) return;
    setLoading(true);
    setDocument("");
    setAnalysis("");
    
    try {
      const form = new FormData();
      form.append("file", file);
      
      // First extract the document
      const extractResponse = await axios.post(`${API_BASE}/api/extract`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setDocument(extractResponse.data.document || "");
      
      // Then analyze the document
      const analyzeResponse = await axios.post(`${API_BASE}/api/analyze`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setAnalysis(analyzeResponse.data.result || "");
    } catch (e: any) {
      alert(e?.response?.data?.detail || "Analysis failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-[var(--bg-primary)]">
      {/* Header */}
      <header className="border-b border-[var(--border-primary)] bg-[var(--bg-secondary)]/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                <span className="text-white font-bold text-lg">⚖️</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold gradient-text">LegalLens</h1>
                <p className="text-sm text-[var(--text-secondary)]">AI Contract Risk Analyzer</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="hidden md:flex items-center space-x-2 text-sm text-[var(--text-secondary)]">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span>API Connected</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Upload and Document Preview */}
          <div className="space-y-8">
            {/* Upload Section - Top Left */}
            <div className="glass-effect rounded-2xl p-8 animate-fade-in h-[50vh] max-h-[400px] min-h-[400px]">
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-[var(--text-primary)]">Upload Contract</h2>
                  <p className="text-[var(--text-secondary)]">Upload your legal document for AI analysis</p>
                </div>
              </div>

              <div className="space-y-6">
                {/* File Upload Area */}
                <div className="relative">
                  <input
                    type="file"
                    accept=".pdf,.txt"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    id="file-upload"
                  />
                  <label
                    htmlFor="file-upload"
                    className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-[var(--border-secondary)] rounded-xl cursor-pointer hover:border-[var(--accent-primary)] transition-colors duration-200 bg-[var(--bg-tertiary)]/50"
                  >
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                      <svg className="w-10 h-10 mb-3 text-[var(--text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      <p className="mb-2 text-sm text-[var(--text-secondary)]">
                        <span className="font-semibold">Click to upload</span> or drag and drop
                      </p>
                      <p className="text-xs text-[var(--text-muted)]">PDF or TXT files only</p>
                    </div>
                  </label>
                </div>

                {/* File Info */}
                {file && (
                  <div className="animate-slide-up p-4 bg-[var(--bg-tertiary)] rounded-xl border border-[var(--border-primary)]">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 rounded-lg bg-[var(--accent-primary)] flex items-center justify-center">
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-[var(--text-primary)] truncate">{file.name}</p>
                        <p className="text-xs text-[var(--text-secondary)]">
                          {(file.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Analyze Button */}
                <button
                  onClick={handleAnalyze}
                  disabled={!file || loading}
                  className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-semibold rounded-xl transition-all duration-200 transform hover:scale-[1.02] disabled:scale-100 disabled:cursor-not-allowed shadow-lg hover:shadow-xl text-sm"
                >
                  {loading ? (
                    <div className="flex items-center justify-center space-x-2">
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Analyzing...</span>
                    </div>
                  ) : (
                    <div className="flex items-center justify-center space-x-2">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                      <span>Analyze Contract</span>
                    </div>
                  )}
                </button>
              </div>

            </div>

            {/* Document Preview Section - Bottom Left */}
            {document && (
              <div className="glass-effect rounded-2xl p-8 animate-fade-in h-[50vh] max-h-[400px] min-h-[300px]">
                <div className="flex items-center justify-between mb-4 flex-shrink-0">
                  <h3 className="text-lg font-semibold text-[var(--text-primary)]">Extracted Document</h3>
                  <div className="flex items-center space-x-2 text-sm text-green-400">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>Extracted</span>
                  </div>
                </div>
                <div className="bg-[var(--bg-tertiary)] rounded-xl p-6 border border-[var(--border-primary)] h-[calc(100%-4rem)] flex flex-col">
                  <div className="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200">
                    <p className="text-sm text-[var(--text-primary)] whitespace-pre-wrap leading-relaxed">
                      {document.length > 1000 ? `${document.substring(0, 1000)}...` : document}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Analysis Results */}
          <div className="flex flex-col">
            <div className="glass-effect rounded-2xl p-4 animate-fade-in h-[70vh] max-h-[800px] min-h-[800px]">

              {!document && !analysis ? (
                
                <div className="flex flex-col items-center justify-center py-12 text-center">
                  <div className="w-16 h-16 rounded-full bg-[var(--bg-tertiary)] flex items-center justify-center mb-4">
                    <svg className="w-8 h-8 text-[var(--text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold text-[var(--text-primary)] mb-2">No Analysis Yet</h3>
                  <p className="text-[var(--text-secondary)]">Upload a contract and click "Analyze Contract" to extract and analyze</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Analysis Results */}
                  {analysis && (
                    <div className="bg-[var(--bg-tertiary)] rounded-xl p-6 border border-[var(--border-primary)] h-[70vh] max-h-[800px] min-h-[500px] flex flex-col">
                      <div className="prose prose-invert max-w-none flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200">
                        <div className="whitespace-pre-wrap text-[var(--text-primary)] leading-relaxed">
                          {analysis}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Loading State */}
                  {loading && (
                    <div className="flex flex-col items-center justify-center py-12 text-center">
                      <div className="w-16 h-16 rounded-full bg-[var(--accent-primary)]/20 flex items-center justify-center mb-6">
                        <div className="w-8 h-8 border-2 border-[var(--accent-primary)] border-t-transparent rounded-full animate-spin"></div>
                      </div>
                      <h4 className="text-xl font-semibold text-[var(--text-primary)] mb-2">Processing Document</h4>
                      <p className="text-[var(--text-secondary)]">Extracting text and analyzing your contract...</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}