import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def fill_sakai_form():
    """酒井悠佑さん専用フォーム自動入力"""
    
    # フォームURL
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfoK1JgkqDUyPO4RpMnvH67dlzW489QKdcfS8MY5HcMFP25xQ/viewform?usp=header"
    
    # 入力データ
    name = "酒井悠佑"
    university = "大阪公立大学"
    grade_option = 2  # 上から3つ目（0から数えて2番目）
    
    print("🚀 酒井さん専用フォーム自動入力を開始します")
    print("=" * 50)
    
    # ChromeDriverの設定
    print("🔧 ChromeDriverを準備中...")
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # ヘッドレスモードにする場合はコメントアウト
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)
    
    try:
        print("📋 フォームを開いています...")
        driver.get(form_url)
        time.sleep(3)
        print("✅ フォーム読み込み完了")
        
        # フォーム構造を確認
        print("\n🔍 フォーム要素を確認中...")
        text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[jsname]")
        radio_groups = driver.find_elements(By.CSS_SELECTOR, "div[role='radiogroup']")
        
        print(f"📝 テキストフィールド: {len(text_inputs)}個発見")
        print(f"⚪ ラジオボタングループ: {len(radio_groups)}個発見")
        
        # 1. 名前を入力（1番目のテキストフィールド）
        print(f"\n📝 名前を入力中: {name}")
        if len(text_inputs) > 0:
            name_field = text_inputs[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", name_field)
            time.sleep(0.5)
            name_field.clear()
            name_field.send_keys(name)
            print("✅ 名前入力完了")
        else:
            print("❌ 名前フィールドが見つかりません")
            return False
        
        # 2. 大学を入力（2番目のテキストフィールド）
        print(f"\n🏫 大学を入力中: {university}")
        if len(text_inputs) > 1:
            university_field = text_inputs[1]
            driver.execute_script("arguments[0].scrollIntoView(true);", university_field)
            time.sleep(0.5)
            university_field.clear()
            university_field.send_keys(university)
            print("✅ 大学入力完了")
        else:
            print("❌ 大学フィールドが見つかりません")
            return False
        
        # 3. 学年を選択（ラジオボタンの3番目）
        print(f"\n🎓 学年を選択中: 上から{grade_option + 1}番目")
        if len(radio_groups) > 0:
            grade_group = radio_groups[0]  # 最初のラジオボタングループ
            driver.execute_script("arguments[0].scrollIntoView(true);", grade_group)
            time.sleep(0.5)
            
            radio_options = grade_group.find_elements(By.CSS_SELECTOR, "div[role='radio']")
            print(f"📊 選択肢数: {len(radio_options)}個")
            
            if grade_option < len(radio_options):
                selected_option = radio_options[grade_option]
                driver.execute_script("arguments[0].click();", selected_option)
                print("✅ 学年選択完了")
            else:
                print(f"❌ {grade_option + 1}番目の選択肢が見つかりません")
                return False
        else:
            print("❌ 学年のラジオボタンが見つかりません")
            return False
        
        # 入力結果を確認
        print("\n📋 入力内容確認:")
        print(f"   名前: {name}")
        print(f"   大学: {university}")
        print(f"   学年: 上から{grade_option + 1}番目を選択")
        
        # 送信前の確認
        print("\n⏸️ 入力が完了しました。内容をご確認ください。")
        response = input("📤 フォームを送信しますか？ (y/n): ")
        
        if response.lower() == 'y':
            # 4. フォームを送信
            print("\n📤 フォームを送信中...")
            
            # 送信ボタンを探す
            submit_selectors = [
                "//span[contains(text(), '送信')]",
                "//span[contains(text(), 'Submit')]",
                "//input[@type='submit']",
                "//button[@type='submit']",
                "//*[@role='button' and contains(text(), '送信')]"
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if submit_button:
                driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                time.sleep(1)
                submit_button.click()
                print("✅ フォーム送信完了！")
                time.sleep(3)
                
                # 送信完了ページの確認
                if "formResponse" in driver.current_url or "送信" in driver.page_source:
                    print("🎉 フォームが正常に送信されました！")
                else:
                    print("⚠️ 送信状態を確認してください")
                
                return True
            else:
                print("❌ 送信ボタンが見つかりません")
                return False
        else:
            print("⏸️ 送信をキャンセルしました")
            return False
            
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return False
    
    finally:
        print("\n⏰ 5秒後にブラウザを閉じます...")
        time.sleep(5)
        driver.quit()
        print("🔚 処理完了")

def main():
    """メイン実行関数"""
    print("🤖 酒井悠佑さん専用 - Googleフォーム自動入力")
    print("📋 入力内容:")
    print("   名前: 酒井悠佑")
    print("   大学: 大阪公立大学") 
    print("   学年: 上から3番目を選択")
    print("=" * 50)
    
    success = fill_sakai_form()
    
    if success:
        print("\n🎉 全ての処理が正常に完了しました！")
    else:
        print("\n⚠️ 処理中にエラーが発生しました。")
        print("💡 以下を確認してください:")
        print("   - インターネット接続")
        print("   - フォームがアクセス可能か")
        print("   - フォーム構造が変更されていないか")

if __name__ == "__main__":
    main()