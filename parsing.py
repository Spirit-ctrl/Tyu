from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def get_schedule():
    
    o = Options()
    o.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=o) 

    driver.get("https://my.tyuiu.ru/")


    element = driver.find_element(By.ID, "email")
    element.send_keys(getenv("LOGIN")) # type: ignore


    element = driver.find_element(By.ID, "password")
    element.send_keys(getenv("PASSWORD")) # type: ignore


    button_element = driver.find_element(By.NAME, "login")
    button_element.click()

    driver.get(getenv("URL_SCHEDULE")) # type: ignore



    soup = BeautifulSoup(driver.page_source, "lxml")

    week = soup.find("div", class_= "my-schedule-table")

    week = week.find_all("div", class_= "table-cell-event")# type: ignore


    schedule = [[], [], [], [], [], [], [], []]

    for i in range(8):
        for j in range(6):
            schedule[j].append(week[i*6 + j].text)

    
    
    for i in range(6):
        for j in range(8):
            if schedule[i][j].find("Подгруппа 1") != -1:
                schedule[i][j] = schedule[i][j][:schedule[i][j].find("Подгруппа 1"):]
            elif schedule[i][j] == "":
                schedule[i][j] = "Нет пары"
            elif schedule[i][j].find("Подгруппа 2") != -1:
                schedule[i][j] = "Нет пары"
            elif schedule[i][j] != "Нет пары":
                text = schedule[i][j]
                
                # Отделяем тип занятия
                lesson_type = ""
                if "Лекция" in text:
                    lesson_type = "Лекция"
                    text = text.replace("Лекция", "").strip()
                elif "Практика" in text:
                    lesson_type = "Практика"
                    text = text.replace("Практика", "").strip()
                elif "Лабораторная" in text:
                    lesson_type = "Лабораторная"
                    text = text.replace("Лабораторная", "").strip()
                
                # Простое разделение по ключевым словам
                parts = text.split()
                subject_parts = []
                corpus_parts = []
                fio_parts = []
                
                mode = "subject"
                for word in parts:
                    if "Корпус" in word:
                        mode = "corpus"
                    elif mode == "corpus" and word.endswith(")") and len(corpus_parts) > 0:
                        corpus_parts.append(word)
                        mode = "fio"
                        continue
                    
                    if mode == "subject":
                        subject_parts.append(word)
                    elif mode == "corpus":
                        corpus_parts.append(word)
                    else:
                        fio_parts.append(word)
                
                subject = " ".join(subject_parts)
                corpus = " ".join(corpus_parts)
                fio = " ".join(fio_parts)
                
                # Формируем результат
                result_parts = []
                if subject:
                    result_parts.append(subject)
                if lesson_type:
                    result_parts.append(lesson_type)
                if corpus:
                    result_parts.append(corpus)
                if fio:
                    result_parts.append(fio)
                
                if result_parts:
                    schedule[i][j] = "\n".join(result_parts)
                else:
                    schedule[i][j] = text
    
    driver.quit()
    return schedule
       

        
def get_schedule_next():
    
    o = Options()
    o.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=o) 

    driver.get("https://my.tyuiu.ru/")


    element = driver.find_element(By.ID, "email")
    element.send_keys(getenv("LOGIN")) # type: ignore


    element = driver.find_element(By.ID, "password")
    element.send_keys(getenv("PASSWORD")) # type: ignore


    button_element = driver.find_element(By.NAME, "login")
    button_element.click()

    driver.get(getenv("URL_SCHEDULE")) # type: ignore

    # Нажимаем кнопку "Следующая неделя"
    next_week_button = driver.find_element(By.CLASS_NAME, "btn-next-week")
    next_week_button.click()

    soup = BeautifulSoup(driver.page_source, "lxml")

    week = soup.find("div", class_= "my-schedule-table-wrapper")

    week = week.find_all("div", class_= "table-cell-event")# type: ignore


    schedule = [[], [], [], [], [], [], [], []]

    for i in range(8):
        for j in range(6):
            schedule[j].append(week[i*6 + j].text)

    
    
    for i in range(6):
        for j in range(8):
            if schedule[i][j].find("Подгруппа 1") != -1:
                schedule[i][j] = schedule[i][j][:schedule[i][j].find("Подгруппа 1"):]
            elif schedule[i][j] == "":
                schedule[i][j] = "Нет пары"
            elif schedule[i][j].find("Подгруппа 2") != -1:
                schedule[i][j] = "Нет пары"
            elif schedule[i][j] != "Нет пары":
                text = schedule[i][j]
                
                # Отделяем тип занятия
                lesson_type = ""
                if "Лекция" in text:
                    lesson_type = "Лекция"
                    text = text.replace("Лекция", "").strip()
                elif "Практика" in text:
                    lesson_type = "Практика"
                    text = text.replace("Практика", "").strip()
                elif "Лабораторная" in text:
                    lesson_type = "Лабораторная"
                    text = text.replace("Лабораторная", "").strip()
                
                # Простое разделение по ключевым словам
                parts = text.split()
                subject_parts = []
                corpus_parts = []
                fio_parts = []
                
                mode = "subject"
                for word in parts:
                    if "Корпус" in word:
                        mode = "corpus"
                    elif mode == "corpus" and word.endswith(")") and len(corpus_parts) > 0:
                        corpus_parts.append(word)
                        mode = "fio"
                        continue
                    
                    if mode == "subject":
                        subject_parts.append(word)
                    elif mode == "corpus":
                        corpus_parts.append(word)
                    else:
                        fio_parts.append(word)
                
                subject = " ".join(subject_parts)
                corpus = " ".join(corpus_parts)
                fio = " ".join(fio_parts)
                
                # Формируем результат
                result_parts = []
                if subject:
                    result_parts.append(subject)
                if lesson_type:
                    result_parts.append(lesson_type)
                if corpus:
                    result_parts.append(corpus)
                if fio:
                    result_parts.append(fio)
                
                if result_parts:
                    schedule[i][j] = "\n".join(result_parts)
                else:
                    schedule[i][j] = text
    
    driver.quit()
    return schedule


