import os, sys
import cv2
import numpy as np
import moviepy.editor as mp

# 比較用画像
im_blank = np.zeros((360, 640, 3), dtype='uint8')
hist_blank = cv2.calcHist([im_blank], [0], None, [256], [0, 256])

for filename in sys.argv[1:]:

    # 動画読み込み
    cap = cv2.VideoCapture(filename)

    if not cap.isOpened():
        print('Could not open cap', file=sys.stderr)
        sys.exit(1)

    fc = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 比較用画像とほぼ一致する場面の時間を取得
    startfc = 0
    for i in range(0, int(fc)):
        (ok, frame) = cap.read()
        if ok:
            hist = cv2.calcHist([frame], [0], None, [256], [0, 256])
            ret = cv2.compareHist(hist_blank, hist, 0)

            # 完全一致にならないのでヒストグラム化して99.9%一致でOKにする
            if ret > 0.999:
                startfc = i
                #cv2.imwrite('debug.png', frame)
                break

    cap.release()
    cv2.destroyAllWindows()


    # なんか3分27秒くらいだった
    videolength = 207

    # 1.0秒引いてみたらなんかちょうどよかった
    startsec = startfc / fps - 1.0
    if startsec < 0:
        startsec = 0

    # 出力ファイル名
    (fname, ext) = os.path.splitext(filename)
    outfilename = fname + '.colocat' + ext

    # moviepyで出力
    clip_in = mp.VideoFileClip(filename).subclip(startsec, videolength)
    clip_in.write_videofile(outfilename, audio_codec = 'aac')
    clip_in.close()

