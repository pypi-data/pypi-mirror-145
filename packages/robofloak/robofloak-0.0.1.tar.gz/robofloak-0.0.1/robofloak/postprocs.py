import numpy as np

# Malisiewicz et al.
def non_max_suppression_fast(boxes, overlapThresh):
	# if there are no boxes, return an empty list
	if len(boxes) == 0:
		return []
	# if the bounding boxes integers, convert them to floats --
	# this is important since we'll be doing a bunch of divisions
	if boxes.dtype.kind == "i":
		boxes = boxes.astype("float")
	# initialize the list of picked indexes
	pick = []
	# grab the coordinates of the bounding boxes
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]
	# compute the area of the bounding boxes and sort the bounding
	# boxes by the bottom-right y-coordinate of the bounding box
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(y2)
	# keep looping while some indexes still remain in the indexes
	# list
	while len(idxs) > 0:
		# grab the last index in the indexes list and add the
		# index value to the list of picked indexes
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)
		# find the largest (x, y) coordinates for the start of
		# the bounding box and the smallest (x, y) coordinates
		# for the end of the bounding box
		xx1 = np.maximum(x1[i], x1[idxs[:last]])
		yy1 = np.maximum(y1[i], y1[idxs[:last]])
		xx2 = np.minimum(x2[i], x2[idxs[:last]])
		yy2 = np.minimum(y2[i], y2[idxs[:last]])
		# compute the width and height of the bounding box
		w = np.maximum(0, xx2 - xx1 + 1)
		h = np.maximum(0, yy2 - yy1 + 1)
		# compute the ratio of overlap
		overlap = (w * h) / area[idxs[:last]]
		# delete all indexes from the index list that have
		idxs = np.delete(idxs, np.concatenate(([last],
			np.where(overlap > overlapThresh)[0])))
	# return only the bounding boxes that were picked using the
	# integer data type
	return boxes[pick].astype("float")


def w_np_non_max_suppression(np_prediction, num_classes, conf_thres=0.5, nms_thres=0.4):
    np_box_corner = np.zeros(np_prediction.shape)
    np_box_corner[:, :, 0] = np_prediction[:, :, 0] - np_prediction[:, :, 2] / 2
    np_box_corner[:, :, 1] = np_prediction[:, :, 1] - np_prediction[:, :, 3] / 2
    np_box_corner[:, :, 2] = np_prediction[:, :, 0] + np_prediction[:, :, 2] / 2
    np_box_corner[:, :, 3] = np_prediction[:, :, 1] + np_prediction[:, :, 3] / 2
    # [x middle, y middle, width, height] , box_confidence, class confidences]

    #print(np_prediction[0][0])
    np_prediction[:, :, :4] = np_box_corner[:, :, :4]
    batch_predictions = []
    for np_image_i, np_image_pred in enumerate(np_prediction):
        filtered_predictions = []
        np_conf_mask = (np_image_pred[:, 4] >= conf_thres).squeeze()

        np_image_pred = np_image_pred[np_conf_mask]
        if np_image_pred.shape[0] == 0:
            # no predictions are to be made
            continue
        np_class_conf = np.max(np_image_pred[:, 5:5 + num_classes], 1)
        np_class_pred = np.argmax(np_image_pred[:, 5:5 + num_classes], 1)
        np_class_conf = np.expand_dims(np_class_conf, axis=1)
        np_class_pred = np.expand_dims(np_class_pred, axis=1)
        # 获得的内容为(x1, y1, x2, y2, obj_conf, class_conf, class_pred)
        np_detections = np.append(np.append(np_image_pred[:, :5], np_class_conf, axis =1), np_class_pred, axis = 1)

        np_unique_labels = np.unique(np_detections[:, -1])

        for c in np_unique_labels:
            np_detections_class = np_detections[np_detections[:, -1] == c]
            np_detections_class = sorted(np_detections_class, key=lambda row: row[4], reverse=True)
            np_max_detections = []

            filtered_predictions.extend(non_max_suppression_fast(np.array(np_detections_class), nms_thres))
        batch_predictions.append(filtered_predictions)
    return batch_predictions

def scale_coords(img1_shape, coords, img0_shape, ratio_pad=None):
    # Rescale coords (xyxy) from img1_shape to img0_shape
    if ratio_pad is None:  # calculate from img0_shape
        gain = max(img1_shape) / max(img0_shape)  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    # x and y padding
    coords[0] -= pad[0]
    coords[2] -= pad[0]
    coords[1] -= pad[1]
    coords[3] -= pad[1]

    coords = [coord / gain for coord in coords]

    coords[0] = int(round(np.clip(coords[0], a_min = 0, a_max=img0_shape[1])))
    coords[2] = int(round(np.clip(coords[2], a_min = 0, a_max=img0_shape[1])))
    coords[1] = int(round(np.clip(coords[1], a_min = 0, a_max=img0_shape[0])))
    coords[3] = int(round(np.clip(coords[3], a_min = 0, a_max=img0_shape[0])))

    return coords

def process_detections(detections, input_dims, class_filter=[], class_names=[]):
    w, h = input_dims

    processed_detections = []
    for i, detection in enumerate(detections):

        x1, y1, x2, y2 = int(detection[0]) , int(detection[1]) , int(detection[2]) , int(detection[3])

        coords = scale_coords((input_dims[0],input_dims[1]), [x1,y1,x2,y2], (h,w))
        x1 = coords[0]
        y1 = coords[1]
        x2 = coords[2]
        y2 = coords[3]

        conf = detection[4]

        label_num = detection[-1]

        label = class_names[int(label_num)]
        if label in class_filter:
            processed_detection = [x1,y1,x2,y2,label,conf]
            processed_detections.append(processed_detection)
    return processed_detections