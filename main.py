from image_loader   import ImageLoader
from bunch_of_cells import BunchOfCells

InputFileName = 'babaYaga.jpg'


ImgLdr = ImageLoader(InputFileName)
ImgLdr.LenOfCellSide = 100

# input picture is cut into squares of side 'LenOfCellSide'
MatrixOfCells = ImgLdr.getCells()


# object for image marking
BunchOfCells = BunchOfCells(MatrixOfCells)

# marking parameters setting
BunchOfCells.radius_red  = 49
BunchOfCells.radius_blue = 48
BunchOfCells.red_blue_contrast = 10


# image slices are marked, put back into single picture and saved to a new file
BunchOfCells.markCells()
OutputFileName = InputFileName.split('.')[0]+ '_marked'                                                          + \
                                              '_CellSide'               + str(ImgLdr.LenOfCellSide)             + \
                                              '_radius_red'             + str(BunchOfCells.radius_red)          + \
                                              '_radius_blue'            + str(BunchOfCells.radius_blue)         + \
                                              '_red_blue_contrast'      + str(BunchOfCells.red_blue_contrast)   + \
                                              '.'                       + InputFileName.split('.')[1]


BunchOfCells.saveImage(OutputFileName)








