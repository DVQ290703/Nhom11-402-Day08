
# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Lê Hoàng Long  
**Vai trò trong nhóm:**  Retrieval Owner 
**Ngày nộp:** 13-4-20265  
**Độ dài yêu cầu:** 500–800 từ

---

## 1. Tôi đã làm gì trong lab này? (100-150 từ)

> Mô tả cụ thể phần bạn đóng góp vào pipeline:
> - Sprint nào bạn chủ yếu làm?
sprint 3

> - Cụ thể bạn implement hoặc quyết định điều gì?
Tôi bổ sung cài đặt hybrid và góp ý kiến cho nội dung cài đặt transform_query

> - Công việc của bạn kết nối với phần của người khác như thế nào?
tôi bổ sung nội dung điều chỉnh mã nguồn 
vibe coding rất là thuận tiện, song cần nhân lực để kiểm soát lại những gì máy tính sinh ra



_________________

---

## 2. Điều tôi hiểu rõ hơn sau lab này (100-150 từ)

> Chọn 1-2 concept từ bài học mà bạn thực sự hiểu rõ hơn sau khi làm lab.
> Ví dụ: chunking, hybrid retrieval, grounded prompt, evaluation loop.
> Giải thích bằng ngôn ngữ của bạn — không copy từ slide.

Tôi thấy sự cần thiết phải nắm được lý thuyết để có thể ước tính được chunking cỡ nào là phù hợp,
khi nào nên lựa chọn phương pháp tiếp cận nào để tăng tốc tính toán, giảm thiểu thời gian chờ đọi


---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn (100-150 từ)

> Điều gì xảy ra không đúng kỳ vọng?
việc lựa chọn ngưỡng để xác định xem thông điệp nào nên trả lời, thông điệp nào nên từ chối gây nhiều khó khăn 

> Lỗi nào mất nhiều thời gian debug nhất?
thời gian mất rất nhiều cho việc lựa chọn ngưỡng

> Giả thuyết ban đầu của bạn là gì và thực tế ra sao?
giả thuyết là ngưỡng 0.4 phù hợp, song sau nhiều thử nghiệm thì ngưỡng 0.2 phù hợp hơn
tuy nhiên thiết nghĩ việc đặt ngưỡng cứng không phải là giải pháp tốt 


_________________

---

## 4. Phân tích một câu hỏi trong scorecard (150-200 từ)

> Chọn 1 câu hỏi trong test_questions.json mà nhóm bạn thấy thú vị.
> Phân tích:
> - Baseline trả lời đúng hay sai? Điểm như thế nào?
> - Lỗi nằm ở đâu: indexing / retrieval / generation?
> - Variant có cải thiện không? Tại sao có/không?

**Câu hỏi:** tôi thành thật là chưa cảm thấy chúng có điều gì thú vị

**Phân tích:**



---

## 5. Nếu có thêm thời gian, tôi sẽ làm gì? (50-100 từ)

> 1-2 cải tiến cụ thể bạn muốn thử.
Tại thời điểm này tôi chưa thể nghĩ ra được đièu gì có thể cải thiện 
song trong thời gian tới thì có thể, 
Tôi đã thiết lập mã nguồn cho phép sử dung local LLM thay vì gọi OpenAI API
để làm được việc đó tôi đã tiến hành điều chỉnh, "tweaking", nhiều đoạn mã có sẵn trong dự án 
việc này tôi cho là sẽ rất cần thiết khi đi làm cho doanh nghiệp, điều đó đã được các diễn giả
 chia sẽ khá nhiều lần trong các worshop và office hour. 

_________________

---

*Lưu file này với tên: `reports/individual/[ten_ban].md`*
*Ví dụ: `reports/individual/nguyen_van_a.md`*
