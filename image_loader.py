import PIL
from PIL import Image
import numpy as np

class ImageLoader:

    '''Storage for RGB input image
       INIT_PARAMETERS:
            - InputFileName
       ATTRIBUTES:
            - LenOfCellSide: side of single square cell original image is sliced into

       METHODS:
            - getCells(): returns array of grayscale slices of the input image
    '''



    def __init__(self, InputFileName):

        self.InputFileName = InputFileName
        self.Image         = PIL.Image.open(InputFileName)
        #self.Image.show()

        self.NofRows, self.NofCols = self.Image.size
        self.DataMtx = np.array(list(self.Image.getdata())).reshape(self.NofCols, self.NofRows, 3)
        self.DataMtx = np.swapaxes(self.DataMtx, 0, 1)


        #PIL.Image.fromarray(np.swapaxes(self.DataMtx, 0, 1).astype('uint8'), mode='RGB').show()



        # conversion to grayscale
        self.DataMtx = np.linalg.norm(self.DataMtx, axis=2)
        self.DataMtx = self.DataMtx*255/self.DataMtx.max()
        #PIL.Image.fromarray(np.swapaxes(self.DataMtx.astype('uint8'), 0, 1), mode='L').show()





    def getCells(self):                                     # returns 4D array of cells from original image


        assert hasattr(self, 'LenOfCellSide')               # make sure len of cell side is set


        NofRowsCells = self.NofRows/self.LenOfCellSide      # number of cells along row-dimension
        NofColsCells = self.NofCols/self.LenOfCellSide      # number of cells along col-dimension
        if (NofRowsCells<=1) or (NofColsCells<=1):
            print 'Too large cell size'
            raise

        OutputMatrixOfCells = np.array(range(  NofRowsCells*NofColsCells*(self.LenOfCellSide**2)   ))
        OutputMatrixOfCells = OutputMatrixOfCells.reshape(NofRowsCells, NofColsCells, self.LenOfCellSide, self.LenOfCellSide)

        # Slicing image into cells
        for jRows in range(NofRowsCells):
            RowImageBegin =  jRows*self.LenOfCellSide
            RowImageEnd   =  RowImageBegin + self.LenOfCellSide

            for jCols in range(NofColsCells):
                ColImageBegin =  jCols*self.LenOfCellSide
                ColImageEnd   =  ColImageBegin + self.LenOfCellSide

                OutputMatrixOfCells[jRows, jCols, :, :] = self.DataMtx[RowImageBegin:RowImageEnd, ColImageBegin:ColImageEnd]



        return OutputMatrixOfCells










