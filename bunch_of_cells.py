import numpy as np
import PIL
from PIL import Image

''' The module is centered around 'BunchOfCells' object having:
       INIT_ARGUMENTS:
            - 4D array of slices derived from initial picture through 'ImageLoader.getCells()'
       ATTRIBUTES:
            - radius_red:           outer radius of FT-matrix to be incremented
            - radius_blue:          inner radius of FT-matrix to which radius_red is contrasted
            !!! radius_red>radius_blue, otherwise exception's raised !!!
            - red_blue_contrast:    minimal value of contrast added

       METHODS:
            - markCells(): transforms FT's of some cells
            - saveImage(): collects transformed cells into single image and saves to a new file
'''



# meddles with FT of a cell thus marking it
def markSingleCell(Cell, Mask,  MaxRedBlueDiffinRow, Avg_red, red_blue_contrast):



    CellFT = np.fft.fft2(Cell)
    MultiplyFactorForRed = (MaxRedBlueDiffinRow + red_blue_contrast)/Avg_red
    Mask*= MultiplyFactorForRed
    CellFT+= Mask*CellFT
    Cell = np.fft.ifft2(CellFT)
    error = np.max(np.abs(np.imag(Cell)))


    return error, Cell


# produces from input zero matrix a mask of units with given radius
def getMask(Matrix, LenOfCellSide, radius):

    L= LenOfCellSide
    r = radius
    # top left corner
    Matrix[r, range(1, r+1)] = 1
    Matrix[range(1, r+1), r] = 1

    # left low
    Matrix[L-r, range(1, r+1)] =1
    Matrix[range(L-r, L), r]   =1

    # right low
    Matrix[L-r, range(L-r, L)] =1
    Matrix[range(L-r, L), L-r] =1

    #right top
    Matrix[r, range(L-r, L)] =1
    Matrix[range(1, r+1), L-r] =1


    return Matrix







class BunchOfCells:

    def __init__(self, InputMatrixOfCells):

        self.InputMatrixOfCells = InputMatrixOfCells





    def markCells(self):

        assert hasattr(self, 'radius_red') and hasattr(self, 'radius_blue') and hasattr(self, 'red_blue_contrast')
        NofRowsCells, NofColsCells, LenOfCellSide, _ = self.InputMatrixOfCells.shape
        if 2*self.radius_red>= LenOfCellSide or self.radius_blue>= self.radius_red:
            raise Exception( 'Error: Mismatch between red, blue radii and LenOfCellSide!')

        # Masks for FT-matrix transformation
        FTRedMask   = getMask(np.zeros([LenOfCellSide, LenOfCellSide]), LenOfCellSide, self.radius_red )
        FTBlueMask  = getMask(np.zeros([LenOfCellSide, LenOfCellSide]), LenOfCellSide, self.radius_blue )












        # getting matrix of average FT amplitudes for all cells at 'radius_red' and 'radius_blue'
        FTMtrxOfAvg_red  = np.zeros([NofRowsCells, NofColsCells])
        FTMtrxOfAvg_blue = np.zeros([NofRowsCells, NofColsCells])
        for jr in range(NofRowsCells):
            for jc in range (NofColsCells):
                FTMagnitudeMtrx  = np.abs(np.fft.fft2(self.InputMatrixOfCells[jr, jc, :, :]))

                FTMtrxOfAvg_blue[jr, jc] = np.sum(FTBlueMask*FTMagnitudeMtrx)/(4*self.radius_blue)

                FTMtrxOfAvg_red[jr, jc] = np.sum(FTRedMask*FTMagnitudeMtrx)/(4*self.radius_red)







        # marking cells via chess-board pattern
        for jr in range(NofRowsCells):
            MaxRedBlueDiffinRow = np.max(FTMtrxOfAvg_red[jr,:] - FTMtrxOfAvg_blue[jr,:])
            MaxRedBlueDiffinRow = np.max([0, MaxRedBlueDiffinRow]) # in case Red<Blue everywhere in the row
            for jc in range (NofColsCells):
                if (jr+jc)%2==1:
                    error, self.InputMatrixOfCells[jr, jc, :, :] = markSingleCell(self.InputMatrixOfCells[jr, jc, :, :], FTRedMask,
                                                                           MaxRedBlueDiffinRow, FTMtrxOfAvg_red[jr, jc],
                                                                           self.red_blue_contrast)

                    print 'Cell(',str(jr),',',str(jc), '): max abs(imaginary part ignored) = ',error

    #saves array of cells back into image
    def saveImage(self, OutputFileName):

        NofRowsCells, NofColsCells, LenOfCellSide, _ = self.InputMatrixOfCells.shape
        OutputMatrix = np.zeros([NofRowsCells*LenOfCellSide, NofColsCells*LenOfCellSide])
        for jRows in range(NofRowsCells):
            RowImageBegin =  jRows*LenOfCellSide
            RowImageEnd   =  RowImageBegin + LenOfCellSide

            for jCols in range(NofColsCells):
                ColImageBegin =  jCols*LenOfCellSide
                ColImageEnd   =  ColImageBegin + LenOfCellSide

                OutputMatrix[RowImageBegin:RowImageEnd, ColImageBegin:ColImageEnd] = self.InputMatrixOfCells[jRows, jCols, :, :]

        PIL.Image.fromarray(np.swapaxes(OutputMatrix, 0, 1).astype('uint8'), mode='L').show()
        PIL.Image.fromarray(np.swapaxes(OutputMatrix, 0, 1).astype('uint8'), mode='L').save(OutputFileName)









