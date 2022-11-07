! Programmed and owned by Hubert E. Coburn II (3-11-2019)

!========================================================================================
! The following program writes the output of the peak detection
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine outwrite
use vars
implicit none

open(unit=output,file=outfile,action='write')

do i = 1, nlines
    write(output,12) peaks(i),energies(i)
end do

12 format(X,I1,T10,F7.2) 

end subroutine outwrite