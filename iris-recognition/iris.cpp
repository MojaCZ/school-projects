// g++ iris.cpp -o iris -std=c++11 `pkg-config --cflags --libs opencv`
#include <iostream>
#include <string>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <dirent.h>
#include <unistd.h>
#include <sys/types.h>
#include <iomanip>

std::vector<std::string> loadDir(std::string);
int compareImages(std::vector<std::string>);
int compareHistograms(cv::Mat, cv::Mat);
std::vector<int> vecFromImg(cv::Mat, int);
std::vector<int> flWindow(std::vector<int>, int);
std::vector<int> scaleVector(std::vector<int>, int);
int plot(std::vector<int>, std::vector<int>);
int plotVectorToImg(cv::Mat, std::vector<int>, int, int, cv::Vec3b);
int DFT(cv::Mat);

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

  // image2 = cv::imread("irises_MICHE_iPhone5_norm/004_IP5_OU_F_LI_01_1.iris.norm.png");
  image2 = cv::imread("irises_MICHE_iPhone5_norm/008_IP5_IN_R_LI_01_1.iris.norm.png");
  // image2 = cv::imread("irises_MICHE_iPhone5_norm/001_IP5_IN_F_RI_01_2.iris.norm.png");
  if (! image2.data) {
    std::cout << "Could not open or find image2" << std::endl;
    return -1;
  }

  DFT(image1);
  DFT(image2);

  if (image1.cols != image2.cols || image1.rows != image2.rows) {
    std::cout << "dim of picture 1 is not equal to dim of picture2";
    return -1;
  }

  // compareHistograms(image1, image2);

  // std::vector<int> V1, V2;
  // V1 = vecFromImg(image1, 10);
  // V2 = vecFromImg(image2, 10);
  //
  // V1 = flWindow(V1, 100);
  // V2 = flWindow(V2, 100);
  //
  // plot(V1, V2);

  // cv::namedWindow("Display window", cv::WINDOW_AUTOSIZE);
  // cv::imshow("image1", image1);
  // cv::waitKey(0);
  // cv::imshow("image2", image2);
  // cv::waitKey(0);

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

std::vector<int> vecFromImg(cv::Mat img, int window) {
  std::vector<int> V;

  // convert image to greyscale
  cv::Mat greyImg;
  cv::cvtColor(img, greyImg, cv::COLOR_RGB2GRAY);

  int windowSize = window * window;
  // std::cout << (int)greyImg.at<uchar>(50, 50) << std::endl;

  for (int j=0; j<img.cols-window; j++) {
    for (int i=0; i<img.rows-window; i++) {
      int S = 0;
      for (int y=j; y<j+window; y++) {  // WINDOW-1
        for (int x=i; x<i+window; x++) {  //WINDOW-1
          S += (int)greyImg.at<uchar>(x, y);
        }
      }
      int A = S / windowSize;
      V.push_back(A);
    }
  }
  return V;
};

// plot will create image and plot vectors into these images
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
  std::cout << "maxSize: " << maxSize << "scale ratio: " << scale << std::endl;

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
  return 1;
}

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
  std::cout << NV.size() << std::endl;
  return NV;

}

int DFT(cv::Mat img) {
  // convert image to greyscale
  cv::Mat greyImg;
  cv::cvtColor(img, greyImg, cv::COLOR_RGB2GRAY);

  // expand to optimal size
  cv::Mat padded;
  int m = cv::getOptimalDFTSize(greyImg.rows);
  int n = cv::getOptimalDFTSize(greyImg.cols);
  cv::copyMakeBorder(greyImg, padded, 0, m-greyImg.rows, 0, n-greyImg.cols, cv::BORDER_CONSTANT, cv::Scalar::all(0));
  cv::Mat planes[] = {cv::Mat_<float>(padded), cv::Mat::zeros(padded.size(), CV_32F)};
  cv::Mat complexI;
  cv::merge(planes, 2, complexI);

  cv::dft(complexI, complexI);

  cv::split(complexI, planes);
  cv::magnitude(planes[0], planes[1], planes[0]);
  cv::Mat magI = planes[0];

  magI += cv::Scalar::all(1);

  magI = magI(cv::Rect(0, 0, magI.cols & -2, magI.rows & -2));

  int cx = magI.cols/2;
  int cy = magI.rows/2;

  cv::Mat q0(magI, cv::Rect(0, 0, cx, cy));
  cv::Mat q1(magI, cv::Rect(cx, 0, cx, cy));
  cv::Mat q2(magI, cv::Rect(0, cy, cx, cy));
  cv::Mat q3(magI, cv::Rect(cx, cy, cx, cy));

  cv::Mat tmp;
  q0.copyTo(tmp);
  q3.copyTo(q0);
  tmp.copyTo(q3);

  q1.copyTo(tmp);
  q2.copyTo(q1);
  tmp.copyTo(q2);

  cv::normalize(magI, magI, 0, 1, cv::NORM_MINMAX);
  // HOW TO CROP IMAGE SO IT SHOWS ONLY INTERESTING PART OF SPECTRUM
  cv::Mat zoom;
  cv::pyrUp(magI, zoom, cv::Size(magI.cols * 2, magI.rows * 2));

  cv::imshow("Input Image", img);
  cv::imshow("spectrum magnitude", zoom);
  cv::waitKey();
  return 0;
}
