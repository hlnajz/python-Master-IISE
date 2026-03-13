class Notifier:
    def send(self, message):
        """Base method to be overridden"""
        print(f"Base Notifier sending: {message}")

class EmailMixin:
    def send_email(self, message):
        print(f"Sending Email: {message}")

class SMSMixin:
    def send_sms(self, message):
        print(f"Sending SMS: {message}")

# Inherits from Notifier and both Mixins
class SmartNotifier(Notifier, EmailMixin, SMSMixin):
    def send(self, message, channel="email"):
        """Unified method to send message via specified channel"""
        if channel == "email":
            self.send_email(message)
        elif channel == "sms":
            self.send_sms(message)
        else:
            print(f"Unsupported channel: {channel}")

# Polymorphic function
def broadcast_message(notifiers, message):
    print(f"\n--- Broadcasting Message: '{message}' ---")
    for notifier in notifiers:
        # We need to know if it's a smart notifier to specify a channel
        if isinstance(notifier, SmartNotifier):
            notifier.send(message, channel="sms") # Defaulting to sms for demo
        else:
            notifier.send(message)

if __name__ == "__main__":
    # Test Scenario
    base_notifier = Notifier()
    smart_notifier = SmartNotifier()

    notifier_list = [base_notifier, smart_notifier]
    
    # Polymorphic broadcast
    broadcast_message(notifier_list, "System Update at 12:00 PM")