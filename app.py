# 쿠팡 화장품 멀티프로세싱으로 가져오기
import requests
from bs4 import BeautifulSoup
import time

from multiprocessing import Pool

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
}

# 가격표에 게시글 링크를 가져옵니다.
def get_links():
    data = []

    for idx in range(1, 17):
        url = "http://www.coupang.com/np/categories/176860?page=" + str(idx)
        data.append(url)
    return data


# 상품과 가격을 가져옵니다.
def get_content(link):
    url = link
    result = requests.get(url, headers=headers)

    soup_obj = BeautifulSoup(result.content, "html.parser")

    div = soup_obj.findAll("div", {"class": "name"})
    lis = soup_obj.find("ul", {"id": "productList"}).findAll("li")

    for li in lis:
        product = li.find("div", {"class": "name"})
        price = li.find("em", {"class": "sale"}).find(
            "strong", {"class": "price-value"}
        )
        print("화장품명: " + product.text.strip() + " / " + "상품가격: " + price.text.strip())


if __name__ == "__main__":
    start_time = time.time()
    # 32개 프로세스 사용 / 테스트 결과 ----3.2799859046936035 seconds-----
    pool = Pool(processes=32)
    pool.map(get_content, get_links())
    print("----%s seconds-----" % (time.time() - start_time))

