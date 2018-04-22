// g++ iris.cpp -o iris -std=c++11 `pkg-config --cflags --libs opencv`
#include <iostream>
#include <opencv2/highgui.hpp>

int compare(cv::Mat, cv::Mat, int);

int main(int argc, char const *argv[]) {

  const int WINDOW = 30;

  cv::Mat image1;
  cv::Mat image2;

  // load image
  image1 = cv::imread("irises_MICHE_iPhone5_norm/001_IP5_IN_F_RI_01_1.iris.norm.png");
  if (! image1.data) {
    std::cout << "Could not open or find image1" << std::endl;
    return -1;
  }

  // image2 = cv::imread("irises_MICHE_iPhone5_norm/004_IP5_OU_F_LI_01_1.iris.norm.png");
  image2 = cv::imread("irises_MICHE_iPhone5_norm/001_IP5_IN_F_RI_01_2.iris.norm.png");
  if (! image2.data) {
    std::cout << "Could not open or find image2" << std::endl;
    return -1;
  }

  if (image1.cols != image2.cols || image1.rows != image2.rows) {
    std::cout << "dim of picture 1 is not equal to dim of picture2";
    return -1;
  }

  compare(image1, image2, WINDOW);

  // set variables
  std::cout << "window size: " << WINDOW << std::endl;
  std::cout << "width image1: " << image1.cols << " width image2: " << image2.cols <<  std::endl;
  std::cout << "height image1: " << image1.rows << " height image2: " << image2.rows << std::endl;

  // cv::namedWindow("Display window", cv::WINDOW_AUTOSIZE);
  cv::imshow("image1", image1);
  cv::imshow("image2", image2);

  cv::waitKey(0);
  return 0;
}

int compare(cv::Mat image1, cv::Mat image2, int WINDOW) {

  std::cout << "from function" << std::endl;
  std::cout << "width image1: " << image1.cols << " width image2: " << image2.cols <<  std::endl;
  std::cout << "height image1: " << image1.rows << " height image2: " << image2.rows << std::endl;

  for (int i=0; i<image1.cols-WINDOW; i=i+WINDOW) {
    for (int j=0; j<image1.rows-WINDOW; j=j+WINDOW) {
      int S1 = 0;
      int S2 = 0;
      for (int x=i; x<i+WINDOW; x++) {
        for (int y=j; y<j+WINDOW; y++) {
          cv::Vec3b px1 = image1.at<cv::Vec3b>(y, x);
          cv::Vec3b px2 = image2.at<cv::Vec3b>(y, x);
          S1 += px1[0];
          S2 += px2[0];
        }
      }
      std::cout << i << " " << j << " " << S1 << " " << S2 << std::endl;
    }
    // std::cout << i << std::endl;
    // cv::Vec3b px = image1.at<cv::Vec3b>(5, i);
    // std::cout << px << std::endl;
  }

};
