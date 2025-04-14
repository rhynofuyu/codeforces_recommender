# Codeforces Problem Recommender

A command-line application that suggests personalized Codeforces practice problems based on a user's handle, rating, and the tags of problems they've already solved successfully.

## Features

- Fetches user's solved problems and rating from Codeforces API
- Analyzes which problem tags the user has practiced more/less
- Recommends problems based on:
  - User's current rating (suggests problems within an appropriate difficulty range)
  - Problem tags (prioritizes less-practiced tags)
  - Already solved problems (excludes these from recommendations)
- Provides explanations for why each problem is recommended
- Caches problem set data to minimize API requests

## Requirements

- Python 3.6+
- `requests` library

## Installation

1. Clone or download this repository
2. Install the required library:

```bash
pip install requests
```

## Usage

Run the script with a Codeforces handle (username) as an argument:

```bash
python codeforces_recommender.py [handle]
```

Optional arguments:
- `--num`: Number of problems to recommend (default: 5)

Example:

```bash
python codeforces_recommender.py tourist --num 3
```

## How It Works

1. **Data Collection**: Fetches your submission history and current rating from Codeforces
2. **Analysis**: Determines which problem tags you've solved more/less and your rating range
3. **Recommendation**: Finds unsolved problems that match your skill level while helping you improve in weaker areas
4. **Display**: Shows problem details with direct links and explains why each problem was recommended

## Project Structure

- `codeforces_recommender.py`: Main script with all functionality
- `cache/`: Directory for caching problem set data (created automatically)

## Notes

- The first run may take longer as it downloads the problem set data
- Subsequent runs will use cached data (refreshed daily)

<!-- Bản Tiếng Việt -->
# Ứng dụng gợi ý bài tập Codeforces

Đây là một ứng dụng nhỏ chạy trên dòng lệnh, giúp bạn tìm các bài tập luyện tập trên Codeforces phù hợp với trình độ và sở thích của mình. Ứng dụng sẽ dựa vào tài khoản Codeforces của bạn, số điểm hiện tại, và những dạng bài bạn đã giải được để đưa ra gợi ý.

## Chức năng chính

- Lấy dữ liệu về các bài bạn đã giải và số điểm hiện tại từ Codeforces.
- Phân tích xem bạn mạnh/yếu ở những dạng bài (tag) nào.
- Gợi ý các bài tập phù hợp:
  - Dựa trên số điểm của bạn (chọn bài có độ khó vừa sức).
  - Ưu tiên các dạng bài bạn ít luyện tập hơn (giúp bạn cải thiện đều).
  - Loại trừ các bài bạn đã giải rồi.
- Giải thích vì sao ứng dụng lại gợi ý bài tập đó cho bạn.
- Lưu dữ liệu bài tập để lần sau chạy nhanh hơn (không cần tải lại từ đầu).

## Để chạy ứng dụng này, bạn cần:

- Python 3.6 trở lên.
- Thư viện `requests`.

## Cài đặt

1. Tải ứng dụng này về máy.
2. Mở terminal/command prompt lên, gõ lệnh sau để cài thư viện:

```bash
pip install requests
```

## Sử dụng

Chạy ứng dụng bằng lệnh:

```bash
python codeforces_recommender.py [tài khoản Codeforces của bạn]
```

Ví dụ:

```bash
python codeforces_recommender.py tourist
```

Bạn có thể thêm tùy chọn `--num` để chỉ định số lượng bài tập muốn gợi ý (mặc định là 5):

```bash
python codeforces_recommender.py tourist --num 3
```

## Ứng dụng hoạt động thế nào?

1. **Thu thập dữ liệu:** Lấy thông tin về các bài bạn đã nộp và số điểm từ Codeforces.
2. **Phân tích:** Xem bạn hay giải được các bài dạng gì, và số điểm của bạn đang ở mức nào.
3. **Gợi ý:** Tìm các bài chưa giải, vừa sức với bạn, và thuộc các dạng bạn cần luyện thêm.
4. **Hiển thị:** Cho bạn thấy thông tin bài tập, link đến bài đó, và lý do vì sao bài này được gợi ý.

## Cấu trúc của ứng dụng

- `codeforces_recommender.py`: File chính chứa toàn bộ code của ứng dụng.
- `cache/`: Thư mục để lưu dữ liệu bài tập (ứng dụng sẽ tự tạo thư mục này).

## Lưu ý

- Lần đầu chạy ứng dụng sẽ hơi lâu một chút vì phải tải dữ liệu bài tập về.
- Các lần sau sẽ nhanh hơn nhiều vì đã có dữ liệu lưu sẵn (dữ liệu này sẽ được cập nhật mỗi ngày).
