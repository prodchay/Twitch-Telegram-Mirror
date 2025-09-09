import subprocess

def main():
    print("Starting Bots...")

    forward_to_twitch = "forward_to_twitch.py"
    twitch_to_telegram = "forward_to_telegram.py"

    p1 = subprocess.Popen(["python", forward_to_twitch])
    p2 = subprocess.Popen(["python", twitch_to_telegram])

    p1.wait()
    p2.wait()

if __name__ == "__main__":
    main()