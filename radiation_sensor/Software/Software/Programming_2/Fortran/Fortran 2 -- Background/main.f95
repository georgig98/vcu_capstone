! Programmed and owned by Hubert E. Coburn II (2-6-2019)

!========================================================================================
! The following main program determines the expected radiation formulas over all channels
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

program main
use vars
implicit none

! Read the input file
call inread

! Determine slope and intercept for each channel
call backdata

! Write the background formula for each channel
call outwrite

end program main