from locust import HttpUser, TaskSet, task, between

class AdminBehavior(TaskSet):
    def on_start(self):
        """Log in as the admin user."""
        self.login()

    def login(self):
        response = self.client.post("/login", data={
            "email": "admin@example.com",  # Replace with actual admin email
            "password": "adminpassword"    # Replace with actual admin password
        })
        
        if response.status_code == 200 and "Welcome" in response.text:
            print("Admin login successful")
        else:
            print("Admin login failed")

    @task
    def admin_homepage(self):
        self.client.get("/admin/home")

    @task
    def choose_user(self):
        with self.client.get("/admin/choose_user", catch_response=True) as response:
            if "Pick One User" in response.text:
                self.client.post("/admin/choose_user", data={"choice": "1"})  # Replace "1" with actual user ID

    @task
    def choose_file(self):
        with self.client.get("/admin/choose_file?user=1", catch_response=True) as response:
            if "Choose File" in response.text:
                self.client.post("/admin/choose_file", data={"choice": "1"})  # Replace "1" with actual file ID

    @task
    def view_data(self):
        self.client.get("/admin/view_data?userID=1&fileID=1")  # Replace with actual IDs
    
    @task
    def view_corr(self):
        self.client.get("/admin/view_corr?userID=1&fileID=1")  # Replace with actual IDs

class NormalUserBehavior(TaskSet):
    def on_start(self):
        """Log in as a normal user."""
        self.login()

    def login(self):
        response = self.client.post("/login", data={
            "email": "user@example.com",  # Replace with actual user email
            "password": "userpassword"    # Replace with actual user password
        })
        
        if response.status_code == 200 and "Welcome" in response.text:
            print("User login successful")
        else:
            print("User login failed")

    @task
    def load_homepage(self):
        self.client.get("/")

    @task
    def upload_file(self):
        files = {'file': ('testfile.csv', 'some,data\n')}
        self.client.post("/upload", files=files)
    
    @task
    def analytics_page(self):
        with self.client.get("/analytics", catch_response=True) as response:
            if "Pick a file to analyze" in response.text:
                self.client.post("/analytics", data={"choice": "1"})  # Replace "1" with actual file ID

class AdminUser(HttpUser):
    tasks = [AdminBehavior]
    wait_time = between(1, 5)
class NormalUser(HttpUser):
    tasks = [NormalUserBehavior]
    wait_time = between(1, 5)
