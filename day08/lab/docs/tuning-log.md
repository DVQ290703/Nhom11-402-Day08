# Tuning Log — RAG Pipeline (Day 08 Lab)

> Template: Ghi lại mỗi thay đổi và kết quả quan sát được.
> A/B Rule: Chỉ đổi MỘT biến mỗi lần.

---

## Baseline (Sprint 2)

**Ngày:** 13/4/2026  
**Config:**
```
retrieval_mode = "dense"
chunk_size = 400 tokens
overlap = 80 tokens
top_k_search = 10
top_k_select = 3
use_rerank = False
llm_model = deepseek-v2
```

**Scorecard Baseline:**
| Metric | Average Score |
|--------|--------------|
| Faithfulness | 4.10/5 |
| Relevance | 4.20/5 |
| Context Recall | 5.00/5 |
| Completeness | 3.50/5 |

**Câu hỏi yếu nhất (điểm thấp):**
> TODO: Liệt kê 2-3 câu hỏi có điểm thấp nhất và lý do tại sao.
> Ví dụ: "q07 (Approval Matrix) - context recall = 1/5 vì dense bỏ lỡ alias."
q10 Nếu cần hoàn tiền khẩn cấp cho khách hàng VIP, quy trình có khác không?  -  Complete: 3 vì thông tin bị chunked giữa chừng
[q09] ERR-403-AUTH là lỗi gì và cách xử lý? - Recall: None vì thông tin có độ tương tự cosin thấp hơn ngưỡng cho phép 
[q05] Tài khoản bị khóa sau bao nhiêu lần đăng nhập sai? - Faithfulness: 1 vì thông tin không có trong retrieved chunks
[q07] Ai có thẩm quyền phê duyệt yêu cầu truy cập hệ thống? - Faithfulness: 1 vì thông tin không có trong retrieved chunks 

**Giả thuyết nguyên nhân (Error Tree):**
- [x] Indexing: Chunking cắt giữa điều khoản
- [x] Indexing: Metadata thiếu effective_date
- [x] Retrieval: Dense bỏ lỡ exact keyword / alias
- [ ] Retrieval: Top-k quá ít → thiếu evidence
- [ ] Generation: Prompt không đủ grounding
- [x] Generation: Context quá dài → lost in the middle

---

## Variant 1 (Sprint 3)

**Ngày:** 13/4/2026  
**Biến thay đổi:** retrieval_mode = "hybrid"  
**Lý do chọn biến này:**
> TODO: Giải thích theo evidence từ baseline results.
> Ví dụ: "Chọn hybrid vì q07 (alias query) và q09 (mã lỗi ERR-403) đều thất bại với dense.
> Corpus có cả ngôn ngữ tự nhiên (policy) lẫn tên riêng/mã lỗi (ticket code, SLA label)."
> 

**Config thay đổi:**
```
retrieval_mode = "hybrid"   # hoặc biến khác
# Các tham số còn lại giữ nguyên như baseline
```

**Scorecard Variant 1:**
| Metric | Baseline | Variant 1 | Delta |
|--------|----------|-----------|-------|
| Faithfulness | 4.10/5 | 4.30/5 | +0.2 |
| Answer Relevance | 4.20/5 | 4.30/5 | +0.1 |
| Context Recall | 5.00/5 | 5.00/5 | 0 |
| Completeness | 3.50/5 | 3.70/5 | +0.2 |

**Nhận xét:**
> TODO: Variant 1 cải thiện ở câu nào? Tại sao?
> Hybrid retrieval giúp tăng Faithfulness và Completeness lên 0.2 điểm.
> Có câu nào kém hơn không? Tại sao?
> Không có câu nào kém hơn baseline.

**Kết luận:**
> TODO: Variant 1 có tốt hơn baseline không?
> Hybrid retrieval có tốt hơn baseline.
> Bằng chứng là gì? (điểm số, câu hỏi cụ thể)
> [q09] ERR-403-AUTH, phương pháp Hybrid thành công nhờ thành phần Sparse (BM25) bắt được chính xác từ khóa mã lỗi, điều mà Dense Retriever đã bỏ lỡ do độ tương tự vector thấp.
---

## Variant 2 (nếu có thời gian)

**Biến thay đổi:** top_k_select = 5  
**Config:**
```
retrieval_mode = "hybrid"
top_k_select = 5
```

**Scorecard Variant 2:**
| Metric | Baseline | Variant 1 | Variant 2 | Best |
|--------|----------|-----------|-----------|------|
| Faithfulness | 4.10/5 | 4.30/ 5 | 4.40/5 | ? |
| Answer Relevance | 4.20/5 | 4.30/5 | 4.40/5 | ? |
| Context Recall | 5.00/5 | 5.00/5 | 5.00/5 | ? |
| Completeness | 3.50/5 | 3.70/5 | 3.80/5 | ? |

---

## Tóm tắt học được

> TODO (Sprint 4): Điền sau khi hoàn thành evaluation.

1. **Lỗi phổ biến nhất trong pipeline này là gì?**
   > Lỗi phổ biến nhất là Retrieval False Negatives (Miss): Mô hình Dense Retriever thuần túy thường bỏ lỡ các mã lỗi chính xác (như ERR-403) hoặc các thuật ngữ chuyên môn viết tắt khi chúng có khoảng cách cosine lớn. Ngoài ra, lỗi cắt đoạn (Chunking failure) khiến các điều khoản dài bị chia cắt, dẫn đến việc LLM thiếu thông tin để trả lời đầy đủ (Completeness thấp).

2. **Biến nào có tác động lớn nhất tới chất lượng?**
   > Biến có tác động lớn nhất tới chất lượng là retrieval_mode. Việc chuyển từ chế độ Dense sang Hybrid đã cải thiện đáng kể điểm số Faithfulness và Completeness, chứng tỏ sự kết hợp giữa tìm kiếm ngữ nghĩa (Dense) và tìm kiếm từ khóa (Sparse) là chìa khóa để xử lý các câu hỏi đa dạng trong tài liệu SLA.

3. **Nếu có thêm 1 giờ, nhóm sẽ thử gì tiếp theo?**
   >  Nếu có thêm 1 giờ, nhóm sẽ thử nghiệm với việc tăng tham số top_k_select lên 5 hoặc 7 để cung cấp nhiều ngữ cảnh hơn cho LLM, đồng thời tối ưu hóa trọng số (weights) trong thuật toán RRF để cân bằng tốt hơn giữa Dense và Sparse retrieval.
