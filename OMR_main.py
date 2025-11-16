import cv2
import numpy as np
import utils

widthImg=700
heightImg=700
path="1.jpg"
answers=[1,2,0,1,4] #the correct answers to compare with students answers for grading
#-----------------
#webcam
camerano=0
webcamfeed=True
cap=cv2.VideoCapture(camerano)
cap.set(10,150)

while True:
    if webcamfeed: success,img=cap.read()
    else: img=cv2.imread(path)
 
    #resize image
    img=cv2.resize(img,(widthImg,heightImg))
    imgContours=img.copy()
    imgBiggestcontours=img.copy()

    #preprocess image
    #1)turn grayscale
    imggray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgblur=cv2.GaussianBlur(imggray,(5,5),1)
    #2) detect edges
    imgCanny=cv2.Canny(imgblur,10,50)
    
    try:
        #find contours
        countours,hierarchy=cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(imgContours,countours, -1,(0,255,0) ,10)
        #find rectangles
        rectCon=utils.rectContour(countours)
        #this has all points of bggest contour we want 4 corner
        biggestContour=utils.getCornerPoints(rectCon[0])
        gradepoints=utils.getCornerPoints(rectCon[1]) #the grade section rectangle
        #print(biggestContour)

        #imgbiggestcontour image has corner points of biggest rec and the grading rectangle highlighted
        if biggestContour.size !=0 and gradepoints.size!=0:
            
            cv2.drawContours(imgBiggestcontours,biggestContour,-1,(0,255,0),20)
            cv2.drawContours(imgBiggestcontours,gradepoints,-1,(255,0,0),20) 

            biggestContour=utils.reorder(biggestContour)
            gradepoints=utils.reorder(gradepoints)
            
            #warping image to get birds eye (imgwarped) 
            pt1=np.float32(biggestContour)
            pt2=np.float32([[0,0],[widthImg,0],[0,heightImg],[widthImg,heightImg]])
            transformationmatrix=cv2.getPerspectiveTransform(pt1,pt2)
            imgwarped=cv2.warpPerspective(img,transformationmatrix,(widthImg,heightImg))

            pt1g=np.float32(gradepoints)
            pt2g=np.float32([[0,0],[400,0],[0,150],[400,150]])
            transformationmatrixg=cv2.getPerspectiveTransform(pt1g,pt2g)
            imgwarpedg=cv2.warpPerspective(img,transformationmatrixg,(400,150)) 
            #cv2.imshow("grade",imgwarpedg)

            #apply threshold to find marked bubbles in imgwarped
            imgwarpgray=cv2.cvtColor(imgwarped,cv2.COLOR_BGR2GRAY)
            imgThreshold=cv2.threshold(imgwarpgray,200,255,cv2.THRESH_BINARY_INV)[1]
            

            #spllit the image into 25 boxes,each box has 1 circle
            boxes=utils.splitBoxes(imgThreshold)
            mypixelval=np.zeros((5,5))
            countc=0
            countr=0
            for image in boxes:
                totalPixels=cv2.countNonZero(image)
                mypixelval[countr][countc]=totalPixels
                countc+=1
                if countc==5:
                    countr+=1
                    countc=0
            
            #now from mypixelval get the index with highest pixel value in each row(for each question) and mark that in 1's and 0's
            myindex=[]
            for x in range(0,5):
                arr=mypixelval[x]
                myindexval=np.where(arr==np.amax(arr)) #myindex=[1,2,0,0,4]
                myindex.append(myindexval[0][0])
            
            #now compare ans list and the myindex list find garade
            grading=[]
            totalquestion=5
            for i in range(0,5):
                if answers[i]==myindex[i]:
                    grading.append(1)
                else:
                    grading.append(0)
            
            grade=(sum(grading)/totalquestion)*100
            print("FINAL GRADE: ",grade)

            #Diaplay the grade and answers in the question sheet
            imgresult=imgwarped.copy()
            utils.showAnswers(imgresult,myindex,grading,answers,5,5)
            imgdrawing=np.zeros_like(imgwarped)
            utils.showAnswers(imgdrawing,myindex,grading,answers,5,5)
            invmatrix=cv2.getPerspectiveTransform(pt2,pt1)
            imginvwarp=cv2.warpPerspective(imgdrawing,invmatrix,(widthImg,heightImg))
            
            #final combination
            imgfinal=img.copy()
            imgfinal=cv2.addWeighted(imgfinal,1,imginvwarp,1,0)


            #now add grade
            imagerawgrade=np.zeros_like(imgwarpedg)
            cv2.putText(imagerawgrade,str(int(grade))+"%",(70,100),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),6)
            invtransformationmatrixg=cv2.getPerspectiveTransform(pt2g,pt1g)
            invimgwarpedg=cv2.warpPerspective(imagerawgrade,invtransformationmatrixg,(widthImg,heightImg)) 
            imgfinal=cv2.addWeighted(imgfinal,1,invimgwarpedg,1,0)
        #printstackimage
        imgBlank=np.zeros_like(img)
        imageArray=([img,imggray,imgblur,imgCanny],
                    [imgContours,imgBiggestcontours,imgwarped,imgThreshold],
                    [imgresult,imgdrawing,imginvwarp,imgfinal]
                    )
    except:
        imgBlank=np.zeros_like(img)
        imageArray=([img,imggray,imgblur,imgCanny],
                    [imgBlank,imgBlank,imgBlank,imgBlank],
                    [imgBlank,imgBlank,imgBlank,imgBlank]
                    )
    lables=[["Orignal Image","gray","blur","Canny edge"],
            ["Image Contours","Largest contours","Image warped","Threshold"],
            ["Results","Raw drawing","inverse warp","Final grade"]]
    imgstack=utils.stackImages(imageArray,0.3)
    cv2.imshow("Original",imgstack)

    if cv2.waitKey(1) & 0xFF== ord('s'):
        cv2.imwrite("Scanned/myImage"+str(count)+".jpg",imgfinal)
        cv2.rectangle(imgstack, ((int(imgstack.shape[1] / 2) - 230), int(imgstack.shape[0] / 2) + 50),
                      (1100, 350), (0, 255, 0), cv2.FILLED)
        cv2.putText(imgstack, "Scan Saved", (int(imgstack.shape[1] / 2) - 200, int(imgstack.shape[0] / 2)),
                    cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)
        cv2.imshow('Result', imgstack)
        cv2.waitKey(300)
        count += 1
