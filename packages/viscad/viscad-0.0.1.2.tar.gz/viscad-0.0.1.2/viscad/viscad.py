import numpy as np
import cv2


class Viscad:
    @classmethod
    def image_true_area(cls, src: np.ndarray) -> int:
        """
        Counts non zero pixels on a binary image
        :param src:
        :return:
        """
        return np.count_nonzero(src)

    @classmethod
    def extract_image(cls, src: np.ndarray, box) -> np.ndarray:
        """
        Extracts subimage from image
        :param src: Original image
        :param box: X, Y, width, height
        :return: Cut image
        """
        return src[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]

    @classmethod
    def resize_image(cls, src: np.ndarray, size: tuple) -> np.ndarray:
        """
        Resizes image
        :param src: Original image
        :param size: Width, height
        :return: Resized image
        """
        return cv2.resize(src, size)

    @classmethod
    def negate_image(cls, src: np.ndarray) -> np.ndarray:
        """
        Negates binary image
        :param src: Original image
        :return: Negated image
        """
        return cv2.bitwise_not(src)

    @classmethod
    def binary_and(cls, image_1: np.ndarray, image_2: np.ndarray) -> np.ndarray:
        """
        Binary And operator for images
        :param image_1: First image
        :param image_2: Second image
        :return: Binary result
        """
        return cv2.bitwise_and(image_1, image_2)

    @classmethod
    def binary_and_with_mask(cls, image_1: np.ndarray, image_2: np.ndarray, mask) -> np.ndarray:
        """
        Binary And operator for images with mask
        :param image_1: First image
        :param image_2: Second image
        :param mask: Mask (read opencv docs, i don't remember anything)
        :return: Binary result
        """
        return cv2.bitwise_and(image_1, image_2, mask=mask)

    @classmethod
    def binary_or(cls, image_1: np.ndarray, image_2: np.ndarray) -> np.ndarray:
        """
        Binary Or operator for images
        :param image_1: First image
        :param image_2: Second image
        :return: Binary result
        """
        return cv2.bitwise_or(image_1, image_2)

    @classmethod
    def threshold(cls, src: np.ndarray, blue: tuple, green: tuple, red: tuple) -> np.ndarray:
        """
        Threshold for 3 channel image
        :param src: Original image
        :param blue: First thresholds
        :param green: Second thresholds
        :param red: Third thresholds
        :return: Thresholded image
        """
        return cv2.inRange(src, (blue[0], green[0], red[0]), (blue[1], green[1], red[1]))

    @classmethod
    def threshold_gray(cls, src: np.ndarray, rang: tuple) -> np.ndarray:
        """
        Threshold for 1 channel image
        :param src: Original image
        :param rang: Thresholds
        :return: Thresholded image
        """
        return cv2.inRange(src, rang[0], rang[1])

    @classmethod
    def reject_borders(cls, src: np.ndarray) -> np.ndarray:
        """
        Rejects non zero pixels that touch image borders
        :param src: Original image
        :return: Image with rejected borders
        """
        out_image: np.ndarray = src.copy()
        h, w = src.shape[:2]
        for row in range(h):
            if out_image[row, 0] == 255:
                cv2.floodFill(out_image, None, (0, row), 0)
            if out_image[row, w - 1] == 255:
                cv2.floodFill(out_image, None, (w - 1, row), 0)
        for col in range(w):
            if out_image[0, col] == 255:
                cv2.floodFill(out_image, None, (col, 0), 0)
            if out_image[h - 1, col] == 255:
                cv2.floodFill(out_image, None, (col, h - 1), 0)
        return out_image

    @classmethod
    def reject_borders_fast(cls, src: np.ndarray, step: int = 1) -> np.ndarray:
        """
        Rejects non zero pixels that touch image borders with selected step
        :param src: Original image
        :param step: Rejection step
        :return: Image with rejected borders
        """
        out_image: np.ndarray = src.copy()
        h, w = src.shape[:2]
        for row in range(0, h, step):
            if out_image[row, 0] == 255:
                cv2.floodFill(out_image, None, (0, row), 0)
            if out_image[row, w - 1] == 255:
                cv2.floodFill(out_image, None, (w - 1, row), 0)
        for col in range(0, w, step):
            if out_image[0, col] == 255:
                cv2.floodFill(out_image, None, (col, 0), 0)
            if out_image[h - 1, col] == 255:
                cv2.floodFill(out_image, None, (col, h - 1), 0)
        return out_image

    @classmethod
    def particle_filter(cls, src: np.ndarray, power) -> np.ndarray:
        """
        Particle filter for binary image
        :param src: Original image
        :param power: Filtering power
        :return: Filtered image
        """
        # Abdrakov's particle filter
        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(src, connectivity=8)
        sizes = stats[1:, -1]
        nb_components = nb_components - 1

        min_size = power

        img2 = np.zeros(output.shape, dtype=np.uint8)
        for i in range(0, nb_components):
            if sizes[i] >= min_size:
                img_to_compare = cls.threshold_gray(output, (i + 1, i + 1))
                img2 = cls.binary_or(img2, img_to_compare)

        img2 = img2.astype(np.uint8)
        return img2

    @classmethod
    def particle_analysis(cls, src: np.ndarray) -> tuple:
        """
        Particle analysis, like in LabVIEW (this function should be rewritten)
        :param src: Original image
        :return: Information about binary image
        """
        dst = src.copy()
        contours, hierarchy = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        arr_of_box = list()
        arr_of_contour_sizes = list()
        arr_of_contour_areas = list()
        for i in range(0, len(contours)):
            cnt = contours[i]
            x, y, w, h = cv2.boundingRect(cnt)
            arr_of_contour_sizes.append(w * h)
            arr_of_contour_areas.append(cv2.contourArea(cnt))
            arr_of_box.append((x, y, w, h))
            cv2.rectangle(dst, (x, y), (x + w, y + h), (255, 255, 255), 1)
        # sorting by sizes
        arr_of_box = [i for _, i in sorted(zip(arr_of_contour_areas, arr_of_box))]
        arr_of_box.reverse()
        arr_of_contour_sizes = sorted(arr_of_contour_sizes)
        arr_of_contour_sizes.reverse()
        arr_of_contour_areas = sorted(arr_of_contour_areas)
        arr_of_contour_areas.reverse()
        return dst, arr_of_box, arr_of_contour_sizes, arr_of_contour_areas

    @classmethod
    def remake_contour(cls, cont, k, draw_on_image=None):
        """
        Remakes contour (i don't remember, read about this in opencv)
        :param cont: Contour, that you want to remake
        :param k: Coefficient for epsilon
        :param draw_on_image: If you want to draw result contour on an image
        :return: Remade contour
        """
        epsilon = k * cv2.arcLength(cont, True)
        new_cnt = cv2.approxPolyDP(cont, epsilon, True)

        if draw_on_image is not None:
            cv2.drawContours(draw_on_image, [new_cnt], 0, (0, 0, 255), 3)
        return new_cnt

    @classmethod
    def auto_brightness(cls, src: np.ndarray, cut: np.ndarray, value: int, bgr_out: bool = True) -> np.ndarray:
        """
        Auto brightness for an image, using another one
        :param src: Original image
        :param cut: Monotone image, from which it will take V (from HSV color space)
        :param value: Needed V
        :param bgr_out: If True - BGR image will be returned, else - HSV
        :return: Lightened or darkened image
        """
        hsv_cut = cv2.cvtColor(cut, cv2.COLOR_BGR2HSV)
        _, _, v = cv2.split(hsv_cut)
        v_mean = v.sum(axis=0).sum(axis=0) / v.size
        mul_k = value / v_mean

        img_hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
        img_hsv[:, :, 2] = cv2.multiply(img_hsv[:, :, 2], mul_k)
        if bgr_out:
            return cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        else:
            return img_hsv

    @classmethod
    def auto_color(cls, src: np.ndarray, cut: np.ndarray, value: tuple, bgr_out: bool = True) -> np.ndarray:
        """
        Auto color for an image, using another one
        :param src: Original image
        :param cut: Monotone image, from which it will take H, S, V (from HSV color space)
        :param value: Needed H, S, V
        :param bgr_out: If True - BGR image will be returned, else - HSV
        :return: Image with changed color
        """
        hsv_cut = cv2.cvtColor(cut, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_cut)
        h_mean = h.sum(axis=0).sum(axis=0) / h.size
        s_mean = s.sum(axis=0).sum(axis=0) / s.size
        v_mean = v.sum(axis=0).sum(axis=0) / v.size
        mul_k_h = value[0] / h_mean
        mul_k_s = value[1] / s_mean
        mul_k_v = value[2] / v_mean

        img_hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
        img_hsv[:, :, 0] = cv2.multiply(img_hsv[:, :, 0], mul_k_h)
        img_hsv[:, :, 1] = cv2.multiply(img_hsv[:, :, 1], mul_k_s)
        img_hsv[:, :, 2] = cv2.multiply(img_hsv[:, :, 2], mul_k_v)
        if bgr_out:
            return cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        else:
            return img_hsv

    @classmethod
    def center_of_mass(cls, src: np.ndarray) -> tuple:
        """
        Center of mass of binary image
        :param src: Original image
        :return: Tuple of center of mass
        """
        mass_x, mass_y = np.where(src >= 255)
        cent_x = np.average(mass_x)
        cent_y = np.average(mass_y)
        return cent_x, cent_y

    @classmethod
    def fill_holes(cls, src: np.ndarray) -> np.ndarray:
        """
        Fills holes on a binary image
        :param src: Original image
        :return: Image with filled holes
        """
        contour, hier = cv2.findContours(src, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contour:
            cv2.drawContours(src, [cnt], 0, 255, -1)
        return src

    @classmethod
    def rotate_image_save_shape(cls, src: np.ndarray, angle) -> np.ndarray:
        """
        Rotate image and save its shape
        :param src: Original image
        :param angle: Angle you want to rotate an image
        :return: Rotated image
        """
        image_center = tuple(np.array(src.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(src, rot_mat, src.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result

    @classmethod
    def rotate_image(cls, src, angle):
        """
        Rotate image without saving its shape
        :param src: Original image
        :param angle: Angle you want to rotate an image
        :return: Rotated image
        """
        # grab the dimensions of the image and then determine the
        # center
        h, w = src.shape[:2]
        cx, cy = (w // 2, h // 2)
        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        m = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
        cos = np.abs(m[0, 0])
        sin = np.abs(m[0, 1])
        # compute the new bounding dimensions of the image
        nw = int((h * sin) + (w * cos))
        nh = int((h * cos) + (w * sin))
        # adjust the rotation matrix to take into account translation
        m[0, 2] += (nw / 2) - cx
        m[1, 2] += (nh / 2) - cy
        # perform the actual rotation and return the image
        return cv2.warpAffine(src, m, (nw, nh))
