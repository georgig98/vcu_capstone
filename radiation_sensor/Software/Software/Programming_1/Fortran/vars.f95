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

integer, parameter :: input = 101                   ! input integer number
integer, parameter :: output1 = 201                  ! output integer number
integer, parameter :: output2 = 202                 ! ditto
integer, parameter :: nc = 4096                     ! number of channels
integer, allocatable :: counts(:)                   ! radiation channel count
integer, allocatable :: channelmod(:)               ! modified channel counts
integer, allocatable :: logchannel(:)                ! logrithmic channel comparison
integer :: ndc                                      ! number of (desired) channels 
integer :: channel(4096)                            ! channel counter
integer :: nlines                                   ! number of lines in the input file
integer :: i, j, k                                  ! simple counters (may only need one)
integer :: n, l, summ                               ! simple placeholder
integer :: ierr                                     ! error input reader 
integer :: x, y                                     ! two counter placeholders 
integer :: cnt                                      ! used in splitting channel data
integer :: time										! time stamp

real, allocatable :: energymod(:)                   ! energy modified per channels
real :: energy(4096)                                ! energy for a given channel
real :: e, e1, e2                                   ! energy markers for a given channel
real :: c, c1, c2                                   ! channel markers for a given energy
real :: nrg                                         ! used in splitting channel data

! The following are input and output file names

character(len = 7), parameter :: infile = 'raw.txt'     
character(len = 13) :: outfile2 = 'sortedmod.txt'
character(len = 10) :: outfile = 'sorted.txt'

! To prevent confusion and make programming the curve fitting easier on myself, 
! the following group of variables are set specifically for that putpose. (power curve) 
!========================================================================================
real, allocatable :: energylog(:)                   ! energy modified per LOG
real, dimension(6,7) :: solver						! 6 by 7 array to solve function
real :: coefficients(6)
real :: store(6)                                    ! storage array
real :: factor                                      ! factor for calculations

integer, parameter :: order =  5                    ! order of the polynomial
integer :: po, ne                                   ! pos and neg value counter

end module vars