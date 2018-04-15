package main

import (
	"image"
	"image/png"
	// "image/draw"
	"errors"
	"fmt"
	"image/color"
	"log"
	"os"
)

// basic colors
var (
	red    = color.RGBA{255, 0, 0, 255}
	green   = color.RGBA{0, 255, 0, 255}
	blue  = color.RGBA{0, 0, 255, 255}
	redT   = color.RGBA{255, 0, 0, 100}
	blueT  = color.RGBA{0, 255, 0, 100}
	greenT = color.RGBA{0, 0, 255, 100}
	black  = color.RGBA{0, 0, 0, 255}
	white  = color.RGBA{255, 255, 255, 255}
)

// ieis is structure keeping information about image and it's path
type iris struct {
	img     image.Image
	imgPath string
}

// NewIris is constructor for iris struct
// requires path to image
// returns pointer to iris structure
func NewIris(imgPath string) (I *iris) {
	I = new(iris)
	I.imgPath = imgPath

	// load file
	f, err := os.Open(imgPath)
	if err != nil {
		log.Fatalln(err)
	}
	defer f.Close()

	// decode image
	I.img, err = png.Decode(f)
	if err != nil {
		log.Fatalln(err)
	}
	return I
}

// GiveHist is function that scan whole image and create hist of
// first parameter is color, it is given as rune 'R' red, 'G' green, 'B' blue, 'g' gray
// color tells us which part of RGB we want to consider to histogram
func (I iris) GiveHist(col rune, n uint8) (H *hist) {
	var F func(int, int) uint8
	if n < 0 || n > 255 {
		log.Fatalln(errors.New("Histogram can be conposed only from n ∈ (0, 255)"))
	}

	switch col {
	case 'R':
		F = func(i, j int) uint8 {
			r, _, _, _ := I.img.At(i, j).RGBA()
			r = r / 257
			return uint8(r)
		}
	case 'G':
		F = func(i, j int) uint8 {
			_, g, _, _ := I.img.At(i, j).RGBA()
			g = g / 257
			return uint8(g)
		}
	case 'B':
		F = func(i, j int) uint8 {
			_, _, b, _ := I.img.At(i, j).RGBA()
			b = b / 257
			return uint8(b)
		}
	case 'g':
		F = func(i, j int) uint8 {
			r, g, b, _ := I.img.At(i, j).RGBA()
			r, g, b = r/257, g/257, b/257
			pxG := uint8(0.299*float32(r) + 0.587*float32(g) + 0.114*float32(b))
			return pxG
		}
	default:
		log.Fatalln(errors.New("Histogram can be construct only from R, B, G or g (gray) colors "))
	}

	// get properties of image
	width := I.img.Bounds().Size().X
	height := I.img.Bounds().Size().Y

	h := make([]uint, n)
	window := 255 / float32(n-1)
	for i := 0; i < width; i++ {
		for j := 0; j < height; j++ {
			px := F(i, j)
			wNumber := float32(px) / window

			if wNumber >= float32(n) {
				fmt.Println(wNumber, n)
				continue
			}

			h[int(wNumber)]++
		}
	}
	H = NewHist(h)
	return H
}

type hist struct {
	hist []uint
	MaxN uint
	Min  uint8
	Max  uint8
}

func NewHist(h []uint) (H *hist) {
	H = new(hist)
	H.hist = h
	return H
}

func (H *hist) MaxNum() {
	for _, e := range H.hist {
		if e > H.MaxN {
			H.MaxN = e
		}
	}
}

func (H *hist) MinMax() {

	if H.MaxN == 0 {
		H.MaxNum()
	}

	haveMin := false
	var min, max int
	for i, e := range H.hist {
		// HOW TO KNOW THIS NUMBER??? ---------------------------------
		if e > H.MaxN/150 {
			if !haveMin {
				min = i
				haveMin = true
			}
			max = i
		}
	}
	H.Min = uint8(min)
	H.Max = uint8(max)
	fmt.Println(H.Min, H.Max)
}

// OPTIMIZE THIS
func (H hist) Neco() {
	var sum uint
	for _, e := range H.hist {
		sum += e
	}
	fmt.Println(sum)
}


type canvas struct {
	pic *image.RGBA
}

func NewCanvas() (C *canvas) {
	C = new(canvas)
	C.pic = image.NewRGBA(image.Rect(0, 0, 1000, 500))
	return C
}

func (C canvas) SaveCanvas(canvasPath string) {
	// save to file
	picFile, err := os.Create(canvasPath)
	if err != nil {
		log.Fatalln(err)
	}
	defer picFile.Close()
	png.Encode(picFile, C.pic)
}

func (C *canvas) DrawFrame() {
	for i := 0; i < C.pic.Bounds().Size().X; i++ {
		C.pic.Set(i, 0, black)
		C.pic.Set(i, C.pic.Bounds().Size().Y-1, black)
	}
	for i := 0; i < C.pic.Bounds().Size().Y; i++ {
		C.pic.Set(0, i, black)
		C.pic.Set(C.pic.Bounds().Size().X-1, i, black)
	}
}

func (C *canvas) DrawAxes(col color.RGBA) (xS, xE, yS, yE int) {
	width := C.pic.Bounds().Size().X
	height := C.pic.Bounds().Size().Y
	x := width / 10
	y := height / 10

	xStart := x / 2
	xEnd := width - xStart
	yStart := y / 2
	yEnd := height - yStart

	for i := xStart; i < xEnd; i++ {
		C.pic.Set(i, height-y, col)
	}

	for i := yStart; i < yEnd; i++ {
		C.pic.Set(x, i, col)
	}

	return x, width - x, y, height - y
}

func (C *canvas) DrawRect(startX, startY, endX, endY int, col color.RGBA) {
	for i := startX; i < endX; i++ {
		for j := endY; j < startY; j++ {
			C.pic.Set(i, j, col)
		}
	}
}

func (C *canvas) DrawHist(hist []uint, col color.RGBA) {
	C.DrawFrame()
	minX, maxX, minY, maxY := C.DrawAxes(black)
	space := (maxX - minX) / len(hist) / 2

	// get ratio and resize histogram
	scaleHist := hist
	ratio := float32(maxY-minY) / float32(maxSlice(hist))
	for i, _ := range scaleHist {
		scaleHist[i] = uint(ratio * float32(scaleHist[i]))
	}

	x := minX + space
	for i := 0; i < len(hist); i++ {
		C.DrawRect(x, maxY, x+space, maxY-int(scaleHist[i]), col)
		x += 2 * space
	}
	for j := minY; j < maxY; j++ {
		C.pic.Set(x, j, black)
	}
}

func maxSlice(s []uint) (max uint) {
	for _, e := range s {
		if e > max {
			max = e
		}
	}
	return max
}

func main() {
	I1 := NewIris("irises_MICHE_iPhone5_norm/001_IP5_IN_F_RI_01_1.iris.norm.png")
	HB1 := I1.GiveHist('B', 200)
	I2 := NewIris("irises_MICHE_iPhone5_norm/004_IP5_OU_F_LI_01_1.iris.norm.png")
	// I2 := NewIris("irises_MICHE_iPhone5_norm/001_IP5_IN_F_RI_01_2.iris.norm.png")
	HB2 := I2.GiveHist('B', 200)
	HB1.Neco()
	HB2.Neco()
	C1 := NewCanvas()
	C2 := NewCanvas()
	C1.DrawHist(HB1.hist, blue)
	C2.DrawHist(HB2.hist, blue)
	C1.SaveCanvas("compare1.png")
	C2.SaveCanvas("compare2.png")
}
