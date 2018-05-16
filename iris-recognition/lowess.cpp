#include <iostream>
#include <string>
// #include <opencv2/highgui.hpp>
// #include <opencv2/imgproc.hpp>
#include <dirent.h>
#include <unistd.h>
#include <sys/types.h>
#include <iomanip>

std::vector<int> flWindow(std::vector<int>, int);
std::vector<int> scaleVector(std::vector<int>, int);
int plot(std::vector<int>, std::vector<int>);
int plotVectorToImg(cv::Mat, std::vector<int>, int, int, cv::Vec3b);

int main(int argc, char const *argv[]) {
  std::vector<int> v = {1,5,3,6,9,8,5,6,8,9,0};
}


// plot will make adjustments on vectors and call plot function to write pixels to image
// just graphical representation
int plot(std::vector<int> V1, std::vector<int> V2) {
  if (V1.size() != V2.size()) {
    std::cout << "scale of vectors isn't same" << std::endl;
    return -1;
  }
  // get max vecrot size
  int maxSize = V1.size();

  int scale = maxSize / 1000;
  V1 = scaleVector(V1, scale);
  V2 = scaleVector(V2, scale);
  int size = V1.size();

  // init parameters of plot
  int x_offset = 50, y_offset = 50;
  int height = 500, width = size + y_offset + 20;
  cv::Vec3b blue = {255, 0, 0}, green = {0, 255, 0}, red = {0, 0, 255}, black = {0, 0, 0};

  // create image
  cv::Mat plot(height, width, CV_8UC3, cv::Scalar(255, 255, 255));

  // vertical border
  for (int j=0; j<height; j++) {
    plot.at<cv::Vec3b>(cv::Point(y_offset,j)) = black;
  }
  // horizontal border
  for (int i=0; i<width; i++) {
    plot.at<cv::Vec3b>(cv::Point(i,height-x_offset)) = black;
  }

  // plot each vector into the image
  plotVectorToImg(plot, V1, x_offset, y_offset, blue);
  plotVectorToImg(plot, V2, x_offset, y_offset, red);

  // display image
  cv::imshow("plot", plot);
  cv::waitKey(0);
}

// plotVectorToImg will take image and write pixels to image (plot)
int plotVectorToImg(cv::Mat plot, std::vector<int> v, int x_offset, int y_offset, cv::Vec3b color) {

  // loop over vector and paint pixels ()
  for (int i=0; i<v.size(); i++) {
    plot.at<cv::Vec3b>(plot.rows-v[i]-y_offset, i+x_offset) = color;
    // for better visualization of plots
    plot.at<cv::Vec3b>(plot.rows-v[i]-y_offset-1, i+x_offset) = color;
  }
  return 1;
}

// flWindow will smooth data by given window size
std::vector<int> flWindow(std::vector<int> V, int window) {
  std::vector<int> NV;
  for (int i=0; i<V.size()-window; i++) {
    int S = 0;
    for (int j=i; j<i+window; j++) {
      S += V[j];
    }
    NV.push_back(S/window);
  }
  return NV;
};

// scale down stands for how mych should vector scale, 1 = same, 2 = 1/2, 3 = 1/3 ...
std::vector<int> scaleVector(std::vector<int> V, int scaleDown) {
  std::vector<int> NV;
  for (int i=0; i<V.size()-scaleDown; i=i+scaleDown) {
    int S = 0;
    for (int j=i; j<i+scaleDown; j++) {
      S += V[j];
    }
    NV.push_back(S/scaleDown);
  }
  return NV;

}
