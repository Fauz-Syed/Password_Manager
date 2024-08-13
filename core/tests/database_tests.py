from core.password_manager.password_manager import PasswordManager
import os
file_name = "C:\\Users\\fauzs\\OneDrive\\Desktop\\Codes\\Projects 2024\\Password_Manager\\common\\configs\\config.yml"
test = PasswordManager(file_name)

def test_user_insert():


	test.insert_users_data()