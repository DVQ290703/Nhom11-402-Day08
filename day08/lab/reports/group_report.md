# Báo Cáo Nhóm — Lab Day 08: Full RAG Pipeline

**Tên nhóm:** Nhóm 11 — Lớp 402  
**Thành viên:**
| Tên | Vai trò | Tên và MHV |
|-----|---------|-------|
| Đỗ Văn Quyết | Tech Lead | Đỗ Văn Quyết - 2A202600042 |
| Lê Thị Phương | Indexing Engineer | Lê Thị Phương - 2A202600107 |
| Hà Hữu An | Retrieval Owner | Hà Hữu An - 2A202600368 |
| Lê Hoàng Long | Retrieval Owner | Lê Hoàng Long - 2A202600095 |
| Hồ Thị Tố Nhi | Generation Owner | Hồ Thị Tố Nhi - 2A202600369 |
| Hoàng Văn Kiên | Eval Owner | Hoàng Văn Kiên - 2A202600077 |

**Ngày nộp:** 2026-04-13  
**Repo:** https://github.com/DVQ290703/Nhom11-402-Day08  
**Độ dài khuyến nghị:** 600–900 từ

---

> **Hướng dẫn nộp group report:**
>
> - File này nộp tại: `reports/group_report.md`
> - Deadline: Được phép commit **sau 18:00** (xem SCORING.md)
> - Tập trung vào **quyết định kỹ thuật cấp nhóm** — không trùng lặp với individual reports
> - Phải có **bằng chứng từ code, scorecard, hoặc tuning log** — không mô tả chung chung

---

## 1. Pipeline nhóm đã xây dựng (150–200 từ)

> Mô tả ngắn gọn pipeline của nhóm:
> - Chunking strategy: size, overlap, phương pháp tách (by paragraph, by section, v.v.)
> - Embedding model đã dùng
> - Retrieval mode: dense / hybrid / rerank (Sprint 3 variant)

**Chunking decision:**
> Nhóm dùng **structural chunking** — ưu tiên tách theo section heading (`=== Section ===`, `=== Điều ===`), rồi tiếp tục chia thành các atomic block (paragraph, Q&A, step, level), chunk_size ≈ 1600 chars (~400 tokens), overlap 80 tokens. Chiến lược này được chọn vì tài liệu nội bộ có cấu trúc điều khoản rõ ràng — cắt theo fixed-size sẽ phá vỡ ranh giới ngữ nghĩa giữa các điều khoản.

**Embedding model:**

OpenAI `text-embedding-3-small` — lưu vào ChromaDB với cosine distance. Lựa chọn này cân bằng giữa chất lượng embedding và chi phí API, phù hợp với corpus 5 tài liệu (~1000–1500 chunks).

**Retrieval variant (Sprint 3):**
> Nhóm chọn **Hybrid Retrieval (Dense + BM25 via Reciprocal Rank Fusion) + LLM-based Rerank**. Lý do: dense embedding bỏ lỡ exact keyword (tên policy, mã ticket), BM25 bù đắp bằng keyword matching. Rerank lọc noise trước khi đưa context vào generation.

---

## 2. Quyết định kỹ thuật quan trọng nhất (200–250 từ)

> Chọn **1 quyết định thiết kế** mà nhóm thảo luận và đánh đổi nhiều nhất trong lab.
> Phải có: (a) vấn đề gặp phải, (b) các phương án cân nhắc, (c) lý do chọn.

**Quyết định:** Chiến lược chunking — Structural chunking vs Fixed-size chunking

**Bối cảnh vấn đề:**

Khi bắt đầu Sprint 1, nhóm cần quyết định cách chia nhỏ 5 tài liệu nội bộ (~5000 lines tổng cộng). Các tài liệu này có cấu trúc phân cấp rõ ràng: section heading → paragraph → Q&A block → step. Câu hỏi đặt ra: nên dùng fixed-size chunking (đơn giản, implement nhanh) hay structural chunking (phức tạp hơn nhưng preserve ngữ nghĩa)?

**Các phương án đã cân nhắc:**

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|-----------|
| Fixed-size (400 tokens, overlap 50) | Implement nhanh, dễ tune | Phá vỡ ranh giới điều khoản, Q&A bị cắt đôi, embedding mất ngữ cảnh |
| Structural chunking (section → block → size limit) | Giữ nguyên đơn vị ngữ nghĩa, dễ debug qua metadata | Phức tạp hơn, cần regex nhận diện pattern, nhiều edge case |

**Phương án đã chọn và lý do:**

Nhóm chọn **structural chunking**. Lý do: tài liệu nội bộ có title heading nhất quán (`=== Section ===`), các block Q&A và step là đơn vị ngữ nghĩa hoàn chỉnh — nếu bị cắt giữa chừng, LLM mất hẳn context. Việc tách theo section trước, sau đó block, đảm bảo mỗi chunk là một đơn vị có thể trả lời độc lập.

**Bằng chứng từ scorecard/tuning-log:**

Context Recall đạt **5.00/5** ở cả baseline và variant — chứng tỏ retrieval lấy đúng source. Câu hỏi gq05 và gq07 fail không phải vì chunking sai mà vì `preprocess_document` lọc bỏ nội dung quan trọng nằm trước section header đầu tiên (ghi chú alias "Approval Matrix"). Đây là bug logic trong preprocess, không phải do chiến lược chunking.

---

## 3. Kết quả grading questions (100–150 từ)

> Sau khi chạy pipeline với grading_questions.json (public lúc 17:00):
> - Câu nào pipeline xử lý tốt nhất? Tại sao?
> - Câu nào pipeline fail? Root cause ở đâu (indexing / retrieval / generation)?
> - Câu gq07 (abstain) — pipeline xử lý thế nào?

**Ước tính điểm raw:** ~72 / 98

**Câu tốt nhất:** ID: **gq06** (Cross-Document, 12 điểm) — Pipeline retrieve đúng 2/2 expected sources (SLA P1 doc + Access Control SOP), LLM tổng hợp đúng quy trình 4 bước và mốc thời gian 24 giờ. Điểm: Faithful 5/5, Relevant 5/5, Recall 5/5, Complete 5/5.

**Câu fail:** ID: **gq05** (Access Control — Admin Access cho Contractor) — Root cause nằm ở **indexing**: hàm `preprocess_document` trong `index.py` lọc bỏ toàn bộ nội dung nằm phía trên section header đầu tiên trong file `access_control_sop.txt`, bao gồm cả đoạn quy định about contractor và third-party vendor. Dữ liệu không bao giờ vào Vector Store → retrieval không thể tìm thấy dù Context Recall báo 5/5.

**Câu gq07 (abstain):** Query "Công ty sẽ phạt bao nhiêu nếu team IT vi phạm cam kết SLA P1?" — Pipeline trả về abstain: *"Tôi xin lỗi, hiện tại tài liệu không có thông tin về vấn đề này."* Đây là **hành vi đúng** vì tài liệu SLA P1 không quy định mức phạt. Grounded prompt hoạt động chính xác — không hallucinate. Điểm thấp (1/1/-/2) phản ánh hạn chế của heuristic keyword scoring, không phải lỗi của pipeline.

---

## 4. A/B Comparison — Baseline vs Variant (150–200 từ)

> Dựa vào `docs/tuning-log.md`. Tóm tắt kết quả A/B thực tế của nhóm.

**Biến đã thay đổi (chỉ 1 biến):** `retrieval_mode`: `"dense"` → `"hybrid"` (dense + BM25/RRF). Tất cả tham số khác giữ nguyên (chunk_size, overlap, top_k, llm_model).

| Metric | Baseline (dense) | Variant (hybrid) | Delta |
|--------|---------|---------|-------|
| Faithfulness | 3.80/5 | 3.70/5 | **-0.10** |
| Answer Relevance | 4.00/5 | 4.00/5 | 0.00 |
| Context Recall | 5.00/5 | 5.00/5 | 0.00 |
| Completeness | 3.20/5 | 3.20/5 | 0.00 |

**Kết luận:**

Variant hybrid **không cải thiện** so với baseline dense trên bộ grading questions này. Delta duy nhất là Faithfulness giảm nhẹ (-0.10), có thể do BM25 kéo thêm một số chunk cận biên làm nhiễu context. Root cause của 2 câu fail lớn nhất (gq05, gq07) nằm ở **indexing** — retrieval mode không thể sửa được vấn đề dữ liệu chưa được index. Nhóm vẫn chọn hybrid + rerank làm config nộp cuối vì lợi thế exact keyword matching sẽ có ích trong production với corpus lớn và truy vấn chứa mã/alias.

---

## 5. Phân công và đánh giá nhóm (100–150 từ)

> Đánh giá trung thực về quá trình làm việc nhóm.

**Phân công thực tế:**

| Thành viên | Phần đã làm | Sprint |
|------------|-------------|--------|
| Lê Thị Phương | Indexing pipeline: preprocess metadata, structural chunking, embed + lưu ChromaDB, inspect tools (`list_chunks`, `inspect_metadata_coverage`) | Sprint 1 |
| Đỗ Văn Quyết | Kiến trúc tổng thể, baseline dense retrieval, `grounded_answer()`, tích hợp end-to-end, review code | Sprint 1, 2 |
| Hồ Thị Tố Nhi | `transform_query`, `build_context_block`, `build_grounded_prompt`, `call_llm`, `rag_answer()`, `compare_retrieval_strategies()` | Sprint 2, 3 |
| Hà Hữu An | `retrieve_dense`, `retrieve_sparse` (BM25), `retrieve_hybrid` (RRF), `rerank` (LLM-based) | Sprint 3 |
| Lê Hoàng Long | Hỗ trợ retrieval: tuning RRF parameters, kiểm thử và debug hybrid pipeline, đánh giá chất lượng kết quả retrieval | Sprint 3 |
| Hoàng Văn Kiên | `eval.py`: 4 hàm scoring, `run_scorecard()`, `compare_ab()`, phân tích A/B kết quả | Sprint 4 |

**Điều nhóm làm tốt:**

Phân công sprint rõ ràng, mỗi thành viên sở hữu một module độc lập. Context Recall đạt 5.00/5 liên tục chứng tỏ chunking và indexing chuẩn. Pipeline không hallucinate — abstain đúng thời điểm, grounded prompt hoạt động tốt.

**Điều nhóm làm chưa tốt:**

Bug trong `preprocess_document` không được phát hiện sớm — lọc bỏ content quan trọng trước section header đầu tiên, trực tiếp gây ra điểm thấp ở gq05. Heuristic keyword scoring trong `eval.py` không đủ chính xác để đánh giá abstain response, dẫn đến kết quả A/B kém tin cậy.

---

## 6. Nếu có thêm 1 ngày, nhóm sẽ làm gì? (50–100 từ)

> 1–2 cải tiến cụ thể với lý do có bằng chứng từ scorecard.

**Cải tiến 1 — Fix indexing preprocess:** Sửa `preprocess_document` trong `index.py` để giữ lại nội dung trước section header đầu tiên (Note, ghi chú alias, metadata mở rộng). Bằng chứng: gq05 scored 1/5 faithfulness do LLM không có evidence về contractor access — data tồn tại trong file gốc nhưng không bao giờ vào Vector Store. Fix này có thể cứu ít nhất 10 điểm.

**Cải tiến 2 — LLM-as-Judge cho scoring:** Thay thế heuristic keyword matching trong `score_faithfulness` và `score_completeness` bằng LLM-as-Judge. Bằng chứng: gq07 abstain đúng nhưng bị chấm 1/5 faithfulness — scoring hiện tại không phân biệt được "đúng không trả lời" và "sai vì không có context".

---

*File này lưu tại: `reports/group_report.md`*  
*Commit sau 18:00 được phép theo SCORING.md*
