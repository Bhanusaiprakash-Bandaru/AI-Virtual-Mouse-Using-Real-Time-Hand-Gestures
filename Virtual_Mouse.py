import cv2 # type: ignore
import numpy as np # type: ignore
import HandtrackingModule as htm # type: ignore
import time
import autopy # type: ignore
import pyautogui # type: ignore

# ---------------- ICON ASSETS ----------------
gesture_icons = {
    "MOVE": cv2.imread("assets/move.png", cv2.IMREAD_UNCHANGED),
    "LEFT_CLICK": cv2.imread("assets/left_click.png", cv2.IMREAD_UNCHANGED),
    "RIGHT_CLICK": cv2.imread("assets/right_click.png", cv2.IMREAD_UNCHANGED),
    "SCROLL_DOWN": cv2.imread("assets/scroll_down.png", cv2.IMREAD_UNCHANGED),
    "SCROLL_UP": cv2.imread("assets/scroll_up.png", cv2.IMREAD_UNCHANGED),
    "DOUBLE_CLICK": cv2.imread("assets/double_click.png", cv2.IMREAD_UNCHANGED),
}

# sanity check (remove later)
for k, v in gesture_icons.items():
    if v is None:
        print(f"ERROR loading icon: {k}")


# ---------------- SETTINGS ----------------
wCam, hCam = 1280, 720
displayW, displayH = 1200, 700
frameR = 40
smoothening = 7


pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
dragging = False

lastScreenshotTime = 0
showScreenshotMsg = 0
screenshotHoldStart = 0   

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

def overlay_png(bg, fg, x, y, size=(40, 40)):
    #fg = cv2.resize(fg, size)
    fg = cv2.resize(fg, size, interpolation=cv2.INTER_NEAREST)

    # If image has no alpha channel, add one
    if fg.shape[2] == 3:
        alpha_channel = np.ones((fg.shape[0], fg.shape[1]), dtype=fg.dtype) * 255
        fg = np.dstack((fg, alpha_channel))

    b, g, r, a = cv2.split(fg)
    alpha = a.astype(float) / 255.0

    for c in range(3):
        bg[y:y+size[1], x:x+size[0], c] = (
            alpha * fg[:, :, c] +
            (1 - alpha) * bg[y:y+size[1], x:x+size[0], c]
        )



def draw_instructions(img):
    overlay = img.copy()
    h, w, _ = img.shape

    # PANEL SETTINGS
    panel_width = 240
    x_start = 10

    # LAYOUT SETTINGS
    y = 60
    gap = 72
    icon_size = 64
    card_pad = 12
    rows = 6

    panel_bottom = y + rows * gap + 20

    # MAIN PANEL BACKGROUND
    cv2.rectangle(
        overlay,
        (x_start, 10),
        (x_start + panel_width, panel_bottom),
        (0, 0, 0),
        -1
    )
    img = cv2.addWeighted(overlay, 0.55, img, 0.45, 0)

    # TITLE
    cv2.putText(
        img,
        "CONTROLS",
        (x_start + 10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    # ROW DRAW FUNCTION
    def draw_row(icon_key, label, y):
        # icon background card
        cv2.rectangle(
            img,
            (x_start + 20 - card_pad, y - card_pad),
            (x_start + 20 + icon_size + card_pad, y + icon_size + card_pad),
            (100, 100, 100),
            -1
        )

        # icon
        overlay_png(
            img,
            gesture_icons[icon_key],
            x_start + 20,
            y,
            size=(icon_size, icon_size)
        )

        # label
        text_x = x_start + 20 + icon_size + card_pad + 20
        text_y = y + int(icon_size * 0.7)

        cv2.putText(
            img,
            label,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )


    # DRAW ROWS
    draw_row("MOVE", "Move Cursor", y); y += gap
    draw_row("LEFT_CLICK", "Left Click", y); y += gap
    draw_row("RIGHT_CLICK", "Right Click", y); y += gap
    draw_row("SCROLL_UP", "Scroll Up", y); y += gap
    draw_row("SCROLL_DOWN", "Scroll Down", y); y += gap
    draw_row("DOUBLE_CLICK", "Double Click", y)

    return img

while True:

    success, img = cap.read()
    if not success or img is None:
        continue

    #cv2.imshow("RAW", img)

    actionText = "READY"

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:

        x1, y1 = lmList[8][1:]   # Index
        fingers = detector.fingersUp()
        # fingers = [Thumb, Index, Middle, Ring, Pinky]

        # CONTROL FRAME
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)
        
        # -------- MOVE --------
        if fingers == [0, 1, 0, 0, 0]:
            actionText = "MOVE"
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            autopy.mouse.move(wScr - clocX, clocY)
            plocX, plocY = clocX, clocY

        # -------- LEFT CLICK --------
        elif fingers == [0, 1, 1, 0, 0]:
            length, img, _ = detector.findDistance(8, 12, img)
            if length < 40:
                autopy.mouse.click()
                actionText = "LEFT CLICK"

        # -------- RIGHT CLICK --------
        elif fingers == [1, 1, 0, 0, 0]:
            length, img, _ = detector.findDistance(4, 8, img)
            if length < 40:
                autopy.mouse.click(button=autopy.mouse.Button.RIGHT)
                actionText = "RIGHT CLICK"
                time.sleep(0.2)

        # -------- DOUBLE CLICK --------
        elif fingers == [0, 1, 1, 1, 0]:
            autopy.mouse.click()
            autopy.mouse.click()
            actionText = "DOUBLE CLICK"
            time.sleep(0.2)

        # -------- SCROLL UP --------
        elif fingers == [0, 1, 1, 0, 1]:
            pyautogui.scroll(50)
            actionText = "SCROLL UP"

        # -------- SCROLL DOWN --------
        elif fingers == [0, 1, 0, 0, 1]:
            pyautogui.scroll(-50)
            actionText = "SCROLL DOWN"

        # -------- DRAG & DROP --------
        else:
            length, img, _ = detector.findDistance(4, 8, img)
            if length < 35 and not dragging:
                dragging = True
                autopy.mouse.toggle(down=True)
                actionText = "DRAGGING"
            elif length > 50 and dragging:
                dragging = False
                autopy.mouse.toggle(down=False)
                actionText = "DROP"

        # -------- SCREENSHOT --------
        
        if fingers[0] == 1 and fingers[2] == 1 and fingers[1] == 0:
            length2, img, _ = detector.findDistance(4, 12, img)

            if length2 < 40:
                if screenshotHoldStart == 0:
                    screenshotHoldStart = time.time()

                elif time.time() - screenshotHoldStart > 0.3:
                    filename = f"screenshot_{int(time.time())}.png"
                    pyautogui.screenshot(filename)
                    actionText = "SCREENSHOT SAVED"
                    showScreenshotMsg = 15
                    lastScreenshotTime = time.time()
                    screenshotHoldStart = 0
            else:
                screenshotHoldStart = 0
        else:
            screenshotHoldStart = 0

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # TEXT INSIDE PINK BOX
    h, w, _ = img.shape

    cv2.putText(
    img,
    f"FPS: {int(fps)}",
    (w - 220, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (255, 0, 0),
    2
    )

    cv2.putText(
    img,
    f"ACTION: {actionText}",
    (w - 220, 70),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 255, 0),
    2
    )


    # SCREENSHOT CONFIRMATION
    if showScreenshotMsg > 0:
        cv2.putText(img, "SCREENSHOT SAVED",
                    (frameR + 5, frameR + 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        showScreenshotMsg -= 1

    img = draw_instructions(img)
    
    '''img_resized = cv2.resize(
    img,
    (displayW, displayH),
    interpolation=cv2.INTER_LINEAR
    )
    cv2.imshow("AI Virtual Mouse", img_resized)'''
    cv2.imshow("AI Virtual Mouse", img)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

