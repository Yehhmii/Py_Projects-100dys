import time, numpy as np, pyautogui
from PIL import ImageGrab

# 1) Let’s calibrate ground‐level under the dino’s feet:
print("Hover over the Dino’s feet (ground level) in 3s…")
time.sleep(3)
gx, gy = pyautogui.position()
print("Ground at:", gx, gy)

# 2) Build a scan‐box that sits *above* that ground by ~10px
#    and only tall enough (~30px) to catch cacti:
BOX = (
    gx + 100,      # left: 100px ahead of the dino
    gy - 70,       # top: 70px above the ground
    gx + 200,      # right: 200px ahead (i.e. 100px wide)
    gy - 40        # bottom: 40px above ground  (i.e. 30px tall)
)
print("Scanning box:", BOX)

# Settings
THRESHOLD_DAY   = 80    # any pixel darker than this is “obstacle” in day
THRESHOLD_NIGHT = 200   # any pixel brighter than this is “obstacle” at night
MIN_PIXELS      = 12    # require at least this many pixels to trigger jump
JUMP_COOLDOWN   = 0.1   # secs between jumps

def is_night():
    # sample sky 50px above top of BOX
    sx = BOX[0] + 50
    sy = BOX[1] - 50
    r,g,b = ImageGrab.grab((sx,sy,sx+1,sy+1)).getpixel((0,0))
    return (r+g+b)/3 < 128

def obstacle_ahead(night):
    arr = np.array(ImageGrab.grab(BOX).convert('L'))
    if not night:
        count = (arr < THRESHOLD_DAY).sum()
    else:
        count = (arr > THRESHOLD_NIGHT).sum()
    # DEBUG: uncomment to see counts
    # print("dark count:", count)
    return count >= MIN_PIXELS

# initial setup
print("Get ready… bot starts in 3s.")
time.sleep(3)

night = is_night()
last_mode_check = time.time()
last_jump = 0

try:
    while True:
        now = time.time()
        # re-detect day/night every 2 s
        if now - last_mode_check > 2:
            night = is_night()
            last_mode_check = now

        # if cooldown passed and real obstacle present → jump
        if now - last_jump > JUMP_COOLDOWN and obstacle_ahead(night):
            pyautogui.press('space')
            last_jump = now

        time.sleep(0.005)

except KeyboardInterrupt:
    print("Bot stopped.")
