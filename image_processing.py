import abc
import cv2

class ImageProcessor:
  
    @abc.abstractmethod
    def CvtColor(self, src, roi):
        pass
    
    @abc.abstractmethod
    def Filter(self, src, roi, size):
        pass
    
    @abc.abstractmethod
    def DetectEdges(self, src, roi, filter_size, low_threshold, ratio, kernel_size):
        pass
    
    @abc.abstractmethod
    def Pixelize(self, src, roi, divs):
        pass


class ImageProcessorImpl(ImageProcessor):
    
    def CvtColor(self, src, roi):
        src_copy = src
        src_copy_roi = src_copy[roi[1]:roi[3], roi[0]:roi[2], 0:3]
        dst_gray_roi = cv2.cvtColor(src_copy_roi, cv2.COLOR_BGR2GRAY)
        dst_roi=cv2.merge([dst_gray_roi, dst_gray_roi, dst_gray_roi])
        src_copy[roi[1]:roi[3], roi[0]:roi[2],0:3] = dst_roi
        return src_copy

    def Filter(self, src, roi, size):
        src_copy = src
        src_copy_roi = src_copy[roi[1]:roi[3], roi[0]:roi[2], 0:3]
        src_blur_roi = cv2.medianBlur(src_copy_roi, size)
        src_copy[roi[1]:roi[3], roi[0]:roi[2], 0:3] = src_blur_roi
        return src_copy

    def DetectEdges(self, src, roi, filter_size, low_threshold, ratio, kernel_size):
        src_copy = src
        src_roi = src_copy[roi[1]:roi[3], roi[0]:roi[2], 0:3]
        src_gray_roi = cv2.cvtColor(src_roi, cv2.COLOR_RGB2GRAY)
        gray_blurred = cv2.medianBlur(src_gray_roi, filter_size)
        detected_edges = cv2.Canny(gray_blurred, low_threshold, ratio, kernel_size)
        dst_roi = cv2.merge([detected_edges, detected_edges, detected_edges])
        dst = src
        dst[roi[1]:roi[3], roi[0]:roi[2], 0:3] = dst_roi
        return dst

    def Pixelize(self, src, roi, divs):
        src_copy = src
        block_size_x = (roi[2] - roi[0]) // divs
        block_size_y = (roi[3] - roi[1]) // divs
        for i in range (1, divs + 1) :
            for j in range (1, divs + 1):
                src_copy_roi = src_copy[roi[1] + block_size_y * (j-1):roi[1] + block_size_y * j,
                                        roi[0] + block_size_x * (i-1):roi[0] + block_size_x * i,0:3]
                src_blur_roi = cv2.medianBlur(src_copy_roi, 11)
                src_copy[roi[1] + block_size_y * (j-1):roi[1] + block_size_y * j,
                         roi[0] + block_size_x * (i-1):roi[0] + block_size_x * i,0:3] = src_blur_roi
        return src_copy
