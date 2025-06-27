import time

def countdown_timer():
    try:
        minutes = int(input("Enter the countdown time in minutes: "))
        total_seconds = minutes * 60

        while total_seconds:
            mins, secs = divmod(total_seconds, 60)
            timer = f"{mins:02d}:{secs:02d}"
            print(timer, end="\r")  # overwrite the line each second
            time.sleep(1)
            total_seconds -= 1

        print("00:00")
        print("GAME OVER")
    except ValueError:
        print("Please enter a valid integer number.")

countdown_timer()
