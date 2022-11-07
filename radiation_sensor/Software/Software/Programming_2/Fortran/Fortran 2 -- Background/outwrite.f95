! Programmed and owned by Hubert E. Coburn II (2-8-2019)

!========================================================================================
! The following program writes the output of the background formulae
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine outwrite
use vars
implicit none

! write the slope and standard deviation to the background formula file

open(unit=output,file=outfile,action='write') 

do i = 1,nlines
    write(output,11) slope(i), sd(i)
end do

11 format(1X,F15.10,T25,F15.10)

end subroutine outwrite