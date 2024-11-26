import cv2
import numpy as np

# Parameters for drawing
drawing = False
ix, iy = -1, -1
annotations = []

# Mouse callback function to draw contours
def draw_contour(event, x, y, flags, param):
    global ix, iy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        annotations.append([(x, y)])  # Start a new contour

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            annotations[-1].append((x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        annotations[-1].append((x, y))  # Close the contour

# Function to display the image and collect annotations
def segment_image(image_path):
    global annotations
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found!")
        return

    annotated_image = image.copy()
    cv2.namedWindow("Image Segmentation")
    cv2.setMouseCallback("Image Segmentation", draw_contour)

    while True:
        temp_image = annotated_image.copy()
        for contour in annotations:
            points = np.array(contour, dtype=np.int32)
            cv2.polylines(temp_image, [points], isClosed=True, color=(0, 255, 0), thickness=2)

        cv2.imshow("Image Segmentation", temp_image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            # Calculate and draw bounding box for each contour
            with open("annotations.txt", "w") as f:
                for contour in annotations:
                    points = np.array(contour, dtype=np.int32)
                    x, y, w, h = cv2.boundingRect(points)
                    cv2.rectangle(temp_image, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw bounding box
                    f.write(f"Contour: {contour}, Bounding Box: (x={x}, y={y}, w={w}, h={h})\n")
                    print(f"Bounding Box: x={x}, y={y}, w={w}, h={h}")
            cv2.imshow("Image Segmentation", temp_image)
            cv2.waitKey(0)
            print("Annotations saved to annotations.txt")
        elif key == ord("c"):
            annotations.clear()
            annotated_image = image.copy()
            print("Annotations cleared")
        elif key == ord("q"):
            break

    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    PathNames = r"C:/Users/cic/Desktop/SW_oop18/dataset"
    segment_image(PathNames + "//000000002473.jpg")
