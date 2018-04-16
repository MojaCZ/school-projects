// g++ iris.cpp -o iris -std=c++11 `pkg-config --cflags --libs opencv`
#include <iostream>
#include <opencv2/highgui.hpp>

int main(int argc, char const *argv[]) {
  cv::Mat image;

  // load image
  image = cv::imread("irises_MICHE_iPhone5_norm/001_IP5_IN_F_RI_01_1.iris.norm.png");
  if (! image.data) {
    std::cout << "Could not open or find image" << std::endl;
    return -1;
  }

  // set variables
  int width  = image.cols;
  int height = image.rows;
  std::cout << "width: " << width << std::endl;
  std::cout << "height: " << height << std::endl;

  std::cout << image.at<cv::Vec3b>(10,10) << std::endl;

  cv::namedWindow("Display window", cv::WINDOW_AUTOSIZE);
  cv::imshow("Display window", image);

  cv::waitKey(0);
  return 0;
}
