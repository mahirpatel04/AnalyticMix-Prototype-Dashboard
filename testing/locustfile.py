from locust import HttpUser, TaskSet, task, between
import random
import string
import re

class GeneralUserTasks(TaskSet):
    def on_start(self):
        self.user_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        self.signup()
        self.login()
        print("User", self.user_id, 'logged in')

    def signup(self):
        self.client.post("/sign-up", data={
            "email": f"user_{self.user_id}@example.com",
            "firstName": f"User{self.user_id}",
            "password1": "password123",
            "password2": "password123"
        })
        print("User", self.user_id, "signed up")

    def login(self):
        self.client.post("/login", data={
            "email": f"user_{self.user_id}@example.com",
            "password": "password123"
        })
        print("User", self.user_id, 'logged in')

    @task(1)
    def upload_csv(self):
        with open("sample.csv", "rb") as file:
            response = self.client.post("/upload", files={"file": file})
        if response.ok:
            print("User", self.user_id, 'uploaded CSV file successfully')
        else:
            print("User", self.user_id, 'failed to upload CSV file', response.status_code)
        
    @task(3)
    def analytics(self):
        self.client.get("/analytics")
        print("User", self.user_id, 'viewed analytics')
    
    @task(3)
    def home(self):
        self.client.get("/")
    
    




class AdminUserTasks(TaskSet):
    def on_start(self):
        self.login()

    @task
    def select_user_task(self):
        # Step 1: Choose a User
        response = self.client.get("/admin/choose_user")
        self.user_id = self.select_user(response.text)
        print(f'Selected User ID: {self.user_id}')

    @task
    def select_file_task(self):
        # Step 2: Choose a File for the selected user
        if hasattr(self, 'user_id'):
            response = self.client.get(f"/admin/choose_file?user={self.user_id}")
            self.file_id = self.select_file(response.text)
            print(f'Selected File ID: {self.file_id}')

    @task
    def analyze_file_task(self):
        # Step 3: Analyze the selected file
        if hasattr(self, 'user_id') and hasattr(self, 'file_id'):
            self.client.post(f"/admin/analyze_file?userID={self.user_id}&file={self.file_id}", data={
                'choice1': ['column1', 'column2'],  # Replace with real column names
                'choice2': ['target_column'],       # Replace with real target column
                'choice3': ['Linear']               # Replace with chosen model(s)
            })
            print("File Analyzed")

    @task
    def view_data_task(self):
        # Step 4: View Data for the selected file
        if hasattr(self, 'user_id') and hasattr(self, 'file_id'):
            self.client.get(f"/admin/view_data?userID={self.user_id}&fileID={self.file_id}")
            print("Viewed Data")

    @task
    def view_correlation_task(self):
        # Step 5: View Correlation for the selected file
        if hasattr(self, 'user_id') and hasattr(self, 'file_id'):
            self.client.get(f"/admin/view_corr?userID={self.user_id}&fileID={self.file_id}")
            print("Viewed Correlation")

    @task
    def logout_task(self):
        # Step 6: Logout
        self.client.get("/logout")
        print("Admin Logged Out")
        self.interrupt()

    def login(self):
        self.client.post("/login", data={
            "email": "admin@gmail.com",
            "password": "password"
        })
        print('Admin Logged In')

    def select_user(self, response_text):
        match = re.search(r'<option value="(\d+)">', response_text)
        if match:
            return match.group(1)
        else:
            raise ValueError("No user ID found in the response")

    def select_file(self, response_text):
        match = re.search(r'<option value="(\d+)">', response_text)
        if match:
            return match.group(1)
        else:
            raise ValueError("No file ID found in the response")



class GeneralUser(HttpUser):
    tasks = [GeneralUserTasks]
    wait_time = between(1, 5)
    weight = 999

class AdminUser(HttpUser):
    tasks = [AdminUserTasks]
    wait_time = between(5, 10)
    weight = 1