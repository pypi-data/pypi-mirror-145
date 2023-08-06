
import ctypes
from dataclasses import dataclass,fields
import numpy as np
import tempfile
from ._bind import CJpegLib
from . import _jpeg

@dataclass
class DCTJPEG(_jpeg.JPEG):
    """JPEG instance to work in DCT domain."""
    Y: np.ndarray
    """luminance"""
    Cb: np.ndarray
    """chrominance blue-difference"""
    Cr: np.ndarray
    """chrominance red-difference"""
    qt: np.ndarray
    """quantization"""
    
    def is_read(self) -> bool:
        has_Y = self.Y is not None
        has_qt = self.qt is not None
        has_CbCr = self.Cb is not None and self.Cr is not None
        has_no_CbCr = self.Cb is None and self.Cr is None
        return (
            (has_Y and has_qt and has_no_CbCr) # grayscale
            or (has_Y and has_qt and has_CbCr) # color
        )
    
    def _alloc_dct_component(self, i:int):
        return (((ctypes.c_short * 64) * self.width_in_blocks(i)) * self.height_in_blocks(i))()
    def read_dct(self):
        # write content into temporary file
        tmp = tempfile.NamedTemporaryFile(suffix='.jpeg')
        tmp.write(self.content)
        tmp.flush()
        # allocate DCT components
        Y = self._alloc_dct_component(0)
        Cb,Cr = None,None
        if self.has_chrominance(): # has chrominance
            Cb = self._alloc_dct_component(1)
            Cr = self._alloc_dct_component(2)
        qt = ((ctypes.c_short * 64) * 4)()
        # call
        CJpegLib.read_jpeg_dct(
            srcfile     = tmp.name,
            Y           = Y,
            Cb          = Cb,
            Cr          = Cr,
            qt          = qt,
        )
        # close temporary file
        # process
        def process_component(comp):
            comp_np = np.ctypeslib.as_array(comp)
            return comp_np.reshape((*comp_np.shape[:-1],8,8))
        qt = process_component(qt)
        self.Y = process_component(Y)
        if self.has_chrominance():
            self.Cb = process_component(Cb)
            self.Cr = process_component(Cr)
        # crop
        self.qt = qt[:self.num_components]
        # return
        return self.Y,(self.Cb,self.Cr),self.qt
    
    def write_dct(self, path:str = None, quality:int=-1):
        """Writes DCT to JPEG.
        
        :param path: Destination file name. If not given, source file is overwritten.
        :type path: str, optional
        :param quality: Compression quality, between 0 and 100.
        :type quality: int, optional
        
        :Example:
        
        >>> jpeg = jpeglib.read_spatial("input.jpeg")
        >>> jpeg.write_spatial("output.jpeg", quality=92)
        """
        # write content into temporary file
        tmp = tempfile.NamedTemporaryFile(suffix='jpeg')
        tmp.write(self.content)
        # parameters
        dstfile = path if path is not None else self.path
        # convert dct
        def process_component(comp):
            comp = comp.reshape((*comp.shape[:-2],64))
            return np.ctypeslib.as_ctypes(comp.astype(np.int16))
        qt = process_component(self.qt)
        Y = process_component(self.Y)
        if self.has_chrominance():
            Cb = process_component(self.Cb)
            Cr = process_component(self.Cr)
        else: Cb,Cr = None,None
        # convert qt
        assert(quality in set(range(-1,101)))
        if quality != -1:
            qt = None
        # call
        CJpegLib.write_jpeg_dct(
            srcfile         = tmp.name,
            dstfile         = dstfile,
            Y               = Y,
            Cb              = Cb,
            Cr              = Cr,
            image_dims      = self.c_image_dims(),
            block_dims      = self.c_block_dims(),
            in_color_space  = self.jpeg_color_space.name,
            in_components   = self.num_components,
            qt              = qt,
            quality         = quality,
            num_markers     = self.num_markers(),
            marker_types    = self.c_marker_types(),
            marker_lengths  = self.c_marker_lengths(),
            markers         = self.c_markers(),
        )
    
    @property
    def Y(self) -> np.ndarray:
        """Luminance tensor getter."""
        if self._Y is None:
            self.read_dct()
        return self._Y
    @Y.setter
    def Y(self, Y: np.ndarray):
        """Luminance tensor setter."""
        self._Y = Y
    
    @property
    def Cb(self) -> np.ndarray:
        """Chrominance blue-difference tensor getter."""
        if self.has_chrominance() and self._Cb is None:
            self.read_dct()
        return self._Cb
    @Cb.setter
    def Cb(self, Cb: np.ndarray):
        """Chrominance blue-difference tensor setter."""
        self._Cb = Cb
    
    @property
    def Cr(self) -> np.ndarray:
        """Chrominance red-difference tensor getter."""
        if self.has_chrominance() and self._Cr is None:
            self.read_dct()
        return self._Cr
    @Cr.setter
    def Cr(self, Cr: np.ndarray):
        """Chrominance red-difference tensor setter."""
        self._Cr = Cr
    
    @property
    def qt(self) -> np.ndarray:
        """Quantization table getter."""
        if self._qt is None:
            self.read_dct()
        return self._qt
    @qt.setter
    def qt(self, qt: np.ndarray):
        """Quantization table setter."""
        self._qt = qt
    
    def free(self):
        """Free the allocated tensors."""
        del self._Y
        del self._Cb
        del self._Cr
        del self._qt
    
@dataclass
class DCTJPEGio(DCTJPEG):
    """Class for compatiblity with jpegio."""
    coef_arrays: list
    quant_tables: list
    def _convert_dct_jpegio(self, dct):
        return (dct
            .transpose((0,3,1,2))
            .reshape((dct.shape[0]*dct.shape[2], dct.shape[1]*dct.shape[3]))
        ).astype(np.int32)
    def _convert_jpegio_dct(self, dct):
        return (dct
            .reshape((-1,8,dct.shape[1]//8,8))
            .transpose((0,2,3,1))
        ).astype(np.int16)
    
    @property
    def coef_arrays(self):
        """Convertor of DCT coefficients to jpegio format."""
        if not self.is_read():
            self.read_dct()
        # collect dct
        self._coef_arrays = [
            self._convert_dct_jpegio(self.Y),
            self._convert_dct_jpegio(self.Cb),
            self._convert_dct_jpegio(self.Cr)
        ]
        return self._coef_arrays

    @coef_arrays.setter
    def coef_arrays(self, coef_arrays):
        self._coef_arrays = coef_arrays
    
    @property
    def quant_tables(self):
        """Convertor of quantization tables to jpegio format."""
        if not self.is_read():
            self.read_dct()
        self._quant_tables = [
            self.qt[0].astype(np.int32),
            self.qt[1].astype(np.int32)
        ]
        return self._quant_tables
    @quant_tables.setter
    def quant_tables(self, quant_tables):
        self._quant_tables = quant_tables
    
    def write(self, path:str = None, quality:int=-1):
        pass
        
        

def to_jpegio(jpeg: DCTJPEG):
    vals = {field.name: getattr(jpeg,field.name) for field in fields(jpeg)}
    return DCTJPEGio(**vals)

