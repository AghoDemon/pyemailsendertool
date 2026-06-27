import smtplib
import json
import random
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# You Can Set The Email And APP Password On The Main APP Too!
class EmailPrankster:
    def __init__(self, email: str, password: str, messages_file: str = "messages.json"):
        self.email = email
        self.password = password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.messages_file = Path(messages_file)
        self.message_data = self._load_messages()
        self.sent_count = 0
        self.daily_limit = 490

# They are Default Messages You Can Edit This  
    def _load_messages(self) -> Dict:
        if not self.messages_file.exists():
            default_messages = {
                "subjects": [
                    "Spammer Tool Made By Demon github.com/aghodemon/pyemailsendertool",
                ],
                "bodies": [
                    "Made By Demon1795 | Free Version V2 | Email Spammer | Github.Com/AghoDemon/poemailsendertool.",
                    
                    "Made By Demon1795 | Free Version V2 | Email Spammer | Github.Com/AghoDemon/poemailsendertool."
                ]
            }
            self._save_messages(default_messages)
            return default_messages
        
        with open(self.messages_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_messages(self, data: Dict) -> None:
        with open(self.messages_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_subject(self, subject: str) -> None:
        self.message_data["subjects"].append(subject)
        self._save_messages(self.message_data)

    def add_body(self, body: str) -> None:
        self.message_data["bodies"].append(body)
        self._save_messages(self.message_data)

    def remove_subject(self, index: int) -> None:
        if 0 <= index < len(self.message_data["subjects"]):
            removed = self.message_data["subjects"].pop(index)
            self._save_messages(self.message_data)
            print(f"Removed subject: {removed}")

    def remove_body(self, index: int) -> None:
        if 0 <= index < len(self.message_data["bodies"]):
            removed = self.message_data["bodies"].pop(index)
            self._save_messages(self.message_data)
            print(f"Removed body: {removed}")

    def get_random_subject(self) -> str:
        return random.choice(self.message_data["subjects"])

    def get_random_body(self) -> str:
        return random.choice(self.message_data["bodies"])

    def create_email(self, recipient: str, subject: Optional[str] = None, body: Optional[str] = None) -> MIMEMultipart:
        if subject is None:
            subject = self.get_random_subject()
        if body is None:
            body = self.get_random_body()
        
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        return msg

    def send_email(self, recipient: str, subject: Optional[str] = None, body: Optional[str] = None, delay: int = 0) -> bool:
        if self.sent_count >= self.daily_limit:
            print(f"Daily limit of {self.daily_limit} emails reached")
            return False

        try:
            msg = self.create_email(recipient, subject, body)
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            self.sent_count += 1
            
            if delay > 0:
                time.sleep(delay)
            
            print(f"Email sent to {recipient} [{self.sent_count}/{self.daily_limit}]")
            return True
            
        except Exception as e:
            print(f"Failed to send to {recipient}: {str(e)}")
            return False

    def send_random_spam(self, recipients: List[str], max_emails: int = 10, delay: int = 3) -> Dict:
        print(f"\nStarting random spam campaign to {len(recipients)} recipients")
        print(f"Maximum emails per person: {max_emails}")
        print("-" * 50)
        
        results = {
            "total_sent": 0,
            "total_failed": 0,
            "per_recipient": {}
        }
        
        for recipient in recipients:
            sent_count = 0
            failed_count = 0
            email_count = random.randint(1, max_emails)
            
            print(f"\nProcessing {recipient} - {email_count} emails")
            
            for i in range(email_count):
                if self.sent_count >= self.daily_limit:
                    print(f"Daily limit reached. Stopping campaign.")
                    return results
                
                if self.send_email(recipient, delay=delay):
                    sent_count += 1
                    results["total_sent"] += 1
                else:
                    failed_count += 1
                    results["total_failed"] += 1
                
                if i < email_count - 1:
                    time.sleep(delay)
            
            results["per_recipient"][recipient] = {
                "sent": sent_count,
                "failed": failed_count,
                "total": email_count
            }
            
            print(f"Completed {recipient}: {sent_count} sent, {failed_count} failed")
            time.sleep(delay * 2)
        
        return results

    def send_targeted_spam(self, recipients: List[str], subject: Optional[str] = None, body: Optional[str] = None, count: int = 3, delay: int = 5) -> Dict:
        print(f"\nStarting targeted spam campaign to {len(recipients)} recipients")
        print(f"Emails per person: {count}")
        print("-" * 50)
        
        results = {
            "total_sent": 0,
            "total_failed": 0,
            "per_recipient": {}
        }
        
        for recipient in recipients:
            sent_count = 0
            failed_count = 0
            
            print(f"\nSending to {recipient}")
            
            for i in range(count):
                if self.sent_count >= self.daily_limit:
                    print(f"Daily limit reached. Stopping campaign.")
                    return results
                
                if self.send_email(recipient, subject, body, delay):
                    sent_count += 1
                    results["total_sent"] += 1
                else:
                    failed_count += 1
                    results["total_failed"] += 1
            
            results["per_recipient"][recipient] = {
                "sent": sent_count,
                "failed": failed_count,
                "total": count
            }
            
            print(f"Completed {recipient}: {sent_count} sent, {failed_count} failed")
            time.sleep(delay)
        
        return results

    def preview_email(self, recipient: str = "friend@example.com", subject: Optional[str] = None, body: Optional[str] = None) -> None:
        if subject is None:
            subject = self.get_random_subject()
        if body is None:
            body = self.get_random_body()
        
        print("\n" + "=" * 60)
        print("EMAIL PREVIEW")
        print("=" * 60)
        print(f"To: {recipient}")
        print(f"Subject: {subject}")
        print("-" * 60)
        print(body)
        print("=" * 60)


def display_menu() -> None:
    print("\n" + "=" * 60)
    print("EMAIL Spammer v2.0")
    print("=" * 60)
    print("\n1. Send random spam campaign")
    print("2. Send targeted spam campaign")
    print("3. Send single email")
    print("4. Manage message database")
    print("5. Preview random email")
    print("6. View statistics")
    print("7. Exit")
    print("-" * 60)


def manage_messages(prankster: EmailPrankster) -> None:
    while True:
        print("\n" + "=" * 60)
        print("MESSAGE DATABASE MANAGEMENT")
        print("=" * 60)
        print("\n1. View all subjects")
        print("2. View all bodies")
        print("3. Add new subject")
        print("4. Add new body")
        print("5. Remove subject")
        print("6. Remove body")
        print("7. Return to main menu")
        print("-" * 60)
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            print("\nSUBJECTS:")
            for i, subject in enumerate(prankster.message_data["subjects"]):
                print(f"{i}. {subject}")
        
        elif choice == "2":
            print("\nBODIES:")
            for i, body in enumerate(prankster.message_data["bodies"]):
                print(f"{i}. {body[:50]}...")
        
        elif choice == "3":
            subject = input("Enter new subject: ")
            prankster.add_subject(subject)
            print("Subject added successfully!")
        
        elif choice == "4":
            body = input("Enter new body (press Enter twice to finish):\n")
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
            full_body = "\n".join(lines)
            prankster.add_body(full_body)
            print("Body added successfully!")
        
        elif choice == "5":
            print("\nSUBJECTS:")
            for i, subject in enumerate(prankster.message_data["subjects"]):
                print(f"{i}. {subject}")
            index = int(input("\nEnter index to remove: "))
            prankster.remove_subject(index)
        
        elif choice == "6":
            print("\nBODIES:")
            for i, body in enumerate(prankster.message_data["bodies"]):
                print(f"{i}. {body[:50]}...")
            index = int(input("\nEnter index to remove: "))
            prankster.remove_body(index)
        
        elif choice == "7":
            break
        
        else:
            print("Invalid choice")


def main() -> None:
    print("=" * 60)
    print("EMAIL SPAMMER v2.0")
    print("=" * 60)
    print("\nDISCLAIMER: Any incorrect usage of this tool is not our responsibility.")
    print("Gmail Limit Is 500 Mail In Day")
    print("Your IP and account may be monitored\n")
    
    try:
        sender_email = input("Enter your Gmail address: ")
        sender_password = getpass("Enter your Gmail(Or Ur MailService) App Password: ")
        
        prankster = EmailPrankster(sender_email, sender_password)
        
        while True:
            display_menu()
            choice = input("\nEnter your choice: ")
            
            if choice == "1":
                print("\nEnter recipients (one per line, press Enter twice to finish):")
                recipients = []
                while True:
                    email_input = input()
                    if not email_input:
                        break
                    recipients.append(email_input)
                
                if recipients:
                    max_emails = int(input("Maximum emails per recipient (1-10): ") or "5")
                    delay = int(input("Delay between emails in seconds (1-10): ") or "3")
                    
                    results = prankster.send_random_spam(recipients, max_emails, delay)
                    
                    print("\nCAMPAIGN COMPLETE")
                    print("=" * 60)
                    print(f"Total sent: {results['total_sent']}")
                    print(f"Total failed: {results['total_failed']}")
                    print("\nPer recipient:")
                    for recipient, stats in results["per_recipient"].items():
                        print(f"  {recipient}: {stats['sent']}/{stats['total']} sent")
            
            elif choice == "2":
                print("\nEnter recipients (one per line, press Enter twice to finish):")
                recipients = []
                while True:
                    email_input = input()
                    if not email_input:
                        break
                    recipients.append(email_input)
                
                if recipients:
                    custom_subject = input("Custom subject (press Enter for random): ")
                    custom_body = input("Custom body (press Enter for random): ")
                    count = int(input("Emails per recipient (1-5): ") or "3")
                    delay = int(input("Delay between emails in seconds (1-10): ") or "5")
                    
                    results = prankster.send_targeted_spam(
                        recipients,
                        custom_subject if custom_subject else None,
                        custom_body if custom_body else None,
                        count,
                        delay
                    )
                    
                    print("\nCAMPAIGN COMPLETE")
                    print("=" * 60)
                    print(f"Total sent: {results['total_sent']}")
                    print(f"Total failed: {results['total_failed']}")
                    print("\nPer recipient:")
                    for recipient, stats in results["per_recipient"].items():
                        print(f"  {recipient}: {stats['sent']}/{stats['total']} sent")
            
            elif choice == "3":
                recipient = input("Enter recipient email: ")
                custom_subject = input("Custom subject (press Enter for random): ")
                custom_body = input("Custom body (press Enter for random): ")
                
                prankster.send_email(
                    recipient,
                    custom_subject if custom_subject else None,
                    custom_body if custom_body else None
                )
            
            elif choice == "4":
                manage_messages(prankster)
            
            elif choice == "5":
                prankster.preview_email()
            
            elif choice == "6":
                print("\nSTATISTICS")
                print("=" * 60)
                print(f"Total emails sent today: {prankster.sent_count}")
                print(f"Daily limit: {prankster.daily_limit}")
                print(f"Remaining: {prankster.daily_limit - prankster.sent_count}")
                print(f"Total subjects: {len(prankster.message_data['subjects'])}")
                print(f"Total bodies: {len(prankster.message_data['bodies'])}")
            
            elif choice == "7":
                print("\nThank you for using Email Spammer By EvilDev!")
                break
            
            else:
                print("\nInvalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user")
    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()
