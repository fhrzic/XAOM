# Import librearies
import pydicom
import numpy as np
import matplotlib.pyplot as plt
import cv2
import json

# Class for manipulating dicom data
class dicomObject:
  
  # Init of class variables
  def __init__(self):
    self.dicomData = None   
    self.dicomImage = np.empty(shape=(0, 0) )
    self.dicomFile = None
    self.pixelData = None
  
  # Open data file
  def importDicom(self, dicomFile):
    # Get data
    try:
      self.dicomData = pydicom.dcmread(dicomFile)
      self.dicomFile = dicomFile
      return 1
    except IOError: 
      print ("ERROR: Could not read dicom File. Check your file and try again")
      return 0
  
  # Show all tags in dicom header
  def showTags(self):
    print (self.dicomData.dir())

  # Get image bit representation
  def getBitRepresentation(self):
    return (self.dicomData.BitsStored)

  # Export dicom data as 16-bit image
  def exportDicomTo16Png(self, fileName = None):
    if fileName == None: 
      fileName = self.dicomFile + ".png"
  
    if ("PixelData" not in self.dicomData.dir()):
      print ("ERROR: Missing PixelData in Dicom file. Check your Dicom file with ImageJ tool.")
      return 0
    else:
      self.pixelData = self.dicomData.pixel_array
      data = self.dicomData.pixel_array
      scale = self.dicomData.BitsStored      
      scale = 65536 / pow(2, scale)
      

    self.dicomImage = data * np.uint16(scale)    
    cv2.imwrite(fileName, self.dicomImage)

  # Export dicom data as 8-bit image
  def exportDicomTo8Png(self, fileName = None):
    if fileName == None: 
      fileName = self.dicomFile + ".png"
    if ("WindowCenter" not in self.dicomData.dir() or "WindowWidth" not in self.dicomData.dir()):
      print ("ERROR: Could not export dicom data to png. Missing tags: 'WindowCenter' or 'WindowWidth'")
      return 0

    if ("PixelData" not in self.dicomData.dir()):
      print ("ERROR: Missing PixelData in Dicom file. Check your Dicom file with ImageJ tool.")
      return 0
    else:
      self.pixelData = self.dicomData.pixel_array
      data = self.dicomData.pixel_array
      level = self.dicomData.WindowCenter
      window = self.dicomData.WindowWidth
   

    self.dicomImage = np.piecewise(data,[data <= (level - 0.5 - (window-1)/2), data > (level - 0.5 + (window-1)/2)], 
      [0, 255, lambda data: ((data - (level - 0.5))/(window-1) + 0.5)*(255-0)])
    
    self.dicomImage = cv2.convertScaleAbs(self.dicomImage)
    cv2.imwrite(fileName, self.dicomImage)

  # Return 8-bit dicom image
  def getDicom8bit(self):
    if ("WindowCenter" not in self.dicomData.dir() or "WindowWidth" not in self.dicomData.dir()):
      print ("ERROR: Could not convert dicom data to 8bit. Missing tags: 'WindowCenter' or 'WindowWidth'")
      return 0

    if ("PixelData" not in self.dicomData.dir()):
      print ("ERROR: Missing PixelData in Dicom file. Check your Dicom file with ImageJ tool.")
      return 0
    else:
      self.pixelData = self.dicomData.pixel_array.copy()
      data = self.dicomData.pixel_array
      level = self.dicomData.WindowCenter
      window = self.dicomData.WindowWidth
    
    self.dicomImage = np.piecewise(data,[data <= (level - 0.5 - (window-1)/2), data > (level - 0.5 + (window-1)/2)], 
      [0, 255, lambda data: ((data - (level - 0.5))/(window-1) + 0.5)*(255-0)])

    
    self.dicomImage = cv2.convertScaleAbs(self.dicomImage)
    return self.dicomImage

  # Return 16-bit dicom image
  def getDicom16bit(self):
    if ("PixelData" not in self.dicomData.dir()):
      print ("ERROR: Missing PixelData in Dicom file. Check your Dicom file with ImageJ tool.")
      return 0
    else:
      self.pixelData = self.dicomData.pixel_array.copy()
      self.dicomImage = np.empty(shape=(0, 0) )
      return self.pixelData
    

  # Preview 8-bit dicom image. It can also resize image
  def previewImage(self, resizeFactor = 1):
    if (self.dicomImage.size != 0 and self.dicomImage.dtype == 'uint8' ):
      cv2.imshow('Dicom image', cv2.resize(self.dicomImage, (0,0), fx=resizeFactor, fy=resizeFactor) )
      cv2.waitKey(0)
      return 1
    else:
      print ("ERROR: Could not display 16bit dicom image. Use 'getDicom8bit' method first.")
      return 0

  # Anonimise dicom
  def anonymize(self, override = False):
    self.dicomData[0x10,0x10].value = "NA"
    self.dicomData[0x10,0x20].value = "NA"
    self.dicomData[0x10,0x30].value = "NA"
    self.dicomData[0x10,0x40].value = "NA"
    self.dicomData[0x17,0x10].value = "NA"
    if override:
      self.dicomData.save_as(self.dicomFile)
    return 1

  # Export dicom
  def exportDicomToFile(self, fileName = None):
    if fileName == None:
      print ("ERROR: No file name provided. Please use method as: exportDicomToFile(fileName='name')")
      return 0
    self.dicomData.save_as(fileName)
    return 1

  # Export Json
  def exportDicomJSONData(self, fileName = None):
    if fileName == None:
      print ("ERROR: No file name provided. Please use method as: exportDicomToFile(fileName='name')")
      return 0

    centre = self.dicomData.WindowCenter
    width = self.dicomData.WindowWidth
    bits = self.dicomData.BitsStored
    colums = self.dicomData.Columns
    rows = self.dicomData.Rows
    if ('ImagerPixelSpacing' in self.dicomData.dir()):
      pixel_spacing = list(self.dicomData.ImagerPixelSpacing)
    else:
      if ('PixelSpacing' in self.dicomData.dir()):
        pixel_spacing = list(self.dicomData.PixelSpacing)
      

    data = {'Centre': centre, 'Width': width, 
    'Bits': bits, 'Columns': colums, 'Rows': rows, 
    'PixelSpacing': pixel_spacing}

    with open(fileName, 'w') as outfile:
      json.dump(data, outfile)
    return 1

  # Check for tags
  def checkForTags(self):
    if 'ImagerPixelSpacing' in self.dicomData.dir() or 'PixelSpacing' in self.dicomData.dir():
      if ("WindowCenter" not in self.dicomData.dir() or "WindowWidth" not in self.dicomData.dir() or "Columns" not in self.dicomData.dir() or
        "Rows" not in self.dicomData.dir() or "BitsStored" not in self.dicomData.dir()):
        return 0
    else:
      return 0
    return 1
