# class Panorama:
#     """
#     ### Panorama class
#     """
#     #region Constructor
    
#     def __init__(self, Panorama=None, panorama_array=None, scratch=None, biXPelsPerMeter=None, biYPelsPerMeter=None, Lcs=None):
#         """_summary_

#         Parameters
#         ----------
#         panorama_array : _type_
#             _description_
#         Panorama : _type_, optional
#             _description_, by default None
#         scratch : _type_, optional
#             _description_, by default None
#         biXPelsPerMeter : _type_, optional
#             _description_, by default None
#         biYPelsPerMeter : _type_, optional
#             _description_, by default None
#         Lcs : _type_, optional
#             _description_, by default None
#         """
#         if Panorama is not None:
#             # Be sure it create copy of the Panorama
#             self = Panorama
#         elif scratch is not None:
#             self._scratch = scratch
#             self._biXPelsPerMeter = biXPelsPerMeter
#             self._biYPelsPerMeter = biYPelsPerMeter
#             self._Lcs = Lcs
#         else:
#             self._scratch = None
#             self._biXPelsPerMeter = biXPelsPerMeter
#             self._biYPelsPerMeter = biYPelsPerMeter
#             self._Lcs = Lcs
            
#         if panorama_array is not None:
#             self._panorama_array = panorama_array
    
    
    
#     #endregion
    
#     #region Public methods
#     def cut_out_panorama(self, x_start=0, x_end=-1, y_start=0, y_end=-1):
#         if len(self._panorama_array.shape) == 3:
#             new_panorama_array = self._panorama_array[y_start:y_end, x_start:x_end, :]
#         elif len(self._panorama_array.shape) == 2:
#             new_panorama_array = self._panorama_array[y_start:y_end, x_start:x_end]
            
            
#         return Panorama(Panorama = self, panorama_array = new_panorama_array)
    
#     def extract_panorama_parts(self, lc_search, lc_positions:Dict[int,int]=None):
#         if isinstance(lc_search, collections.Iterable) and len(lc_search) == 2:
#             lc_extract = lc_search
            
#         elif isinstance(lc_search, int):            
#             lc_extract = Scratch.get_lcs_to_extract(lc_search)
            
#         else:
#             raise(ValueError("lc_search must be an int, or a list of 2 ints"))
            
#         for lc in lc_extract:
#             if lc > 0:
#                 if lc in lc_positions or lc in self._Lcs:
#                     lc = self.lc_index(lc)
#                 else:
#                     LcNotDefinedError(lc)
#         x_start = self.get_lc_position(lc[0])
#         x_end = self.get_lc_position(lc[1])

        
#         return self.cut_out_panorama(self, x_start, x_end)
        
   
#     def display(self, downscale_ratio = 10, title = False, show_lcs = False, show = True, borne=[0,-1,0,-1]):
#         # if downscaleRatio > 1 :
#         #     image = transform.downscale_local_mean(np.array(self.panorama), (downscaleRatio, downscaleRatio, 1))/255
#         # else : 
#         #     image = self.panorama/255

#         image = downscale_panorama(self.panorama_array, downscale_ratio)/255
        
#         fig, ax = plt.subplots(figsize = (18, 9), clear = True)
#         ax.set_xmargin(0)
#         ax.set_yticks([])
#         ax.set_xticks([])
#         plt.box(on = None)
#         if title : plt.title(self.filename , fontsize=15, color = 'white')
#         io.imshow(image[borne[0]:borne[1],borne[2]:borne[3]])

#         if show_lcs:
#             plot_lc_panorama(self, ax, len_xAxis=np.shape(image)[1], start_ind=borne[2], end_ind=borne[3])

#         if show: plt.show()

#         return fig, ax, image
        
#     #endregion
    
#     #region Private methods
    
#     #endregion
    
#     #region Properties
#     def get_panorama_array(self):
#         return self._panorama_array
    
#     def set__panorama_array(self, value:np.ndarray):
#         self._panorama_array = value
    
#     panorama_array = property(get_panorama_array, set__panorama_array)    
#     panorama = property(get_panorama_array, set__panorama_array)
    
#     def get_scratch(self):
#         return self.__scratch
    
#     def set_scratch(self, value):
#         self.__scratch = value
        
#     _scratch = property(get_scratch, set_scratch)
    
#     def get_biXPelsPerMeter(self):
#         return self.__biXPelsPerMeter
    
#     def set_biXPelsPerMeter(self, value):
#         self.__biXPelsPerMeter = value
        
#     _biXPelsPerMeter = property(get_biXPelsPerMeter, set_biXPelsPerMeter)
    
#     def get_biYPelsPerMeter(self):
#         return self.__biYPelsPerMeter
    
#     def set_biYPelsPerMeter(self, value):
#         self.__biYPelsPerMeter = value
        
#     _biYPelsPerMeter = property(get_biYPelsPerMeter, set_biYPelsPerMeter)
    
#     def get_Lcs(self):
#         return self.__Lcs
    
#     def set_Lcs(self, value:Dict[int,int]):
#         self.__Lcs = value
        
#     _Lcs = property(get_Lcs, set_Lcs)
    
    
        
#     @property
#     def array(self):
#         return self._array
    
    
#     @array.setter
#     def array(self, value : np.ndarray):
#         self._array = value
#     #endregion
    
#     #region Attributes
    
#     #endregion
    
#     #region Static methods
    
#     #endregion