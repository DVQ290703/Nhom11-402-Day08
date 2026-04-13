# Architecture — RAG Pipeline (Day 08 Lab)

> Template: Điền vào các mục này khi hoàn thành từng sprint.
> Deliverable của Documentation Owner.

## 1. Tổng quan kiến trúc

```
[Raw Docs]
    ↓
[index.py: Preprocess → Chunk → Embed → Store]
    ↓
[ChromaDB Vector Store]
    ↓
[rag_answer.py: Query → Retrieve → Rerank → Generate]
    ↓
[Grounded Answer + Citation]
```

**Mô tả ngắn gọn:**
> TODO: Mô tả hệ thống trong 2-3 câu. Nhóm xây gì? Cho ai dùng? Giải quyết vấn đề gì?

 Hệ thống là một trợ lý ảo RAG (Retrieval-Augmented Generation) được thiết kế để hỗ trợ bộ phận IT và HR tra cứu nhanh chóng các chính sách SLA, mã lỗi và quy trình vận hành nội bộ. Giải pháp sử dụng kiến trúc tìm kiếm Hybrid (kết hợp giữa vector similarity và BM25) cùng mô hình DeepSeek-V2 thực thi cục bộ để cung cấp câu trả lời chính xác, bảo mật và luôn có dẫn nguồn (citations) từ tài liệu gốc.

---

## 2. Indexing Pipeline (Sprint 1)

### Tài liệu được index
| File | Nguồn | Department | Số chunk |
|------|-------|-----------|---------|
| `policy_refund_v4.txt` | policy/refund-v4.pdf | CS | TODO |
| `sla_p1_2026.txt` | support/sla-p1-2026.pdf | IT | TODO |
| `access_control_sop.txt` | it/access-control-sop.md | IT Security | TODO |
| `it_helpdesk_faq.txt` | support/helpdesk-faq.md | IT | TODO |
| `hr_leave_policy.txt` | hr/leave-policy-2026.pdf | HR | TODO |

### Quyết định chunking
| Tham số | Giá trị | Lý do |
|---------|---------|-------|
| Chunk size | 256 tokens | Giúp giữ nguyên ngữ cảnh của các điều khoản ngắn và mã lỗi. |
| Overlap | 64 tokens | Giúp đảm bảo không bị mất thông tin khi cắt đoạn. |
| Chunking strategy | Heading-based / paragraph-based | TODO |
| Metadata fields | source, section, effective_date, department, access | Phục vụ filter, freshness, citation |

### Embedding model
- **Model**: paraphrase-multilingual-MiniLM-L12-v2
- **Vector store**: ChromaDB (PersistentClient)
- **Similarity metric**: Cosine

---

## 3. Retrieval Pipeline (Sprint 2 + 3)

### Baseline (Sprint 2)
| Tham số | Giá trị |
|---------|---------|
| Strategy | Dense (embedding similarity) |
| Top-k search | 10 |
| Top-k select | 3 |
| Rerank | Không |

### Variant (Sprint 3)
| Tham số | Giá trị | Thay đổi so với baseline |
|---------|---------|------------------------|
| Strategy | hybrid |  |
| Top-k search | 10 |  |
| Top-k select | 5 |  |
| Rerank | Không |  |
| Query transform | Không |  |

**Lý do chọn variant này:**
> TODO: Giải thích tại sao chọn biến này để tune.
> Ví dụ: "Chọn hybrid vì corpus có cả câu tự nhiên (policy) lẫn mã lỗi và tên chuyên ngành (SLA ticket P1, ERR-403)."

 lựa chọn kiến trúc Hybrid Retrieval kết hợp với việc tăng Top-k select lên 5 vì hai lý do chính:

Khắc phục điểm yếu mã lỗi: Phương pháp tìm kiếm ngữ nghĩa thuần túy (Dense) thường bỏ sót các từ khóa chính xác như mã lỗi ERR- hoặc các tên riêng kịch thuật. Việc thêm BM25 (Hybrid) đảm bảo hệ thống bắt được các từ khóa cứng này một cách chính xác qua cơ chế Keyword Matching.
Cải thiện độ đầy đủ (Completeness): Qua đánh giá Baseline, kết quả cho thấy nhiều câu trả lời bị thiếu thông tin do bằng chứng nằm ở các đoạn văn tiếp nối (đã bị chunk nhỏ). Việc tăng top_k_select từ 3 lên 5 giúp cung cấp cho LLM một dải ngữ cảnh đầy đủ hơn, từ đó tăng độ chính xác và tính toàn vẹn của câu trả lời mà không làm loãng Prompt.

---

## 4. Generation (Sprint 2)

### Grounded Prompt Template
```
Answer only from the retrieved context below.
If the context is insufficient, say you do not know.
Cite the source field when possible.
Keep your answer short, clear, and factual.

Question: {query}

Context:
[1] {source} | {section} | score={score}
{chunk_text}

[2] ...

Answer:
```

### LLM Configuration
| Tham số | Giá trị |
|---------|---------|
| Model | d eepseek-chat |
| Temperature | 0 (để output ổn định cho eval) |
| Max tokens | 512 |

---

## 5. Failure Mode Checklist

> Dùng khi debug — kiểm tra lần lượt: index → retrieval → generation

| Failure Mode | Triệu chứng | Cách kiểm tra |
|-------------|-------------|---------------|
| Index lỗi | Retrieve về docs cũ / sai version | `inspect_metadata_coverage()` trong index.py |
| Chunking tệ | Chunk cắt giữa điều khoản | `list_chunks()` và đọc text preview |
| Retrieval lỗi | Không tìm được expected source | `score_context_recall()` trong eval.py |
| Generation lỗi | Answer không grounded / bịa | `score_faithfulness()` trong eval.py |
| Token overload | Context quá dài → lost in the middle | Kiểm tra độ dài context_block |

---

## 6. Diagram (tùy chọn)

> TODO: Vẽ sơ đồ pipeline nếu có thời gian. Có thể dùng Mermaid hoặc drawio.

```mermaid

graph TD
    subgraph Indexing_Pipeline [1. LUỒNG INDEXING]
        A[Tài liệu gốc - data/docs/] --> B[Tiền xử lý văn bản]
        B --> C[Chia nhỏ đoạn - Chunking<br/>size=256, overlap=64]
        C --> D[Tạo Embedding<br/>paraphrase-multilingual]
        D --> E[(Lưu vào ChromaDB)]
    end
    subgraph RAG_Pipeline [2. LUỒNG TRUY VẤN - HYBRID]
        Q((Người dùng đặt câu hỏi)) --> Query[Nhận Query]
        
        Query --> Dense[<b>Dense Retrieval</b><br/>Vector Similarity]
        Query --> Sparse[<b>Sparse Retrieval</b><br/>Keyword - BM25]
        
        Dense --> RRF[<b>Reciprocal Rank Fusion</b><br/>Hợp nhất kết quả]
        Sparse --> RRF
        
        RRF --> Select[Chọn Top 5 Chunks<br/>Chất lượng nhất]
        
        Select --> Prompt[Xây dựng Grounded Prompt<br/>Kèm Citation ID]
        Prompt --> LLM[<b>DeepSeek-V2</b><br/>sinh câu trả lời]
        
        LLM --> Result((Trả về Answer + Sources))
    end
    E -.-> Dense
    E -.-> Sparse
    style E fill:#f9f,stroke:#333,stroke-width:2px
    style LLM fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style RRF fill:#fff4dd,stroke:#d4a017,stroke-width:2px