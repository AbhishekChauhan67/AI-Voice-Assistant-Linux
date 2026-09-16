
from .service import STT


def main():
    stt = STT()

    print()
    print("Press SPACE to start recording.")
    print("Press SPACE again to stop.")
    print("Press CTRL+C to exit.")
    print()

    try:
        while True:
            input("Press ENTER to start recording...")

            stt.start_recording()

            input("Press ENTER to stop recording...")

            audio = stt.stop_recording()

            if audio is None:
                print("No audio recorded.")
                continue

            print("Recognizing...")

            text = stt.recognize(audio)

            if text:
                print(f"You: {text}")
            else:
                print("No text recognized.")

            print()

    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()

