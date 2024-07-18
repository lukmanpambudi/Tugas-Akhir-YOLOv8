import cv2
import numpy as np
import utilsV2
from ultralytics import YOLO
import time

last_mask_time = time.time()

def getLane(results, display=2):
    global last_mask_time
    frameCopy = frame.copy()

    mask_np = utilsV2.masking(results)
    if mask_np is not None:
        last_mask_time = time.time()  
        points = utilsV2.valTrackbars()
        hT, wT, c = frame.shape
        
        frameWarp = utilsV2.warping(mask_np, points, wT, hT)
        if frameWarp is None or frameWarp.size == 0:
            print("Error: frameWarp is invalid or has zero size.")
            return
        else: 
            print("ada nilai framewarp")

        frameWarpPoints = utilsV2.drawPoints(frameCopy, points)
        processedImage = utilsV2.isEndOfLane(results, model, frameWarp, display=True)
        if processedImage is None or processedImage.size == 0:
            print("processedImage tidak ada nilainya ")
            return
        else: 
            print("ada nilai processed image")
            

        if display == 1:
            stack_img = utilsV2.stackImages(0.7, ([tampilResults, frameWarpPoints], [mask_np, frameWarp]))
            cv2.imshow('Stacked Image', stack_img)
            cv2.imshow('Processed Image', processedImage)


        elif display == 2:
            # cv2.imshow("Result Instance Segmentation", tampilResults)
            stack_img = utilsV2.stackImages(0.7, ([frameWarpPoints, mask_np], [frameWarp, processedImage]))
            cv2.imshow('Stacked Image', stack_img)
            
            # cv2.imshow('Masking', mask_np)
            # cv2.imshow('Warp', frameWarp)
            


    else:
        # Tutup window jika tidak ada nilai baru dalam 10 detik
        current_time = time.time()
        if current_time - last_mask_time > 15:
            if cv2.getWindowProperty("Masking", cv2.WND_PROP_VISIBLE) > 0:
                cv2.destroyWindow("Masking")
            if cv2.getWindowProperty("Warp", cv2.WND_PROP_VISIBLE) > 0:
                cv2.destroyWindow("Warp")
            if cv2.getWindowProperty("Warp Points", cv2.WND_PROP_VISIBLE) > 0:
                cv2.destroyWindow("Warp Points")
            if cv2.getWindowProperty("Processed Image", cv2.WND_PROP_VISIBLE) > 0:
                cv2.destroyWindow("Processed Image")
            if cv2.getWindowProperty("Stacked Image", cv2.WND_PROP_VISIBLE) > 0:
                cv2.destroyWindow("Stacked Image")
            if cv2.getWindowProperty("Result Instance Segmentation", cv2.WND_PROP_VISIBLE) > 0:
                cv2.destroyWindow("Result Instance Segmentation")


if __name__ == '__main__':
    # model = YOLO("/home/pambudi/Yolov8/model/YOLO8n/YOLO8n_6Juli.pt")
    model = YOLO("/home/pambudi/Yolov8/model/YOLO8n/YOLO8n_13Juli.pt")
    # model = YOLO("/home/pambudi/Yolov8/model/YOLO8n/best4juni_416.pt")
    video_path = ("/home/pambudi/Yolov8/model/WIN_20240530_16_26_19_Pro.mp4")
    # video_path = ("/home/pambudi/Yolov8/model/EndTrack.mp4")

    cap = cv2.VideoCapture(video_path)    
    # cap = cv2.VideoCapture(2)    
    if not cap.isOpened():
        print("Gagal membuka video.")
        exit()
    initializeTrackBarVals = [8, 128, 0, 179]
    # initializeTrackBarVals = [8, 136, 0, 179]
    utilsV2.initializeTrackbars(initializeTrackBarVals)
    frameCounter = 0

    
    while True:
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0

        ret, video = cap.read()
        if not ret:
            print("Gagal membaca frame dari video.")
            break
        
        frame = utilsV2.tambahkan_bingkai(video)
        frame = cv2.resize(frame, (512, 256))
        # results = model(frame, imgsz=416, conf=0.5)
        results = model(frame, imgsz=416, conf=0.5)
        tampilResults = results[0].plot()
        getLane(results, display=2)
        cv2.imshow("Result Instance Segmentation", tampilResults)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()