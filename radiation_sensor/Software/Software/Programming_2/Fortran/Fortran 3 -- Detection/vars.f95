! Programmed and owned by Hubert E. Coburn II

!========================================================================================
! The following module provides the variables for reading, manipulating, and writing data 
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

module vars
implicit none

! The following provides variables for the main program's looping
!========================================================================================
integer :: i                                                ! basic counter
integer :: ierr                                             ! error input reader 


integer :: nlines                                           ! line counter
integer, parameter :: input1 = 101                          ! in file numbers
integer, parameter :: input2 = 102
integer, parameter :: input3 = 103

integer, parameter :: output = 201                          ! output file number

integer, allocatable :: counts(:)                           ! counts of each channel
integer, allocatable :: rawdata(:)                          ! raw counts of each channel
integer, allocatable :: expected(:)                         ! expected counts of each channel
integer, allocatable :: peaks(:)                            ! peak points



real, allocatable :: ts(:)                                  ! Time stamp of raw data
real, allocatable :: slope(:)                               ! slope for a given channel
real, allocatable :: energies(:)                            ! energy of each channel
real, allocatable :: std(:)                                 ! standard deviation of each channel
real, allocatable :: ratio(:)                               ! ratio of actual to expected


real :: tsmax                                               ! max time of measurement




character(len = 10), parameter :: infile1 = 'rawmod.txt'     ! input file names
character(len = 19), parameter :: backfile = 'BACKGROUND_DATA.TXT'
character(len = 13),parameter :: infile2 = 'sortedmod.txt'
character(len = 13),parameter :: outfile = 'PEAK_DATA.TXT'               ! output file name


end module vars