# 웹 스프래핑

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from bs4 import BeautifulSoup

class NaverBookingScraper:
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        # Chrome 드라이버 설정
        options = webdriver.ChromeOptions()
        
        # 브라우저 옵션
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 개발 중에는 브라우저를 볼 수 있도록 headless 모드 비활성화
        # options.add_argument('--headless')
        
        # ChromeDriver 자동 관리
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # n---- pass
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def login_manually(self):
        """수동 로그인을 위해 로그인 페이지로 이동"""
        print("로그인 페이지로 이동합니다...")
        self.driver.get("https://nid.naver.com/nidlogin.login?svctype=1&locale=ko_KR&url=https%3A%2F%2Fnew.smartplace.naver.com%2F&area=bbt")
        
        print("수동으로 로그인해주세요.")
        print("로그인 완료 후 엔터를 눌러주세요.")
        input("로그인 완료 후 엔터를 눌러주세요...")
        
        # 로그인 확인
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("로그인이 완료된 것 같습니다!")
            return True
        except:
            print("로그인 확인에 실패했습니다.")
            return False
    

    def close(self):
        """브라우저 종료"""
        if self.driver:
            self.driver.quit()
            print("브라우저가 종료되었습니다.")

def main():
    """메인 실행 함수"""
    target_url = "https://partner.booking.naver.com/bizes/331452/booking-list-view?bookingStatusCodes=RC03&dateDropdownType=TODAY&dateFilter=REGDATE&endDateTime=today&startDateTime=today"
    
    scraper = NaverBookingScraper()
    
    try:
        # 1. 로그인
        if scraper.login_manually():
            # 2. 예약 목록 페이지로 이동
            if scraper.navigate_to_booking_list(target_url):
                # 3. 페이지 구조 분석
                analysis = scraper.save_page_analysis()
                
                # 4. 데이터 추출 시도
                scraper.extract_booking_data()
                
                print("\n=== 다음 단계 ===")
                print("1. page_analysis.json 파일을 확인해보세요")
                print("2. 브라우저에서 개발자 도구(F12)로 실제 예약 데이터 구조를 확인해보세요")
                print("3. 구조 파악 후 extract_booking_data 함수를 수정하겠습니다")
                
                # 브라우저를 잠시 열어두어 구조 확인 가능하도록
                input("\n구조 확인 후 엔터를 눌러 종료하세요...")
        
    except Exception as e:
        print(f"오류 발생: {e}")
    
    finally:
        scraper.close()

if __name__ == "__main__":
    main()