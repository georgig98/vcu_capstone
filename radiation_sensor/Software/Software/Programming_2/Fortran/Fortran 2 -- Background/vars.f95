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


integer, allocatable :: countsl1(:)                         ! Low and high counts of
integer, allocatable :: countsh1(:)                         ! the 5 measurements taken

integer, allocatable :: countsl2(:)
integer, allocatable :: countsh2(:)

integer, allocatable :: countsl3(:)
integer, allocatable :: countsh3(:)

integer, allocatable :: countsl4(:)
integer, allocatable :: countsh4(:)

integer, allocatable :: countsl5(:)
integer, allocatable :: countsh5(:)

integer, allocatable :: counts(:)


integer :: nlines                                           ! line counter
integer, parameter :: input = 101                           ! in file numbers    
integer, parameter :: input1 = 102                          
integer, parameter :: input2 = 103
integer, parameter :: input3 = 104
integer, parameter :: input4 = 105
integer, parameter :: input5 = 106
integer, parameter :: output = 201                          ! output file number


real, allocatable :: ts(:)                                  ! Time stamp of raw data
real, allocatable :: slope(:)                               ! slope for a given channel
real, allocatable :: countshavg(:)                          ! avg counts per high channel    
real, allocatable :: sd(:)                                  ! standard deviation of each channel


real :: tsmax                                               ! max time of measurement




character(len = 10), parameter :: infile = 'rawmod.txt'     ! input file names
character(len = 5), parameter :: infile1 = '1.txt'
character(len = 5), parameter :: infile2 = '2.txt'
character(len = 5), parameter :: infile3 = '3.txt'
character(len = 5), parameter :: infile4 = '4.txt'
character(len = 5), parameter :: infile5 = '5.txt'
character(len = 19),parameter :: outfile = 'BACKGROUND_DATA.TXT'  ! output file name


end module vars