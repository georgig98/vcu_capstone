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
    
    if loop == 'yes':
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
