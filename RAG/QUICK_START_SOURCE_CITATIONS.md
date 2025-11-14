# Quick Start: Source Citations in RAG

## ⚡ 3-Step Setup

### Step 1: Rebuild Vector Database
```python
# Run Cell 7 in your notebook
process_documents()
```
This adds metadata to all document chunks.

### Step 2: Test It
```python
# Run Cell 18 to verify
# You'll see source information displayed
```

### Step 3: Use It
```python
# Run Cell 17 to launch Gradio
demo.launch()
```

---

## 📋 What You'll See

### Before (No Citations)
```
SirusAI helpt organisaties met AI-implementatie 
van strategie tot uitvoering.
```

### After (With Citations) ✨
```
SirusAI helpt organisaties met AI-implementatie 
van strategie tot uitvoering (Source 1, Source 2).

---
📚 Sources Used:
**Source 1**: SirusAI - Positionering (Page 2)
**Source 2**: SirusAI - Business Plan (Page 1)
```

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 📄 **Document Name** | Shows which file the info came from |
| 📖 **Page Numbers** | Precise page references for PDFs |
| 🔢 **Inline Citations** | (Source 1) format within answers |
| 📚 **Source List** | Complete references at end of response |
| 🔍 **Debug Info** | Enable DEBUG_MODE=True to see retrieval details |

---

## 🔧 Quick Configuration

### Turn Off Source List Footer
```python
# In Cell 13 (chatbot_ui_stream), comment out:
# sources_list = format_sources_list(vdb_results)
```

### Change Number of Sources Retrieved
```python
# In Cell 1
TOP_K = 5  # Change this number (default: 5)
```

### Enable/Disable Debug Output
```python
# In Cell 1
DEBUG_MODE = True   # See detailed source info
DEBUG_MODE = False  # Clean output only
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| No sources shown | Rebuild vector DB with `process_documents()` |
| Wrong sources cited | Increase TOP_K or refine your query |
| No page numbers | Check if PDF has extractable text |
| Duplicate sources | Already handled - check metadata consistency |

---

## 💡 Pro Tips

1. **Ask Specific Questions**: More specific queries = better source matching
2. **Check Debug Output**: Set DEBUG_MODE=True to see what's retrieved
3. **Verify First Few Queries**: Make sure citations are accurate
4. **Adjust Chunk Size**: Edit CHUNK_SIZE in Cell 1 for precision tuning

---

## 📊 Modified Functions

| Function | What Changed |
|----------|--------------|
| `load_files()` | Now captures source metadata |
| `process_documents()` | Preserves metadata in chunks |
| `retrieve_context()` | Shows source info in debug |
| `construct_and_query_stream()` | Formats context with source labels |
| `format_sources_list()` | **NEW** - Creates source reference list |
| `chatbot_ui_stream()` | Appends source list to response |

---

## ✅ Verification Checklist

- [ ] Ran `process_documents()` after code changes
- [ ] Ran test cell (18) successfully
- [ ] See source labels in debug output
- [ ] Chatbot shows citations in responses
- [ ] Source list appears at end of responses
- [ ] Page numbers visible for PDFs (if applicable)

---

**You're ready to go!** 🚀

Questions? See full guide: `SOURCE_GROUNDING_GUIDE.md`

