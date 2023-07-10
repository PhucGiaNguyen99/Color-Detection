import pandas as pd
import cv2

# Name constants for the color values
imageUrl = 'image01.jpg'
red_value = 0
green_value = 0
blue_value = 0
x_pos = 0
y_pos = 0
clicked = False

colors_name_data_frame = pd.read_csv('wikipedia_color_names.csv')

# get the data frame part of names and color values
colors_name_data_frame.drop(colors_name_data_frame.iloc[:, 5:8], inplace=True, axis=1)
colors_name_data_frame.rename(
    columns={'Hex (24 bit)': 'Hex', 'Red (8 bit)': 'Red', 'Green (8 bit)': 'Green', 'Blue (8 bit)': 'Blue'},
    inplace=True)
image = cv2.imread(imageUrl)


# Find the color with the smallest difference
def getColorName(red, green, blue):
    minimum_value = 10000
    for i in range(len(colors_name_data_frame)):
        rgb_value = abs(red - int(colors_name_data_frame.loc[i, 'Red'])) + abs(
            green - int(colors_name_data_frame.loc[i, "Green"])) + abs(
            blue - int(colors_name_data_frame.loc[i, "Blue"]))
        if rgb_value <= minimum_value:
            minimum_value = rgb_value
            colors_name = colors_name_data_frame.loc[i, "Name"]
    return colors_name


def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global blue_value, green_value, red_value, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        blue_value, green_value, red_value = image[y_pos, x_pos]
        blue_value = int(blue_value)
        green_value = int(green_value)
        red_value = int(red_value)


if __name__ == '__main__':
    cv2.namedWindow("Color Name")
    cv2.setMouseCallback('Color Name', draw_function)

    while (1):
        if (clicked):
            cv2.rectangle(image, (20, 20), (950, 60), (blue_value, green_value, red_value), -1)
            color_name = 'Selected color name is: ' + getColorName(red_value, green_value, blue_value)
            cv2.putText(image, color_name, (50, 50), 2, 0.75, (255, 255, 255), 1, cv2.FONT_ITALIC)
            minimumValue = abs(red_value + green_value + blue_value)
            if (minimumValue >= 600):
                cv2.putText(image, color_name, (50, 50), 2, 0.75, (0, 0, 0), 1, cv2.FONT_ITALIC)
            clicked = False
        cv2.imshow("Color Name",image)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


