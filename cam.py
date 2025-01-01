import multiprocessing
import time
import torch



model = torch.hub.load("ultralytics/yolov5", "yolov5s")


def webcam():
    from detect import run  # Ensure you import run correctly from your YOLOv5 setup
    run(weights="runs/train/exp3/weights/best.pt", source=0, save_txt=True, save_conf=True, save_crop=True)


def start_webcam():
    # Create a new process to run the `webcam` function
    process = multiprocessing.Process(target=webcam)
    process.start()

    # Get the PID of the new process
    print(f"Webcam process started with PID: {process.pid}")

    time.sleep(45)

    # After 5 seconds, terminate the webcam process
    process.terminate()
    print(f"Webcam process terminated after 5 seconds.")
    # Return the process object if you want to manage it later
    return process


if __name__ == "__main__":
    process = start_webcam()

    print(f"The process PID is: {process.pid}")
