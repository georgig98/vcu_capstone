#=== IMPORTS ============================================================================================

# Get Python3 print() function
from __future__ import print_function

# Standard libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import sys
import time
import platform
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# CTypes support
from ctypes import *
# Named tuples (structs) support
from collections import namedtuple

# Histogram support
histogramSupport = False
try:
    #import asciiHistogram_lib as histogram
    import printHistogram_lib as histogram
    histogramSupport = True
except ImportError:
    histogram = None
    pass

def runDetect(loop):
    """ The following function runs the Kromek supplied detection software and returns the input file for the 
    Fortran program to run through"""
    #========================================================================================================
    #=== CONFIGURATION (User Configurable) ==================================================================
    global outputPrefixPadding
    global outputPrefix
    global verboseOutput
    global runtime_OS
    global runtime_64bit
    global _kromek
    global DataReceived_FirstTimestamp
    global DataReceived_TimestampOffset_ms
    global writefile
    
    # Logging / Output
    verboseOutput                   = True
    outputPrefix                    = "Kromek Lib:"
    outputPrefixPadding             = 15

    # Diagnostics (when executing this file directly)
    
    if loop.lower() == 'yes':
        timeup = 15
    else:
        timeup = input('Enter live time in seconds (must be greater than or equal to 10 s): ')
    
    while int(timeup) < 10 or int(timeup) > 100:
        print('Live time must be greater than or equal to 10 s and less than 100 seconds')
        timeup = input('Enter live time in seconds: ')
        
     
    diagnostics_LiveTime_sec        = timeup 
    diagnostics_FactoryReset        = False
    diagnostics_PrintStatusEvents   = True
    diagnostics_PrintRawDataEvents  = True
    diagnostics_Histogram_enabled   = True
    diagnostics_Histogram_bins      = 48
    diagnostics_Histogram_height    = 10
    diagnostics_Write_CSVs          = False

    #========================================================================================================
    #=== LOAD DRIVER ========================================================================================

    # Automatic check of Windows/Linux & 32/64-bit
    runtime_OS = platform.system()
    runtime_64bit = sys.maxsize > 2 ** 32

    # Kromek spectrometer driver
    if runtime_OS == "Linux":
        _kromek = cdll.LoadLibrary('kromek_drivers/linux/libSpectrometerDriver.so')
    elif runtime_OS == "Windows":
        if runtime_64bit:
            _kromek = windll.LoadLibrary('kromek_drivers/windows64/SpectrometerDriver.dll')
        else:
            _kromek = windll.LoadLibrary('kromek_drivers/windows32/SpectrometerDriver.dll')
    else:
        raise Exception('Unsupported OS for pyKromek library!')

    #========================================================================================================
    #=== GLOBALS ============================================================================================

    # -- Version information
    versionLib                  = "1.0.5"

    # -- CALLBACKS (Keep references to CFUNCTYPE() objects...)
    CB_ERROR                    = None
    callback_Error              = None
    callbackFwd_Error           = None

    CB_DATARECEIVED             = None
    callback_DataReceived       = None
    callbackFwd_DataReceived    = None

    CB_DEVICECHANGED            = None
    callback_DeviceChanged      = None
    callbackFwd_DeviceChanged   = None

    #========================================================================================================
    #=== EXECUTION / DIAGNOSTICS ============================================================================
    #========================================================================================================

    # Library file executed directly?

    writefile = open("rawdata.csv", "w")
    writefile.write('Channel,Time'+'\n')
    if __name__ == '__main__':

        # Run diagnostic test...
        ConsolePrint("=========================================")
        ConsolePrint("=========  K r o m e k   L i b  =========")
        ConsolePrint("========= D I A G N O S T I C S =========")
        ConsolePrint("=========================================")

        # Initialize the library
        init_success = Kromek_Initialize(setErrorCallback=True, errorCallbackFunction=ExampleCallback_Error)
        ConsolePrint(["*** Library initialization FAILED! ***", "Library successfully initialized!"][init_success], isVerboseOutput=False)

        # Print the version information
        productVersion, majorVersion, minorVersion, buildVersion = Kromek_GetDriverVersion()
        ConsolePrint("Kromek Driver Version    : v " + str(productVersion) + "." + str(majorVersion) + "." + str(minorVersion) + "." + str(buildVersion))
        ConsolePrint("pyKromek Library Version : v " + versionLib)

        # Print the user configured settings
        ConsolePrint("                 =-=-=                   ")
        ConsolePrint("Request for status msgs  : " + str(diagnostics_PrintStatusEvents))
        ConsolePrint("Request for data events  : " + str(diagnostics_PrintRawDataEvents))
        ConsolePrint("Request for CSV output   : " + str(diagnostics_Write_CSVs))
        ConsolePrint("Request for histograms   : " + str(diagnostics_Histogram_enabled))
        ConsolePrint("                 =-=-=                   ")

        # Set device changed callback (for device connect/disconnect messages)?
        if diagnostics_PrintStatusEvents:
            ConsolePrint("Setting device changed callback...")
            Kromek_SetDeviceChangedCallback(ExampleCallback_DeviceChanged)

        # Start querying the detectors...
        ConsolePrint("Querying detectors...")

        # Send zero to get ID of first detector, if it exists
        nextDetectorID = Kromek_GetDetectorID_FirstOrNext()
        detectorCount = 0
        # 'nextDetectorID' will be an int (>0 = True), else False if no detectors were found
        
        
        while nextDetectorID:
            detectorCount += 1

            # Set 'thisDetectorID' to the returned ID #
            thisDetectorID = nextDetectorID
            ConsolePrint("=== Detector #" + str(detectorCount) + " =========================")

            # Get the type of the detector at this ID
            thisDetectorType = Kromek_GetDetectorType(thisDetectorID)
            thisDetectorSerial = Kromek_GetSerialNumber(thisDetectorID)
            ConsolePrint("Type: '" + str(thisDetectorType) + "' *** Serial # '" + str(thisDetectorSerial) + "'")

            # Is the detector already acquiring data?
            if Kromek_IsAcquiring(thisDetectorID):
                # Stop the current acquisition
                ConsolePrint("Stopping current acquisition...")
                Kromek_Acquisition_Stop(thisDetectorID)

            # Set data received callback?
            if diagnostics_PrintRawDataEvents:
                ConsolePrint("Setting data received callback...")
                DataReceived_FirstTimestamp = None
                DataReceived_TimestampOffset_ms = 0
                Kromek_SetDataReceivedCallback(ExampleCallback_DataReceived)

            # Apply factory settings
            if diagnostics_FactoryReset:
                ConsolePrint("Resetting to factory defaults...")
                success = Kromek_FactoryReset(thisDetectorID)
                ConsolePrint("Factory defaults applied!") if success else ConsolePrint("*** Factory settlings FAILED! ***")

            # Run acquisition, by preset live time
            ConsolePrint("Acquire for " + str(diagnostics_LiveTime_sec) + " seconds (Preset live time)...")
            Kromek_Acquisition_Start(thisDetectorID, liveTime_sec=int(diagnostics_LiveTime_sec))

            # Wait for acquisition to complete...
            waitTime_sec = 0
            while Kromek_IsAcquiring(thisDetectorID):
                time.sleep(1.05)
                waitTime_sec += 1
                ConsolePrint("... Elapsed time: " + str(waitTime_sec) + " sec")

            # Get acquired data
            try:
                spectrum, totalcounts, livetime, realtime = Kromek_GetAcquiredData(thisDetectorID)
                ConsolePrint("Acquisition complete!")
                ConsolePrint("Actual live time : " + str(round(livetime, 3)))
                ConsolePrint("Actual real time : " + str(round(realtime, 3)))
                if livetime > 0:
                    ConsolePrint("Total counts     : " + str(totalcounts) + " (" + str(round(totalcounts / livetime, 1)) + " cps)")
                else:
                    ConsolePrint("Total counts     : " + str(totalcounts) + " (? cps)")
                ConsolePrint("Overload counts  : " + "+" + str(spectrum[-1]) + " counts")
                ConsolePrint("Spectrum maxima  : " + str(max(spectrum[:-1])) + " counts")

                # Histogram?
                if histogramSupport and diagnostics_Histogram_enabled:
                    # Print histogram
                    ConsolePrint("Spectrum:")
                    histogram.Print_Histogram(spectrum[:-1], bincount=diagnostics_Histogram_bins, height=diagnostics_Histogram_height, markerChar='*')

                # Write CSV?
                if diagnostics_Write_CSVs:
                    ConsolePrint("Writing CSV...")
                    CSVdata = []
                    # Add headers
                    CSVdata.append("Kromek Detector Measurement" + "\n")
                    CSVdata.append("Type," + str(thisDetectorType) + "\n")
                    CSVdata.append("ID#," + str(thisDetectorSerial) + "\n")
                    CSVdata.append("\n")
                    CSVdata.append("Channel#,Counts" + "\n")
                    # Add channel data
                    for i in xrange(len(spectrum)):
                        CSVdata.append(str(i + 1) + "," + str(spectrum[i]) + "\n")
                    # Create unique filename
                    fileName_csv = "Diagnostics" + " - " + str(thisDetectorType) + " - #" + str(thisDetectorSerial) + ".csv"
                    # Write-out the file
                    f = open(fileName_csv, mode='w')
                    f.writelines(CSVdata)
                    f.close()
                    ConsolePrint("Wrote: " + "'" + fileName_csv + "'")

            # Handle error if the Kromek_GetAcquiredData() function returned False (e.g. Detector was disconnected)
            except TypeError:
                ConsolePrint("*** ERROR RETRIEVING ACQUIRED DATA! ***")

            # See if another detector exists for the loop
            nextDetectorID = Kromek_GetDetectorID_FirstOrNext(thisDetectorID)

        ConsolePrint("=========================================")

        # Diagnostics loop done
        if detectorCount == 0:
            ConsolePrint("*** No Detectors Found! ***")
            ConsolePrint("=========================================")
            ConsolePrint("Diagnostics FAILED!")
        else:
            ConsolePrint("Diagnostics COMPLETE!")

        # End of diagnostics
        ConsolePrint("Exiting...")

        # Cleanup
        Kromek_Cleanup()
    writefile.close()

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#=-= FUNCTIONS =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


def Kromek_Initialize(setErrorCallback=False, errorCallbackFunction=None):
    """
    Initialises the driver library. Sets the error callback function, if provided

    Returns:
        (bool) True or False if the library was successfully initialized
    """
    ConsolePrint("[Function: Kromek_Initialize]", isVerboseOutput=True)

    global CB_ERROR
    global callback_Error
    global callbackFwd_Error

    if setErrorCallback and errorCallbackFunction is not None:
        # Initialize the library with provided error callback function

        # Create error callback
        ConsolePrint("[Request: Set error callback]", isVerboseOutput=True)

        # Set global for the desired callback function
        callbackFwd_Error = errorCallbackFunction

        # 'ErrorCallback' type: void (stdcall *ErrorCallback)(void *pCallbackObject, unsigned int deviceID, int errorCode, const char *pMessage);
        # *** Since it's defined as a STDCALL ("stdcall *ErrorCallback"), use 'WINFUNCTYPE()' not 'CFUNCTYPE()' in Windows
        if runtime_OS == "Windows":
            CB_ERROR = WINFUNCTYPE(None, c_void_p, c_uint, c_int, c_char_p)
        else:
            CB_ERROR = CFUNCTYPE(None, c_void_p, c_uint, c_int, c_char_p)

        # Create a C-callable callback from the Python function of the same format
        callback_Error = CB_ERROR(CallbackForward_Error)

        # Format: int kr_Initialise(ErrorCallback errorCallbackFunc, void *pUserData);
        _kromek.kr_Initialise.argtypes = [CB_ERROR, c_void_p]
        _kromek.kr_Initialise.restype = c_int
        success = _kromek.kr_Initialise(callback_Error, None)

    else:
        # Initialize the library with no error callback function nor userdata

        # Format: int kr_Initialise(ErrorCallback errorCallbackFunc, void *pUserData);
        _kromek.kr_Initialise.restype = c_int
        success = _kromek.kr_Initialise(None, None)

    # Return the success value (Documentation: "1 on success, or 0 on error") as bool (True or False)
    # ** Enumerator for ERROR_OK is = 0, so documentation seems to be wrong, So: 0 on success, >0 on error..?
    if success == 0:
        ConsolePrint("[Result  : " + str(success) + "]", isVerboseOutput=True)
        return True
    else:
        ConsolePrint("[Result  : " + str(success) + "]", isVerboseOutput=True)
        return False


def Kromek_Cleanup():
    """
    Clean up the driver library on application exit.

    NOTE:
    Call on application exit or once you have finished using the library to ensure that resources used by the library have been released.

    Returns:
        (bool) True or False if cleaned-up successfully
    """
    ConsolePrint("[Function: Kromek_Cleanup]", isVerboseOutput=True)
    success = _kromek.kr_Destruct()

    # Return True or False, if successful (success value = 0 on OK, or >0 on error)
    if success == 0:
        ConsolePrint("[Result  : Cleaned-up]", isVerboseOutput=True)
        return True
    else:
        ConsolePrint("[Result  : Clean-up FAILED]", isVerboseOutput=True)
        return False


def Kromek_GetDetectorID_FirstOrNext(detectorID=0):
    """
    Gets the next detector ID # in the list after a provided ID #.
    Pass 0 to get the first detector's ID.

    NOTE:
    Device IDs are based upon the device and port that it is plugged into, and not 0 indexed

    Returns:
        (int) The ID # of the next detector in the list
        or
        (bool) False if detector not found
    """
    ConsolePrint("[Function: Kromek_GetDetectorID_FirstOrNext]", isVerboseOutput=True)

    # Create c_uint for the provided detector ID to connect to
    c_desiredDetectorID = c_uint(detectorID)

    # Get the Kromek detector by the provided index, if it exists
    # Format: unsigned int kr_GetNextDetector(unsigned int detectorID);
    _kromek.kr_GetNextDetector.restype = c_uint
    c_nextDetectorID = _kromek.kr_GetNextDetector(c_desiredDetectorID)

    # Return the found detector ID, or 'False' if detector not found
    if c_nextDetectorID != 0:
        ConsolePrint("[Result  : " + str(c_nextDetectorID) + "]", isVerboseOutput=True)
        return c_nextDetectorID
    else:
        ConsolePrint("[Result  : False]", isVerboseOutput=True)
        return False


def Kromek_Acquisition_Start(detectorID, liveTime_sec=0, realTime_sec=0):
    """
    Start an acquisition for a fixed length of time (or with no arguments to run indefinitely) on a given detector.

    NOTE:
    This command instructs a device to start receiving data.
    If a previous acquisition was performed then this call will append the counts to the previous acquisition's data.

    The live and real time parameters allow the calling application to set a limit to the amount of time to collect data.
    If both a live time and real time are supplied the detector will acquire data up until the first of the two timers expire.
    Either (or both) values can be entered as 0 to be disabled.
    Supplying 0 for both the real time and live time will cause the detector to continue acquiring data indefinitely until stopped.

    Returns:
        (bool) True or False if acquisition started successfully
    """
    ConsolePrint("[Function: Kromek_Acquisition_Start]", isVerboseOutput=True)

    # Create c_uint for the provided detector ID to connect to
    c_desiredDetectorID = c_uint(detectorID)

    # Create c_uint vars for the provided acquisition times
    c_realTime = c_uint(int(round(realTime_sec * 1000)))
    c_liveTime = c_uint(int(round(liveTime_sec * 1000)))
    if liveTime_sec > 0:
        ConsolePrint("Begin acquisition (Live time preset): " + str(c_liveTime.value) + " ms", isVerboseOutput=True)
    else:
        ConsolePrint("Begin acquisition (Real time preset): " + str(c_realTime.value) + " ms", isVerboseOutput=True)

    # Begin the acquisition
    # Format: int kr_BeginDataAcquisition(unsigned int deviceID, unsigned int realTime, unsigned int liveTime);
    success = _kromek.kr_BeginDataAcquisition(c_desiredDetectorID, c_realTime, c_liveTime)

    # Return True or False, if successful (success value = 0 on OK, or >0 on error)
    if success == 0:
        ConsolePrint("[Result  : Acquisition started]", isVerboseOutput=True)
        return True
    else:
        ConsolePrint("[Result  : Acquisition FAILED]", isVerboseOutput=True)
        return False


def Kromek_Acquisition_Stop(detectorID):
    """
    Stop the data acquisition on a given detector.

    NOTE:
    Due to the threaded nature of the driver the device will not be stopped immediately.
    In some cases, new data for the specified device may still be received for a short time following this call.
    The callback function will be called with the ERROR_ACQUISITION_COMPLETE once all data has been received.

    Returns:
        (bool) True or False if acquisition was stopped successfully
    """
    ConsolePrint("[Function: Kromek_Acquisition_Stop]", isVerboseOutput=True)

    # Create c_uint for the provided detector ID to connect to
    c_desiredDetectorID = c_uint(detectorID)

    # Stop the acquisition
    # Format: int kr_StopDataAcquisition(unsigned int deviceID);
    success = _kromek.kr_StopDataAcquisition(c_desiredDetectorID)

    # Return True or False, if successful (success value = 0 on OK, or >0 on error)
    if success == 0:
        ConsolePrint("[Result  : Stop requested]", isVerboseOutput=True)
        return True
    else:
        ConsolePrint("[Result  : Stop request FAILED]", isVerboseOutput=True)
        return False


def Kromek_Acquisition_Clear(detectorID):
    """
    Clears the data acquisition on a given detector.

    NOTE:
    Clear any stored data for the given detector.
    Real time and live time will also be cleared.

    Returns:
        (bool) True or False if acquisition was stopped successfully
    """
    ConsolePrint("[Function: Kromek_Acquisition_Clear]", isVerboseOutput=True)

    # Create c_uint for the provided detector ID to connect to
    c_desiredDetectorID = c_uint(detectorID)

    # Clear the acquisition
    # Format: int kr_ClearAcquiredData (unsigned int deviceID);
    success = _kromek.kr_ClearAcquiredData(c_desiredDetectorID)

    # Return True or False, if successful (success value = 0 on OK, or >0 on error)
    if success == 0:
        ConsolePrint("[Result  : Acquisition cleared]", isVerboseOutput=True)
        return True
    else:
        ConsolePrint("[Result  : Acquisition clearing FAILED]", isVerboseOutput=True)
        return False


def Kromek_IsAcquiring(detectorID):
    """
    Determine if the given detector is currently acquiring data.

    Returns:
        (bool) True or False if detector is currently acquiring data
    """

    # Create c_uint for the provided detector ID to connect to
    c_desiredDetectorID = c_uint(detectorID)

    # Query the detector
    # Format: int kr_IsAcquiringData(unsigned int deviceID);
    isAcquiring = _kromek.kr_IsAcquiringData(c_desiredDetectorID)

    # Return True or False, if detector is currently acquiring data
    if isAcquiring == 0:
        return False
    else:
        return True


def Kromek_GetAcquiredData(detectorID):
    """
    Retrieve the latest set of acquired data for the device.

    Returns:
        (list, int, int, int) The acquired data, total counts, live time (in sec), and real time (in sec)
        or
        (bool) False if the operation failed
    """
    ConsolePrint("[Function: Kromek_GetAcquiredData]", isVerboseOutput=True)

    # Create c_uint for the provided detector ID to connect to
    c_desiredDetectorID = c_uint(detectorID)

    # Create data buffer and other variables
    c_dataBuffer = (c_uint * 4096)()
    c_totalCounts = c_uint(0)
    c_realTime_ms = c_uint(0)
    c_liveTime_ms = c_uint(0)

    # Get the acquired data
    # Format: int kr_GetAcquiredData (unsigned int deviceID, unsigned int *pBuffer, unsigned int *pTotalCounts, unsigned int *pRealTime, unsigned int *pLiveTime);
    _kromek.kr_GetAcquiredData.argtypes = [c_uint, POINTER(c_uint * 4096), POINTER(c_uint), POINTER(c_uint), POINTER(c_uint)]
    _kromek.kr_GetAcquiredData.restype = c_int
    success = _kromek.kr_GetAcquiredData(c_desiredDetectorID, pointer(c_dataBuffer), pointer(c_totalCounts), pointer(c_realTime_ms), pointer(c_liveTime_ms))

    # Return the data or False if error (success value = 0 on OK, or >0 on error)
    if success == 0:
        # Convert data buffer to list
        spectrum = [c_dataBuffer[c] for c in range(4096)]
        return spectrum, c_totalCounts.value, c_liveTime_ms.value / 1000.0, c_realTime_ms.value / 1000.0
    else:
        return False


def Kromek_GetDetectorType(detectorID):
    """
    Gets the type of the detector, by provided ID #
    e.g. Returns: "GR1", "SIGMA 25", etc.

    Returns:
        (string) The type of the detector
        or
        (bool) False if detector not found
    """
    ConsolePrint("[Function: Kromek_GetDetectorType]", isVerboseOutput=True)

    # Create c_uint for the provided detector ID to connect to
    c_desiredDetectorID = c_uint(detectorID)

    # Create string buffer for the name
    c_nameBuffer = create_string_buffer(200)
    c_nameLength = c_int(200)

    # Get the Kromek detector's name
    # Format: int kr_GetDeviceName (unsigned int deviceID, char *pBuffer, int bufferSize, int *pNumBytesOut);
    success = _kromek.kr_GetDeviceName(c_desiredDetectorID, c_nameBuffer, c_nameLength, pointer(c_nameLength))

    # Return the name or False if error (success value = 0 on OK, or >0 on error)
    if success == 0:
        ConsolePrint("[Result  : '" + str(c_nameBuffer.value) + "']", isVerboseOutput=True)
        return c_nameBuffer.value
    else:
        ConsolePrint("[Result  : False]", isVerboseOutput=True)
        return False


def Kromek_GetSerialNumber(detectorID):
    """
    Retrieve the serial number from the detector.

    Returns:
        (string) The serial number of the detector
        or
        (bool) False if the operation failed
    """
    ConsolePrint("[Function: Kromek_GetSerialNumber]", isVerboseOutput=True)

    # Create c_uint for the provided detector ID to connect to
    c_desiredDetectorID = c_uint(detectorID)

    # Create char buffer for the serial number
    c_serialBuffer = create_string_buffer(200)
    c_serialLength = c_int(200)

    # Get the detector's serial number
    # Format: int kr_GetDeviceSerial (unsigned int deviceID, char *pBuffer, int bufferSize, int *pNumBytesOut);
    success = _kromek.kr_GetDeviceSerial(c_desiredDetectorID, c_serialBuffer, c_serialLength, pointer(c_serialLength))

    # Return the data or False if error (success value = 0 on OK, or >0 on error)
    if success == 0:
        ConsolePrint("[Result  : '" + str(c_serialBuffer.value) + "']", isVerboseOutput=True)
        return c_serialBuffer.value
    else:
        ConsolePrint("[Result  : False]", isVerboseOutput=True)
        return False


def Kromek_GetDriverVersion():
    """
    Retrieve the version information from the device driver.

    NOTE:
    Not to be confused with the firmware version of the physical device.

    Returns:
        (int, int, int, int) The versions: product, major, minor, and build
    """
    ConsolePrint("[Function: Kromek_GetDriverVersion]", isVerboseOutput=True)

    # Create c variables
    c_productVersion = c_int(0)
    c_majorVersion = c_int(0)
    c_minorVersion = c_int(0)
    c_buildVersion = c_int(0)

    # Get the version information
    # Format: void kr_GetVersionInformation(int *pProduct, int *pMajor, int *pMinor, int *pBuild);
    _kromek.kr_GetVersionInformation(pointer(c_productVersion), pointer(c_majorVersion), pointer(c_minorVersion), pointer(c_buildVersion))

    # Return the version information
    return c_productVersion.value, c_majorVersion.value, c_minorVersion.value, c_buildVersion.value


def Kromek_FactoryReset(detectorID):
    """
    Resets probe to factory defaults (gain & LLD)

    Returns:
        (bool) True or False if defaults applied successfully
    """
    ConsolePrint("[Function: Kromek_FactoryReset]", isVerboseOutput=True)

    # Create c_uint for the provided detector ID to connect to
    c_desiredDetectorID         = c_uint(detectorID)

    # Get the detector type
    detectorType = Kromek_GetDetectorType(detectorID)

    # Set the factory default values
    if detectorType == "SIGMA 25":
        # "SIGMA 25":
        #   define EVENT_DEADTIME           5.813E-05
        #   define DEFAULT_LLD              80
        #   define DEFAULT_GAIN			    0
        #   define DEFAULT_DIFF_GAIN		240
        #   define DEFAULT_HIGH_VOLTAGE	    0
        #   define DEFAULT_WARMUP_TIME		60
        c_newGain = c_byte(0)
        c_newLLD = c_ushort(80)
    elif detectorType == "SIGMA 50":
        # "SIGMA 50":
        #    define EVENT_DEADTIME          5.813E-05
        #    define DEFAULT_LLD             80
        #    define DEFAULT_GAIN			0
        #    define DEFAULT_DIFF_GAIN		240
        #    define DEFAULT_HIGH_VOLTAGE	0
        #    define DEFAULT_WARMUP_TIME		60
        c_newGain = c_byte(0)
        c_newLLD = c_ushort(80)
    elif detectorType == "GR1" or detectorType == "GR1A":
        # "GR1" / "GR1A"
        #   define EVENT_DEADTIME			1.0e-5
        #   define DEFAULT_LLD				32
        #   define DEFAULT_GAIN			    0
        #   define DEFAULT_DIFF_GAIN		240
        #   define DEFAULT_HIGH_VOLTAGE	    0
        #   define DEFAULT_WARMUP_TIME		60
        c_newGain = c_byte(0)
        c_newLLD = c_ushort(48)  # Better than factory default
    elif detectorType == "TN15":
        # "TN15"
        #   define EVENT_DEADTIME           5.813E-05
        #   define DEFAULT_LLD              250
        #   define DEFAULT_GAIN			    0
        #   define DEFAULT_DIFF_GAIN		240
        #   define DEFAULT_HIGH_VOLTAGE	    0
        #   define DEFAULT_WARMUP_TIME		60
        c_newGain = c_byte(0)
        c_newLLD = c_ushort(250)
    else:
        ConsolePrint("*** Unsupported detector for Factory Reset! ***")
        return False

    # Set enumerator values
    c_HIDREPORTNUMBER_SETGAIN       = c_int(0x02)
    c_HIDREPORTNUMBER_SETLLD_TYPE1  = c_int(0x01)
    c_HIDREPORTNUMBER_SETLLD_TYPE2  = c_int(0x09)

    # Send commands...
    # -- Gain
    # Format: int kr_SendInt8ConfigurationCommand(unsigned int deviceID, ConfigurationCommandsEnum commandNumber, unsigned char command);
    success = _kromek.kr_SendInt8ConfigurationCommand(c_desiredDetectorID, c_HIDREPORTNUMBER_SETGAIN, c_newGain)
    ConsolePrint("[New gain set: " + str(c_newGain.value) + "]", isVerboseOutput=True) if success == 0 else None
    # -- LLD
    if success == 0:
        # ... Method #1
        # Format: int kr_SendInt16ConfigurationCommand(unsigned int deviceID, ConfigurationCommandsEnum commandNumber, unsigned short command);
        success = _kromek.kr_SendInt16ConfigurationCommand(c_desiredDetectorID, c_HIDREPORTNUMBER_SETLLD_TYPE1, c_newLLD)
        if success == 0:
            ConsolePrint("[New LLD set: " + str(c_newLLD.value) + "]", isVerboseOutput=True)
        else:
            # ... Method #2
            # Format: int kr_SendInt16ConfigurationCommand(unsigned int deviceID, ConfigurationCommandsEnum commandNumber, unsigned short command);
            success = _kromek.kr_SendInt16ConfigurationCommand(c_desiredDetectorID, c_HIDREPORTNUMBER_SETLLD_TYPE2, c_newLLD)
            ConsolePrint("[New LLD set: " + str(c_newLLD.value) + "]", isVerboseOutput=True) if success == 0 else None


    # Return True or False, if successful (success value = 0 on OK, or >0 on error)
    if success == 0:
        ConsolePrint("[Result  : Factory settings applied]", isVerboseOutput=True)
        return True
    else:
        ConsolePrint("[Result  : Factory settings FAILED]", isVerboseOutput=True)
        return False


def Kromek_SetDeviceChangedCallback(callbackFn):
    """
    Sets a call back function for the following events:
    - When a new device is connected
    - When an existing device is disconnected

    Returns:
        (None)
    """
    ConsolePrint("[Function: Kromek_SetDeviceChangedCallback]", isVerboseOutput=True)

    global CB_DEVICECHANGED
    global callback_DeviceChanged
    global callbackFwd_DeviceChanged

    # Create error callback...
    # Format: void (stdcall *DeviceChangedCallback)(unsigned int deviceID, BOOL added, void *pObject);
    # *** Since it's defined as a STDCALL ("stdcall *DeviceChangedCallback"), use 'WINFUNCTYPE()' not 'CFUNCTYPE()' in Windows
    if runtime_OS == "Windows":
        CB_DEVICECHANGED = WINFUNCTYPE(None, c_uint, c_bool, c_void_p)
    else:
        CB_DEVICECHANGED = CFUNCTYPE(None, c_uint, c_bool, c_void_p)

    # Set global for the desired callback function
    callbackFwd_DeviceChanged = callbackFn

    # Create a C-callable callback from the Python function of the same format
    callback_DeviceChanged = CB_DEVICECHANGED(CallbackForward_DeviceChanged)

    # Set the callback
    # Format: void kr_SetDeviceChangedCallback(DeviceChangedCallback callbackFunc, void *pUserData);
    _kromek.kr_SetDeviceChangedCallback.argtypes = [CB_DEVICECHANGED, c_void_p]
    _kromek.kr_SetDeviceChangedCallback.restype = None
    _kromek.kr_SetDeviceChangedCallback(callback_DeviceChanged, None)


def Kromek_SetDataReceivedCallback(callbackFn):
    """
    Sets a call back function for the following events:
    - For each measured pulse within the detector during an acquisition

    The callback function will receive a timestamp, channel number, and counts received in that channel (typically 1).

    This is very similar to CANBERRA's TLIST mode.

    NOTE:
    Beware with use for high count rate applications, as each signal event will trigger the defined callback.
    e.g. For a 1000 cps measurement, the callback will be called 1000 times/sec

    Returns:
        (None)
    """
    ConsolePrint("[Function: Kromek_SetDataReceivedCallback]", isVerboseOutput=True)

    global CB_DATARECEIVED
    global callback_DataReceived
    global callbackFwd_DataReceived

    # Create callback...
    # Format: void (stdcall *DataReceivedCallback)(void *pCallbackObject, unsigned int deviceID, long long timestamp, int channelNumber, int numCounts);
    # *** Since it's defined as a STDCALL ("stdcall *DataReceivedCallback"), use 'WINFUNCTYPE()' not 'CFUNCTYPE()' in Windows
    if runtime_OS == "Windows":
        CB_DATARECEIVED = WINFUNCTYPE(None, c_void_p, c_uint, c_longlong, c_int, c_int)
    else:
        CB_DATARECEIVED = CFUNCTYPE(None, c_void_p, c_uint, c_longlong, c_int, c_int)

    # Set global for the desired callback function
    callbackFwd_DataReceived = callbackFn

    # Create a C-callable callback from the Python function of the same format
    callback_DataReceived = CB_DATARECEIVED(CallbackForward_DataReceived)

    # Set the callback
    # Format: void kr_SetDataReceivedCallback(DataReceivedCallback callbackFunc, void *pUserData);
    _kromek.kr_SetDataReceivedCallback.argtypes = [CB_DATARECEIVED, c_void_p]
    _kromek.kr_SetDataReceivedCallback.restype = None
    _kromek.kr_SetDataReceivedCallback(callback_DataReceived, None)


#========================================================================================================
#=== CALLBACK FORWARDERS ================================================================================

def CallbackForward_Error(pCallbackObject, deviceID, errorCode, errorMessage):
    """
    Triggered on any library/communication errors, and forwards the event to the set callback function.

    *** This is a strictly defined function for the C callback from the driver *** Do not modify arguments ***

    Format: void (stdcall *ErrorCallback)(void *pCallbackObject, unsigned int deviceID, int errorCode, const char *pMessage);
    """
    global callbackFwd_Error

    # Create named tuple to forward to callback
    ErrorEvent = namedtuple("ErrorEvent", "deviceID errorCode errorMessage")(deviceID, errorCode, errorMessage)

    # Forward to callback
    callbackFwd_Error(ErrorEvent)


def CallbackForward_DeviceChanged(deviceID, deviceAdded, errorCode):
    """
    Triggered if 'Kromek_SetDeviceChangedCallback()' has been set and any device changed events occur, and forwards the event to the set callback function.

    *** This is a strictly defined function for the C callback from the driver *** Do not modify arguments ***

    Format: void (stdcall *DeviceChangedCallback)(unsigned int deviceID, BOOL added, void *pObject);
    """
    global callbackFwd_DeviceChanged

    # Create named tuple to forward to callback
    DeviceEvent = namedtuple("DeviceEvent", "deviceID deviceAdded errorCode")(deviceID, deviceAdded, errorCode)

    # Forward to callback
    callbackFwd_DeviceChanged(DeviceEvent)


def CallbackForward_DataReceived(pCallbackObject, deviceID, timestamp, channel, numCounts):
    """
    Triggered if 'Kromek_SetDataReceivedCallback()' has been set and any measurement events occur, and forwards the data to the set callback function.

    *** This is a strictly defined function for the C callback from the driver *** Do not modify arguments ***

    Format: void (stdcall *DataReceivedCallback)(void *pCallbackObject, unsigned int deviceID, long long timestamp, int channelNumber, int numCounts);
    """
    global callbackFwd_DataReceived

    # Create named tuple to forward to callback
    DataEvent = namedtuple("DataEvent", "deviceID timestamp channel counts")(deviceID, timestamp, channel, numCounts)

    # Forward to callback
    callbackFwd_DataReceived(DataEvent)


#========================================================================================================
#=== EXAMPLE CALLBACK RECEIVERS =========================================================================

def ExampleCallback_Error(event):
    """
    Example callback receive function for any library/communication errors.

    Data is received as a named tuple, with the following fields, accessible via:
        event.deviceID (as int)
        event.errorCode (as int)
        event.errorMessage (as string)

    The event is received and the error is printed to the terminal.

    Example of use with the pyKromek library, during initialization, setting this function as the callback:

        init_success = Kromek_Initialize(setErrorCallback=True, errorCallbackFunction=ExampleCallback_Error)

    Error codes, passed as errorCode (int):
        ERROR_OK                    = 0
        ERROR_DEVICE_OPEN_FAILED    = 100
        ERROR_READ_FAILED           = 101
        ERROR_INTERNAL_DEVICE       = 102
        ERROR_WRITE_FAILED          = 103
        ERROR_UNKNOWN               = 5
        ERROR_NOT_INITIALISED       = 6
        ERROR_INVALID_DEVICE_ID     = 7
        ERROR_ACQUISITION_COMPLETE  = 8
    """
    # What's the error code?
    if event.errorCode == 8:
        # Acquisition complete
        ConsolePrint("*** EVENT: ACQUISITION COMPLETE ***", isVerboseOutput=True)
    elif event.errorCode == 7:
        # Invalid device ID
        ConsolePrint("*** ERROR: INVALID DEVICE ID! ***", isVerboseOutput=False)
    else:
        # Other error code provided...
        ConsolePrint("*** ERROR *** Code: " + str(event.errorCode) + ", Message: '" + event.errorMessage + "' ***", isVerboseOutput=False)


def ExampleCallback_DeviceChanged(event):
    """
    Example callback receive function for the 'Kromek_SetDeviceChangedCallback()'.

    Data is received as a named tuple, with the following fields, accessible via:
        event.deviceID (as int)
        event.deviceAdded (as bool)
        event.errorCode (as int)

    The event is received and the device status is printed to the terminal.

    Example of use with the pyKromek library, setting this function as the callback:

        Kromek_SetDeviceChangedCallback(ExampleCallback_DeviceChanged)

    Error codes:
        ERROR_OK                    = 0
        ERROR_DEVICE_OPEN_FAILED    = 100
        ERROR_READ_FAILED           = 101
        ERROR_INTERNAL_DEVICE       = 102
        ERROR_WRITE_FAILED          = 103
        ERROR_UNKNOWN               = 5
        ERROR_NOT_INITIALISED       = 6
        ERROR_INVALID_DEVICE_ID     = 7
        ERROR_ACQUISITION_COMPLETE  = 8
    """
    # Connected or disconnected?
    thisDetectorType = Kromek_GetDetectorType(event.deviceID)
    thisSerial = Kromek_GetSerialNumber(event.deviceID)
    if event.deviceAdded is True:
        ConsolePrint("*** DEVICE EVENT: CONNECTED *** (Type: '" + thisDetectorType + "', Serial# '" + str(thisSerial) + "')", isVerboseOutput=False)
    elif event.deviceAdded is False:
        ConsolePrint("*** DEVICE EVENT: DISCONNECTED *** (Type: '" + thisDetectorType + "', Serial# '" + str(thisSerial) + "')", isVerboseOutput=False)
    else:
        ConsolePrint("*** DEVICE EVENT *** (Type: '" + thisDetectorType + "', Serial# '" + str(thisSerial) + "') ErrorCode = " + str(event.errorCode), isVerboseOutput=False)


def ExampleCallback_DataReceived(event):
    """
    Example callback receive function for the 'Kromek_SetDataReceivedCallback()'.

    Data is received as a named tuple, with the following fields, accessible via:
        event.deviceID (as int)
        event.timestamp (as long long)
        event.channel (as int)
        event.counts (as int)

    The data is received, the timestamp is adjusted to be relative, and the data is simply printed to the terminal.

    Example of use with the pyKromek library, setting this function as the callback:

        DataReceived_FirstTimestamp = None
        DataReceived_TimestampOffset_ms = 0
        Kromek_SetDataReceivedCallback(ExampleCallback_DataReceived)

    """
    global DataReceived_FirstTimestamp
    global DataReceived_TimestampOffset_ms

    # Format the timestamp
    #TODO: Perhaps it's in seconds, like so:
    # Pseudo code: utc = 1980-01-06UTC + (gps - (leap_count(2014) - leap_count(1980)))
    # Code:
    #    utc = datetime(1980, 1, 6) + timedelta(seconds=1092121243.0 - (35 - 19))
    #    print(utc)
    # where leap_count(date) is the number of leap seconds introduced before the given date
    # so: (leap_count(2014) - leap_count(1980)) == (35 - 19)
    if DataReceived_FirstTimestamp is None:
        DataReceived_FirstTimestamp = event.timestamp
    relative_milliseconds = ((event.timestamp - DataReceived_FirstTimestamp) / 10.0 / 1e3) + DataReceived_TimestampOffset_ms

    writefile.write(str(event.channel)+','+'{:0.4f}'.format(relative_milliseconds) + " \n")


#========================================================================================================
#=== UTILITY FUNCTIONS ==================================================================================

def VerboseOutput(true_or_false):
    """
    Enable or disable verbose output of the library.

    """
    global verboseOutput

    if true_or_false is True:
        verboseOutput = True
    else:
        verboseOutput = False


def ConsolePrint(message, isVerboseOutput=False):
    if isVerboseOutput:
        print(('{0:<' + str(outputPrefixPadding) + '}{1:<15}').format(outputPrefix, message)) if verboseOutput else None
    else:
        print(('{0:<' + str(outputPrefixPadding) + '}{1:<15}').format(outputPrefix, message))

def runAnalyzer(loop):
############################################################################################
	# Import the data
	raw_data = pd.read_csv('rawdata.csv')
	back_data = pd.read_csv('backdata.csv')
############################################################################################
	# The following code sets up the bins used to lower the channel count from 
	# 4096 to 1024 and then adds the bins to the pandas data-frame
	upper = 4
	bins = []

	for i in range(1024):
		bins.append(upper)
		upper = upper+4
		
	raw_data['Channel Bin'] = pd.cut(raw_data['Channel'], bins = bins, labels = range(1023))
############################################################################################
	#The following code sets up the bins used range the time from beginning to end
	index = int(raw_data['Time'].iloc[-1]/1000)+1
	upper = 0
	bins = []

	for i in range(index):
		bins.append(upper)
		upper = upper + 1
	bins.append(upper)

	raw_data['Time(s)'] = raw_data['Time'] / 1000
	raw_data['Time Bins'] = pd.cut(raw_data['Time']/1000,
		 bins = bins, labels = np.array(range(index))+1 )
############################################################################################
	# The following code determines the energy level of each channel
	energy_range= np.array(range(1024))+1
	energy_range = 9.22+2.02*energy_range
############################################################################################
	# The following code determines the energy of each count
	count_energy = np.array(raw_data['Channel Bin'])
	count_energy = 9.22+2.02*count_energy
	raw_data['Energy (keV)'] = count_energy
############################################################################################
	# The following code determines the bin counts of each channel
	channel_count = []
	channels = (np.array(range(1024))+1)

	for i in range(1024):
	  channel_count.append(sum(raw_data['Channel Bin'] == i+1))
	channel_count = np.array(channel_count)  
############################################################################################
	# The following code determines the estimated background radiation
	back_est = np.array(back_data['Slope'])*raw_data['Time'].iloc[-1]

	back_sub = []
	for i in range(1024):
	  back_sub.append(max(channel_count[i]-back_est[i],0))

	back_sub = np.array(back_sub)
############################################################################################
	# The following code determines weather or not a given channel has peaked above the 
	# expected background radiation by a ratio of 8
	peaks = []
	for i in range(1024):
		if back_est[i] > 0:
			peaks.append(channel_count[i]/back_est[i])
		elif back_est[i] <= 0 :
			peaks.append(channel_count[i])
			
	peak_ratio = 8
	
	for i in range(1024):
		if peaks[i] >= peak_ratio:
			peaks[i] = 1
		elif peaks[i] < peak_ratio:
			peaks[i] = 0
	
	peaks = np.array(peaks)
	
	if sum(peaks) >=14 :
		present_radiation = 'Yes'
	elif sum(peaks) < 14 : 
		present_radiation = 'No'
	
	
############################################################################################
	# The following code sets up some of the settings for plotting
	plot = True
	if plot == True:
		plt.rcParams['axes.facecolor'] = 'silver'
		plt.hot()
		plotx = np.array(raw_data['Energy (keV)'])
		ploty = (np.array(raw_data['Time']))/1000
		scale_b =  0.00003**2*(plotx)**3
############################################################################################
		# The following code plots the data over time on a scatter plot
		plt.subplot(3,1,1)
		plt.scatter(ploty,
					plotx,
					s = scale_b,
					c=plotx,
					alpha = 0.65)

		plt.xlabel('Time (s)')
		plt.ylabel('Energy (keV)')
		plt.title('Radiation Counts Over Time')
############################################################################################
		# The following forms the Line plot
		plt.subplot(3,1,2)
		plt.plot(energy_range,
				 channel_count,
				 color = 'black',
				 lw = 0.15,
				 alpha = 0.9)
		plt.scatter(energy_range,
					channel_count, 
					c = channel_count,
					s = 0.2,
					alpha = 0.6)
		plt.xlabel('Energy (keV)')
		plt.ylabel('Counts')
		plt.title('Accumulated Radiation Counts per Energy Level')
############################################################################################
		# The following code properly arranges the plots and saves the figure before
		# showing the plot
		plt.figtext(0.45,0.2,s = 'Total number of unexpected peaks     :    ' + str(sum(peaks)))
		plt.figtext(0.425,0.125,s = 'Was radiation present during measurement time?     :    ' + present_radiation)
		plt.tight_layout()
		
		manager = plt.get_current_fig_manager()     
		
		manager.window.state('zoomed')
		plt.savefig('Radiation Detection Run.png')
		
		if loop.lower() == 'yes':
			plt.show(block = False)
			plt.pause(10)
			plt.close()
		else:
			plt.show(block = True)
############################################################################################
# The following code runs the program
while True:
    loop = input('Are you performing looping measurements? "yes" or "no"    ')

    while loop.lower() != 'yes' and loop.lower() != 'no':
        print('Enter "yes" or "no"')
        loop = input('Are you performing looping measurements? "yes" or "no"    ')
    
    try:    
        if loop.lower() == 'yes':
            while True:
                runDetect(loop)
                runAnalyzer(loop)
                plt.pause(10)
        else:
            runDetect(loop)
            runAnalyzer(loop)
    except KeyboardInterrupt:
        print('Exiting looping status')
