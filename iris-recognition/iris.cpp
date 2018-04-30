// g++ iris.cpp -o iris -std=c++11 `pkg-config --cflags --libs opencv`
#include <iostream>
#include <string>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <dirent.h>
#include <unistd.h>
#include <sys/types.h>
#include <iomanip>

int compare(cv::Mat, cv::Mat, int);
std::vector<std::string> loadDir(std::string);
int train(std::vector<std::string>);
int getMax(cv::Mat, cv::Mat, int (&min)[3], int);
int compareImages(std::vector<std::string>);
int compareHistograms(cv::Mat, cv::Mat);
int plot(std::vector<int>, std::vector<int>);
int plotVectorToImg(cv::Mat, std::vector<int>, int, int, cv::Vec3b);

int main(int argc, char const *argv[]) {

  std::vector<std::string> paths;
  paths = loadDir("/irises_MICHE_iPhone5_norm/");
  // compareImages(paths);

  const int WINDOW = 50;

  cv::Mat image1;
  cv::Mat image2;

  // load image
  image1 = cv::imread("irises_MICHE_iPhone5_norm/001_IP5_IN_F_RI_01_1.iris.norm.png");
  if (! image1.data) {
    std::cout << "Could not open or find image1" << std::endl;
    return -1;
  }

  image2 = cv::imread("irises_MICHE_iPhone5_norm/004_IP5_OU_F_LI_01_1.iris.norm.png");
  // image2 = cv::imread("irises_MICHE_iPhone5_norm/001_IP5_IN_F_RI_01_2.iris.norm.png");
  if (! image2.data) {
    std::cout << "Could not open or find image2" << std::endl;
    return -1;
  }

  if (image1.cols != image2.cols || image1.rows != image2.rows) {
    std::cout << "dim of picture 1 is not equal to dim of picture2";
    return -1;
  }
  // compareHistograms(image1, image2);

  std::vector<int> V1, V2;
  for (int i=0; i<image1.cols; i++) {
    int px1 = image1.at<cv::Vec3b>(0, i)[0];
    int px2 = image2.at<cv::Vec3b>(0, i)[0];
    V1.push_back(px1);
    V2.push_back(px2);
  }
  plot(V1, V2);

  // for (int i=0; i<)
  // compare(image1, image2, WINDOW);

  // cv::namedWindow("Display window", cv::WINDOW_AUTOSIZE);
  // cv::imshow("image1", image1);
  // cv::imshow("image2", image2);

  cv::waitKey(0);
  return 0;
}

std::vector<std::string> loadDir(std::string relativePath) {
  // get current working directory and append relative path to files
  char cwd[1024];
  getcwd(cwd, sizeof(cwd)) != NULL;
  std::string imagesDir(cwd);
  imagesDir.append(relativePath);

  // get all fileNames in directory
  std::vector<std::string> paths; // vector of files in directory
  DIR* dirp = opendir(strdup(imagesDir.c_str()));
  struct dirent * dp;
  int i = 0;
  while ((dp = readdir(dirp)) != NULL) {
    if (i>1) {
      paths.push_back(imagesDir + (dp->d_name));
    }
    i++;
  }
  closedir(dirp);
  return paths;
}

int compareImages(std::vector<std::string> paths) {
  // each with each
  for (int i=0; i<paths.size(); i++) {  //paths.size()
    for (int j=i+1; j<paths.size(); j++) {  //paths.size()

      // check just images of one iris
      if ( paths[i].substr(0,paths[i].size()-16) == paths[j].substr(0,paths[j].size()-16) ) {
        continue;
      }
      cv::Mat img1 = cv::imread(paths[i]);
      if (! img1.data) {
        std::cout << "Could not open or find image1" << std::endl;
        return -1;
      }
      cv::Mat img2 = cv::imread(paths[j]);
      if (! img2.data) {
        std::cout << "Could not open or find image2" << std::endl;
        return -1;
      }
      std::cout << paths[i].substr(73, 20)  << " VS " << paths[j].substr(73, 20) << ":   ";
      compareHistograms(img1, img2);
    }
  }
}

// return number
int compareHistograms(cv::Mat img1, cv::Mat img2) {
  cv::Mat hsv_img1; cv::Mat hsv_img2;

  cv::cvtColor( img1, hsv_img1, cv::COLOR_BGR2HSV);
  cv::cvtColor( img2, hsv_img2, cv::COLOR_BGR2HSV);


  int h_bins = 50; int s_bins = 60;
  int histSize[] = { h_bins, s_bins };

  float h_ranges[] = { 0, 180 };
  float s_ranges[] = { 0, 256 };

  const float* ranges[] = { h_ranges, s_ranges };

  int channels[] = { 0, 1 };

  cv::MatND hist_img1;
  cv::MatND hist_img2;

  cv::calcHist( &hsv_img1, 1, channels, cv::Mat(), hist_img1, 2, histSize, ranges, true, false);
  cv::normalize( hist_img1, hist_img1, 0, 1, cv::NORM_MINMAX, -1, cv::Mat());

  cv::calcHist( &hsv_img2, 1, channels, cv::Mat(), hist_img2, 2, histSize, ranges, true, false);
  cv::normalize( hist_img2, hist_img2, 0, 1, cv::NORM_MINMAX, -1, cv::Mat());

  // 0 = correlation, 1 = CHI2, 2 = intersection, 3 = BhattacharyyaD, 4 = synonym
  // M1 closer to 1 - closer pictures
  double M1 = cv::compareHist( hist_img1, hist_img2, 0);
  // M2 smaller - closer
  double M2 = cv::compareHist( hist_img1, hist_img2, 1);
  // M3 bigger - closer
  double M3 = cv::compareHist( hist_img1, hist_img2, 2);
  // M4 smaller - closer
  double M4 = cv::compareHist( hist_img1, hist_img2, 3);
  // M5 smaller - closer
  double M5 = cv::compareHist( hist_img1, hist_img2, 4);

  std::cout << std::setw(8) << M1 << std::setw(10) << M2 << std::setw(10) << M3 << std::setw(10) << M4 << std::setw(10) << M5;
  if (M1 < 0.5) {
    std::cout << "1 ";
  }
  if (M2 > 200) {
    std::cout << "2 ";
  }
  if (M3 < 10) {
    std::cout << "3 ";
  }
  if (M4 > 0.5) {
    std::cout << "4 ";
  }
  if (M5 > 70) {
    std::cout << "5 ";
  }
  std::cout << std::endl;
  return 1;
}

int train(std::vector<std::string> paths) {
  // if I have 815 files in dir, and I want to compare each with each,
  // C(815,2) = (815*814)/(2!) = 331705 of combinations

  int min[3] = {255,255,255}, max[3] = {0, 0, 0};
  // different window

  // each with each
  for (int i=0; i<paths.size(); i++) {  //paths.size()
    for (int j=i+1; j<paths.size(); j++) {  //paths.size()
      cv::Mat img1 = cv::imread(paths[i]);
      cv::Mat img2 = cv::imread(paths[j]);
      getMax(img1, img2, max, 20);
      std::cout << "MAX IS: [" << max[0] << ", " << max[1] << ", " << max[2] << "]" << std::endl;
    }
  }
    // find min max average
}

int getMax(cv::Mat img1, cv::Mat img2, int (&max)[3], int WINDOW) {
  int windowSize = WINDOW * WINDOW;
  for (int j=0; j<img1.cols-WINDOW; j++) {
    for (int i=0; i<img1.rows-WINDOW; i++) {
      int B1=0, G1=0, R1 = 0;
      int B2=0, G2=0, R2 = 0;
      for (int y=j; y<j+WINDOW-1; y++) {
        for (int x=i; x<i+WINDOW-1; x++) {
          cv::Vec3b px1 = img1.at<cv::Vec3b>(x, y);
          cv::Vec3b px2 = img2.at<cv::Vec3b>(x, y);
          B1 += px1[0]; G1 += px1[1]; R1 += px1[2];
          B2 += px2[0]; G2 += px2[1]; R2 += px2[2];
        }
      }

      int B1A = B1/windowSize, G1A = G1/windowSize, R1A = R1/windowSize; // get averageas of image pixel in each color
      int B2A = B2/windowSize, G2A = G2/windowSize, R2A = R2/windowSize;
      int diffB = abs(B1A - B2A), diffG = abs(G1A - G2A), diffR = abs(B1A - B2A);
      // std::cout << "diffR: " << diffR << " diffG: " << diffG << " diffB: " << std::endl;
      if (diffB > max[0]) { max[0] = diffB;}
      // if (diffR > max[0]) { max[0] = diffR; std::cout << "new max R " << diffR << std::endl;}

      if (diffG > max[1]) { max[1] = diffG;}

      if (diffR > max[2]) { max[2] = diffR;}
    }
  }
}

int abs(int a) {
  if (a<0) {
    return -a;
  } else {
    return a;
  }
}

int compare(cv::Mat image1, cv::Mat image2, int WINDOW) {
  int windowSize = WINDOW * WINDOW;
  // make a window in size of WINDOW, width i
  for (int j=0; j<image1.cols-WINDOW; j++) {
    for (int i=0; i<image1.rows-WINDOW; i++) {
      int R1=0, G1=0, B1 = 0;
      int R2=0, G2=0, B2 = 0;
      for (int y=j; y<j+WINDOW-1; y++) {
        for (int x=i; x<i+WINDOW-1; x++) {
          cv::Vec3b px1 = image1.at<cv::Vec3b>(x, y);
          cv::Vec3b px2 = image2.at<cv::Vec3b>(x, y);
          R1 += px1[0]; G1 += px1[1]; B1 += px1[2];
          R2 += px2[0]; G2 += px2[1]; B2 += px2[2];
        }
      }
      int R1A = R1/windowSize, G1A = G1/windowSize, B1A = B1/windowSize;
      int R2A = R2/windowSize, G2A = G2/windowSize, B2A = B2/windowSize;
      std::cout << "WINDOW: [" << i << " " << j << "] " << " averageas difference img1-img2 [R G B]: " << R1A-R2A << "\t" << G1A-G2A << "\t" << B1A-B2A << std::endl;
    }
  }
};


// plot will create image and plot vectors into these images
int plot(std::vector<int> V1, std::vector<int> V2) {
  // get max vecrot size
  int size = V1.size();
  if (V2.size() > size) {
    size = V2.size();
  }
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

// plotVectorToImg will take image and plot pixel by pixel vector values
int plotVectorToImg(cv::Mat plot, std::vector<int> v, int x_offset, int y_offset, cv::Vec3b color) {

  // loop over vector and paint pixels ()
  for (int i=0; i<v.size(); i++) {
    plot.at<cv::Vec3b>(plot.rows-v[i]-y_offset, i+x_offset) = color;
    // for better visualization of plots
    plot.at<cv::Vec3b>(plot.rows-v[i]-y_offset-1, i+x_offset) = color;
  }
}
