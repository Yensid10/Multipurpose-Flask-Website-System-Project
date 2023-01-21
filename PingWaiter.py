from plyer import notification


class Notifty:
    def main(self, str):
        self.notification(str)

    def notification(self, string):
        notification.notify(
            title="Test Ping",
            message=string,
            app_icon="Waiter.ico",
            timeout=10,
        )


N = Notifty()
N.main("Calling for Help")
