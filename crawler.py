import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert


class Crawler:
    def __init__(self, user_id, user_passwd, user_name):
        self.user_id = user_id
        self.user_passwd = user_passwd
        self.user_name = user_name
        self.subjects = set()
        self.initialized = False

    def get_user_name(self):
        return self.user_name

    def get_id(self):
        return self.id

    def get_passwd(self):
        return self.passwd

    def craw(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(
            "--force-device-scale-factor=0.67"
        )  # 67% 축소 7개 과목은 100%에서 다 표시되지 않기에.
        options.add_argument("window-size=5000, 5000")
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(5000, 5000)

        URL = "https://sso.daegu.ac.kr/dgusso/ext/tigersstd/login_form.do?Return_Url=https://tigersstd.daegu.ac.kr/nxrun/ssoLogin.jsp"
        driver.get(URL)
        print("로그인 시작")

        driver.find_element(By.XPATH, '//*[@id="usr_id"]').click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="usr_id"]'))
        )

        driver.find_element(By.XPATH, '//*[@id="usr_id"]').send_keys(self.user_id)
        driver.find_element(By.XPATH, '//*[@id="usr_pw"]').click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="usr_pw"]'))
        )

        driver.find_element(By.XPATH, '//*[@id="usr_pw"]').send_keys(self.user_passwd)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="idLoginForm"]/div[1]/div[3]/button')
            )
        )

        driver.find_element(
            By.XPATH, '//*[@id="idLoginForm"]/div[1]/div[3]/button'
        ).click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="Mainframe.VFrameSet.TopFrame.form.mnTop.item0:text"]',
                )
            )
        )

        driver.find_element(
            By.XPATH, '//*[@id="Mainframe.VFrameSet.TopFrame.form.mnTop.item0:text"]'
        ).click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="Mainframe.VFrameSet.HFrameSet.LeftFrame.form.tabMenu.tabMnu.form.grdMnLeft.body.gridrow_17.cell_17_0.celltreeitem.treeitemtext:text"]',
                )
            )
        )

        driver.find_element(
            By.XPATH,
            '//*[@id="Mainframe.VFrameSet.HFrameSet.LeftFrame.form.tabMenu.tabMnu.form.grdMnLeft.body.gridrow_17.cell_17_0.celltreeitem.treeitemtext:text"]',
        ).click()
        time.sleep(3)

        alert = Alert(driver)
        alert.accept()  # OK 클릭

        time.sleep(3)

        alert = Alert(driver)
        alert.accept()  # OK 클릭

        time.sleep(3)

        data = []

        row_index = 0
        while True:
            try:
                # 행 선택자 (예: gridrow_0, gridrow_1, ...)
                row_xpath = f'//*[@id="Mainframe.VFrameSet.HFrameSet.innerVFrameSet.innerHFrameSet.innerVFrameSet2.WorkFrame.0001692.form.grdSngj.body.gridrow_{row_index}"]'
                row_element = driver.find_element(By.XPATH, row_xpath)

                # 행 내 셀들 찾기 (예: cell_0, cell_1, cell_2 ... )
                cells = row_element.find_elements(
                    By.XPATH, ".//div[contains(@id, 'cell')]"
                )

                row_data = []
                for cell in cells:
                    row_data.append(cell.text.strip())

                data.append(row_data)
                row_index += 1

            except Exception:
                # 더 이상 행이 없으면 루프 종료
                break

            # data는 2차원 리스트 (행렬) 형태로 저장됨

        ## 게시여부 판단 섹션
        new_subjects = []
        for row in data:
            if "O" in row:
                subject_name = row[2]
                if subject_name not in self.subjects:
                    new_subjects.append(subject_name)

        # 새로 발견한 과목들 기존 집합에 추가
        self.subjects.update(new_subjects)

        # 초기화 완료 표시
        self.initialized = True
        driver.quit()
        # 새로 생긴 과목 리스트 리턴
        return new_subjects
