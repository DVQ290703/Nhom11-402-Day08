# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Lê Thị Phương  
**Vai trò trong nhóm:** Indexing Engineer 
**Ngày nộp:** 2026-04-13  

---

## 1. Tôi đã làm gì trong lab này? (100–150 từ)

Trong lab này, tôi phụ trách chính phần **indexing pipeline (Sprint 1)** — nền tảng dữ liệu cho toàn bộ hệ thống RAG. Tôi xây dựng pipeline hoàn chỉnh gồm: đọc tài liệu `.txt`, preprocess để extract metadata (source, department, effective_date, access), làm sạch nội dung và chuẩn hóa text. Sau đó, tôi thiết kế chiến lược **structural chunking**: ưu tiên tách theo section heading (`=== Section ===`, `=== Điều ===`, …), rồi tiếp tục chia nhỏ theo paragraph hoặc các block có cấu trúc như Q&A, step, level.

Tiếp theo, tôi triển khai embedding bằng OpenAI `text-embedding-3-small` và lưu trữ toàn bộ chunks vào ChromaDB với cosine distance. Ngoài ra, tôi bổ sung các hàm inspect như `list_chunks()` và `inspect_metadata_coverage()` để debug và kiểm tra chất lượng index.

---

## 2. Điều tôi hiểu rõ hơn sau lab này (100–150 từ)

Sau lab, tôi nhận ra rằng **chunking strategy quan trọng hơn nhiều so với embedding model**. Nếu chunk bị cắt sai ranh giới (ví dụ giữa một điều khoản hoặc giữa Q&A), thì embedding tốt đến đâu cũng không thể cứu được context. Việc split theo structure (section → block → chunk size) giúp giữ nguyên ngữ nghĩa tốt hơn rất nhiều so với split theo fixed length.

Ngoài ra, tôi hiểu rõ hơn vai trò của metadata trong retrieval. Việc extract các field như `department`, `effective_date` không chỉ phục vụ filtering mà còn giúp debug và phân tích dữ liệu sau này. Cuối cùng, tôi học được rằng embedding pipeline cần có bước inspect rõ ràng — nếu không nhìn trực tiếp vào chunks, rất khó phát hiện lỗi logic.

---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn (100–150 từ)

Khó khăn lớn nhất là thiết kế logic **preprocess metadata**. Tài liệu không có format hoàn toàn đồng nhất, nên việc parse các dòng `Key: Value` dễ bị nhầm với nội dung thật. Tôi phải xử lý nhiều edge case như: dòng in hoa, dòng trống, hoặc header không rõ ràng.

Một điểm khác là **chunking theo structure** phức tạp hơn tôi nghĩ. Việc nhận diện các pattern như “Q:”, “Bước 1”, “Level 2” đòi hỏi regex cẩn thận, nếu không sẽ làm vỡ cấu trúc logic của tài liệu.

Ngoài ra, việc chọn kích thước chunk (1600 chars ~ 400 tokens) và overlap cũng cần thử nghiệm. Nếu chunk quá dài sẽ gây nhiễu, nhưng nếu quá ngắn thì mất context.

---

## 4. Phân tích một quyết định kỹ thuật trong indexing (150–200 từ)

**Quyết định:** Sử dụng **structural chunking thay vì fixed-size chunking**

Ban đầu, cách đơn giản nhất là chia văn bản thành các đoạn cố định theo độ dài (ví dụ 400 tokens). Tuy nhiên, cách này có nhược điểm lớn là phá vỡ cấu trúc tự nhiên của tài liệu. Ví dụ, một điều khoản hoặc một cặp Q&A có thể bị chia đôi, khiến embedding không còn mang đủ ý nghĩa.

Trong pipeline của tôi, tôi áp dụng chiến lược 3 bước:
- **Bước 1:** Split theo section heading (`=== Section ===`, `=== Điều ===`)
- **Bước 2:** Trong mỗi section, chia thành các **atomic blocks** (paragraph, Q&A, step, level, …)
- **Bước 3:** Ghép các block lại thành chunk theo giới hạn kích thước

Cách này đảm bảo mỗi chunk là một đơn vị ngữ nghĩa hoàn chỉnh. Khi retrieval, hệ thống dễ lấy được đúng context hơn, đặc biệt với các câu hỏi cần thông tin đầy đủ như quy trình hoặc chính sách.

Kết quả là số lượng chunk hợp lý, nội dung rõ ràng, và dễ debug hơn thông qua metadata và inspect tools.

---

## 5. Kết luận

Phần indexing đóng vai trò nền tảng cho toàn bộ hệ thống RAG. Một pipeline indexing tốt giúp cải thiện đáng kể chất lượng retrieval và giảm lỗi downstream. Bài học quan trọng nhất là: **giữ nguyên cấu trúc ngữ nghĩa của dữ liệu quan trọng hơn tối ưu thuật toán embedding**. Nếu dữ liệu đầu vào đã tốt, các bước phía sau sẽ hoạt động hiệu quả hơn rất nhiều.