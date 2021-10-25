import cv2

def reproduce_example_6(image, template):
    result0 = cv2.matchTemplate(image[:,:,0], template[:,:,0],
        cv2.TM_CCOEFF_NORMED)
    result1 = cv2.matchTemplate(image[:,:,1], template[:,:,1],
        cv2.TM_CCOEFF_NORMED)
    result2 = cv2.matchTemplate(image[:,:,2], template[:,:,2],
    cv2.TM_CCOEFF_NORMED) 

    (minVal, maxVal, minLoc, maxLoc1) = cv2.minMaxLoc(result0)
    (minVal, maxVal, minLoc, maxLoc2) = cv2.minMaxLoc(result1)
    (minVal, maxVal, minLoc, maxLoc3) = cv2.minMaxLoc(result2)

    (startX1, startY1) = (maxLoc1)
    (startX2, startY2) = (maxLoc2)
    (startX3, startY3) = (maxLoc3)
    (startX, startY) = (0,0)
    if result0[startX1,startY1] > result1[startX2, startY2] and result0[startX1,startY1] > result2[startX3,startY3]:
        (startX, startY) = (maxLoc1)
    elif result1[startX2, startY2] > result0[startX1,startY1] and result1[startX2, startY2] > result2[startX3,startY3]:
        (startX, startY) = (maxLoc2)
    elif result2[startX3,startY3] > result0[startX1,startY1] and result2[startX3,startY3] > result1[startX2, startY2]:
        (startX, startY) = (maxLoc3)

    endX = startX + template.shape[1]
    endY = startY + template.shape[0]
    cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 0), 3)

    cv2.imshow("Output", image)
    cv2.waitKey(0)