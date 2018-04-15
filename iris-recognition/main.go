package main

import (
	"image"
	"image/png"
	// "image/draw"
	"fmt"
	"image/color"
	"log"
	"os"
)

func main() {
	// load file
	f, err := os.Open("irises_MICHE_iPhone5_norm/001_IP5_IN_F_RI_01_1.iris.norm.png")
	if err != nil {
		log.Fatalln(err)
	}
	defer f.Close()

	// decode image
	pic, err := png.Decode(f)
	if err != nil {
		log.Fatalln(err)
	}
	fmt.Println(hist(pic, 255))

	// display HIST
	img := image.NewRGBA(image.Rect(0, 0, 1000, 500))

	drawHist(img, hist(pic, 50), color.RGBA{255, 0, 0, 255})

	// save to file
	fH, err := os.Create("hist.png")
	if err != nil {
		log.Fatalln(err)
	}
	defer fH.Close()
	png.Encode(fH, img)
}

func hist(pic image.Image, n int) []int {
	// get properties of image
	width := pic.Bounds().Size().X
	height := pic.Bounds().Size().Y
	hist := make([]int, n)
	window := 255 / n
	fmt.Println(1 / window)
	fmt.Printf("%T", window)

	for i := 0; i < width; i++ {
		for j := 0; j < height; j++ {
			r, g, b, _ := pic.At(i, j).RGBA()
			r, g, b = r/257, g/257, b/257
			pxG := int(0.299*float64(r) + 0.587*float64(g) + 0.114*float64(b))
			wNumber := pxG / window

			if wNumber >= n {
				continue
			}

			hist[wNumber]++
		}
	}
	return hist
}

func drawHist(img *image.RGBA, hist []int, col color.RGBA) {
	// X := img.Bounds().Size().X
	// Y := img.Bounds().Size().Y
	fmt.Println("len of hist is: ", len(hist))
	drawFrame(img)
	// minX, maxX, minY, maxY := drawAxes(img, col)
	drawAxes(img, col)

	for i := 0; i < len(hist); i++ {
		for j := 0; j < 10; j++ {
			img.Set(i+j+100, hist[i], col)
		}
	}

}

func drawAxes(img *image.RGBA, col color.RGBA) (xS, xE, yS, yE int) {

	width := img.Bounds().Size().X
	height := img.Bounds().Size().Y
	x := width / 10
	y := height / 10

	xStart := x / 2
	xEnd := width - xStart
	yStart := y / 2
	yEnd := height - yStart

	for i := xStart; i<xEnd; i++ {
		img.Set(i, height-y, col)
	}

	for i := yStart; i<yEnd; i++ {
		img.Set(x, i, col)
	}

	return x, width-x, y, height-y
}

func drawFrame(img *image.RGBA) {
	for i := 0; i < img.Bounds().Size().X; i++ {
		img.Set(i, 0, color.RGBA{0, 0, 0, 255})
		img.Set(i, img.Bounds().Size().Y-1, color.RGBA{0, 0, 0, 255})
	}
	for i := 0; i < img.Bounds().Size().Y; i++ {
		img.Set(0, i, color.RGBA{0, 0, 0, 255})
		img.Set(img.Bounds().Size().X-1, i, color.RGBA{0, 0, 0, 255})
	}
}

func drawRect(img *image.RGBA, startX, startY, endX, endY int, fill bool, col color.RGBA) {
	for i := startX; i < endX; i++ {
		for j := startY; j < endY; j++ {
			
		}
	}
}
