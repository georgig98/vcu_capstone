! Programmed and owned by Hubert E. Coburn II (2-25-2019)

!========================================================================================
! The following main program determines the expected radiation formulas over all channels
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

program main
use vars
implicit none

! Read the background input file
call inread

! Check the arrays
call arrays

! Write the background formula for each channel
call outwrite

! Run the debugger
!call debugger

end program main