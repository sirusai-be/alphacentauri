# Source Grounding Implementation Guide

## ✨ Overview
Your RAG system has been enhanced with **automatic source grounding and citation**. Now every response will show exactly which documents (and pages) were used to generate the answer.

---

## 🎯 What Changed

### 1. **Metadata Preservation Throughout Pipeline**
- **Before**: Documents were loaded as plain text without tracking source information
- **After**: Each document chunk includes metadata:
  - `source`: Filename (e.g., "SirusAI - Business Plan.pdf")
  - `type`: File type (pdf or text)
  - `chunk_id`: Position within the document
  - `total_chunks`: Total number of chunks from that document
  - Page numbers (for PDFs)

### 2. **Enhanced Document Loading** (`load_files()`)
- PDFs now extract page-by-page with `[Page X]` markers embedded in text
- Each document returns a dictionary with `content` and `metadata`
- Metadata travels with the content through the entire pipeline

### 3. **Metadata-Aware Chunking** (`process_documents()`)
- When splitting documents into chunks, metadata is preserved
- Each chunk inherits the source document's metadata
- Chunk position tracking helps trace back to original location

### 4. **Smart Context Formatting** (`construct_and_query_stream()`)
- Context is formatted with clear source labels: `[Source 1: Document Name, Page X]`
- Claude receives explicit instructions to cite sources in responses
- Citation format: `(Source 1)`, `(Source 2, Source 3)`, etc.

### 5. **Automatic Source List** (`format_sources_list()`)
- After each response, a formatted "Sources Used" section is appended
- Shows document names and page numbers (for PDFs)
- Eliminates duplicate entries

### 6. **Enhanced Debugging** (`retrieve_context()`)
- Debug mode now shows which sources were retrieved
- Displays chunk IDs and page markers for verification

---

## 🚀 How to Use

### Step 1: Reprocess Your Documents
**IMPORTANT**: You need to reload your documents to add metadata to the vector database.

Run these cells in order:
1. Cell 7: `process_documents()` - This will reload all documents with metadata

```python
process_documents()  # This updates ChromaDB with metadata
```

### Step 2: Test the Feature
Run Cell 18 (the new test cell) to verify source grounding is working:

```python
# This will show:
# - Which sources were retrieved
# - How they're formatted
# - Sample of the context with source labels
```

### Step 3: Use the Chatbot
Launch the Gradio interface (Cell 17) and ask a question. You'll see:

**Example Query**: "Wat is het waardevoorstel van SirusAI?"

**Example Response**:
```
SirusAI is een onafhankelijke AI- en automatisatiepartner die organisaties 
helpt om AI doelgericht, veilig en rendabel te implementeren (Source 1). 
Ze begeleiden bedrijven van strategie tot uitvoering, zodat AI een tastbare 
hefboom wordt voor groei, efficiëntie en innovatie (Source 2, Source 3).

---
📚 Sources Used:
**Source 1**: SirusAI - Positionering (Page 2)
**Source 2**: SirusAI - Business Plan (Page 1)
**Source 3**: SirusAI - WaardeVoorstel (Page 1)
```

---

## 🔧 Configuration Options

### Customize Citation Format
Edit the prompt in `construct_and_query_stream()` to change how Claude cites sources:

```python
# Current format: (Source 1)
# You can change to: [1], [Ref 1], etc.
```

### Toggle Source List Display
To disable the "Sources Used" section at the end:

```python
# In chatbot_ui_stream(), comment out:
# sources_list = format_sources_list(vdb_results)
# if sources_list:
#     full_response += sources_list
#     yield full_response
```

### Adjust Verbosity
Control debug output by setting:

```python
DEBUG_MODE = False  # Turn off detailed logging
```

---

## 📊 Benefits

### 1. **Transparency & Trust**
- Users can verify where information comes from
- Builds confidence in AI responses
- Enables fact-checking against source documents

### 2. **Compliance & Auditability**
- Essential for regulated industries (legal, medical, financial)
- Meets requirements for explainable AI
- Creates audit trail for decision-making

### 3. **Better User Experience**
- Users can explore source documents for more details
- Reduces "hallucination" concerns
- Empowers users with direct document references

### 4. **Debugging & Improvement**
- Quickly identify if wrong documents are being retrieved
- Helps optimize chunk size and retrieval settings
- Makes RAG system behavior more transparent

---

## 🎨 Advanced Customizations

### Add Section/Heading Extraction
For more precise citations, you can extract section headings from PDFs:

```python
# In load_files(), after extracting page content:
# Look for headings (all caps, specific formatting)
# Add to metadata: "section": "Business Model Overview"
```

### Link to Original Documents
Add hyperlinks to source documents:

```python
# In format_sources_list():
source_path = os.path.join(FILES_DIR, source_name)
sources_info.append(f"**Source {i}**: [{full_source}]({source_path})")
```

### Score-Based Citation Confidence
Show retrieval similarity scores:

```python
# Use similarity_search_with_score instead:
results = vectorstore.similarity_search_with_score(query, k=TOP_K)
# Then display confidence: "Source 1 (Confidence: 92%)"
```

---

## ⚠️ Important Notes

1. **Vector Database Must Be Rebuilt**
   - Old ChromaDB data doesn't have metadata
   - Run `process_documents()` to rebuild with metadata
   - This is a one-time operation

2. **Page Numbers for PDFs Only**
   - Text files show filename only (no page concept)
   - PDF page extraction depends on PyPDF2 quality
   - Some PDFs may not extract clean page markers

3. **Performance Impact**
   - Minimal - metadata is lightweight
   - Slightly larger prompt to Claude (includes source labels)
   - Still well within token limits

4. **Multilingual Support**
   - Source labels are in English
   - Claude will cite in the language of the response
   - Works with Dutch, French, English queries

---

## 🐛 Troubleshooting

### Problem: No sources shown in response
**Solution**: 
- Verify you ran `process_documents()` after code changes
- Check DEBUG_MODE=True to see retrieval output
- Ensure ChromaDB has data: check `CHROMA_DB_DIR`

### Problem: Page numbers missing
**Solution**:
- Verify PDF has extractable text (not scanned images)
- Check if `[Page X]` markers appear in debug output
- Some PDFs may need OCR preprocessing

### Problem: Wrong sources cited
**Solution**:
- Adjust `TOP_K` value (increase for more sources)
- Improve query specificity
- Check `CHUNK_SIZE` - smaller chunks = more precise citations

### Problem: Duplicate sources in list
**Solution**:
- `format_sources_list()` already deduplicates
- If still seeing duplicates, check metadata consistency

---

## 📚 Technical Details

### Data Flow
```
PDF/TXT Files
    ↓ (load_files)
Documents with Metadata
    ↓ (process_documents)
Chunks with Metadata in ChromaDB
    ↓ (retrieve_context)
Retrieved Chunks + Metadata
    ↓ (construct_and_query_stream)
Formatted Context with Source Labels
    ↓ (Claude API)
Response with Citations
    ↓ (format_sources_list)
Response + Source List
```

### Metadata Schema
```python
{
    "source": "SirusAI - Business Plan.pdf",
    "type": "pdf",
    "total_pages": 15,
    "chunk_id": 3,
    "total_chunks": 42
}
```

---

## 🎓 Best Practices

1. **Test with Known Queries**
   - Ask questions where you know the source document
   - Verify citations are accurate

2. **Monitor Retrieval Quality**
   - Keep DEBUG_MODE=True during development
   - Check if right documents are being retrieved

3. **Optimize Chunk Size**
   - Smaller chunks = more precise citations
   - Larger chunks = more context, fewer citations
   - Current setting: 500 chars (good balance)

4. **User Education**
   - Inform users about the citation format
   - Explain that (Source 1) refers to the list at the bottom

---

## 🎉 Summary

Your RAG system now provides full transparency about where answers come from:
- ✅ Every piece of information is traceable
- ✅ Users can verify responses against source documents
- ✅ Page-level precision for PDFs
- ✅ Automatic formatting and deduplication
- ✅ Ready for production use

**Next Steps**:
1. Run `process_documents()` to rebuild vector DB
2. Test with Cell 18
3. Launch Gradio and try some queries!

---

*Generated by SirusAI RAG Enhancement - November 2025*

