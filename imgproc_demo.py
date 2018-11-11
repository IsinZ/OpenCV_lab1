import argparse
import cv2
import image_processing

class MouseCallbackState:
    def __init__(self, is_selection_started = 0, is_selection_finished = 0, point_first = [0,0], point_second = [0,0]):
        self.is_selection_started = is_selection_started
        self.is_selection_finished = is_selection_finished
        self.point_first = point_first
        self.point_second = point_second
     
def OnMouse(event, x, y, flag, param):
    if event==1 and not param.point_first[0] and not param.point_first[1]:  
                param.is_selection_started = 1
                param.is_selection_finished = 0
                param.point_first[0] = x
                param.point_first[1] = y
    elif event==4 and not param.point_second[0] and not param.point_second[1]: 
                param.is_selection_started=0
                param.is_selection_finished=1
                param.point_second[0]=x
                param.point_second[1]=y

def build_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--proc', type = str, dest = 'proc', help = 'Filter')
    parser.add_argument('-i', '--im_dir', type = str, dest = 'image', help = 'Image to process')
    args = parser.parse_args()
    return args
                
if __name__ == '__main__':
    args=build_argparse()
    proc = args.proc
    p = MouseCallbackState()
    obj = image_processing.ImageProcessorImpl()
    img = cv2.imread(args.image)
    cv2.imshow("Original", img)
    cv2.setMouseCallback("Original", OnMouse, p)
    k = cv2.waitKey(0)
    if k==32:
        roi = [p.point_first[0], p.point_first[1], p.point_second[0], p.point_second[1]]
        if proc == 'gray':
            dst = obj.CvtColor(img, roi)
        elif proc == 'median':
            dst = obj.Filter(img, roi, 7)
        elif proc == 'edges':
            dst = obj.DetectEdges(img, roi, 1, 50, 4, 1)
        elif proc == 'pixelize':
            dst = obj.Pixelize(img, roi, 5) 
    cv2.imshow("Result", dst) 
    cv2.waitKey()
        